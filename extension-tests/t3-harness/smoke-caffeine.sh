#!/usr/bin/env bash
# T3 preparation: Caffeine-only smoke run. NOT part of T3.
#
# Confirms that the runtime serves governed requests through its full pipeline,
# with provisioning supplied only by environment variables and request headers,
# so that no protected file needs editing. No Redis is started.
#
# Usage: smoke-caffeine.sh <output-dir>
set -euo pipefail

OUT="${1:?output directory required}"
mkdir -p "$OUT"
RUNTIME="${PROTOTYPES:-$HOME/Desktop/AI Projects}/Enterprise_AI_Runtime_Service"
JAVA_HOME="${JAVA_HOME:-$(mvn -v | sed -n 's/.*runtime: //p')}"
GW_PORT=18080; RT_PORT=18081; GW_NAME=t3-smoke-gateway
WIREMOCK_IMAGE="wiremock/wiremock:3.9.1"   # the image RuntimeServiceIT uses

log() { echo "[$(date -u +%H:%M:%SZ)] $*" | tee -a "$OUT/smoke.log"; }
cleanup() {
  [[ -n "${RT_PID:-}" ]] && kill "$RT_PID" 2>/dev/null || true
  docker rm -f "$GW_NAME" >/dev/null 2>&1 || true
}
trap cleanup EXIT

log "runtime revision: $(git -C "$RUNTIME" rev-parse HEAD); status: $(git -C "$RUNTIME" status --short . | wc -l | tr -d ' ') changed files"
log "building runtime-api from current source"
( cd "$RUNTIME" && mvn -q -o -pl runtime-api -am package -DskipTests )
JAR="$RUNTIME/runtime-api/target/runtime-api-1.0.0-SNAPSHOT-app.jar"
log "jar sha256: $(shasum -a 256 "$JAR" | cut -d' ' -f1)"

log "starting stub gateway ($WIREMOCK_IMAGE) on $GW_PORT"
docker rm -f "$GW_NAME" >/dev/null 2>&1 || true
docker run -d --name "$GW_NAME" -p "$GW_PORT:8080" "$WIREMOCK_IMAGE" >/dev/null
for _ in $(seq 60); do curl -sf "localhost:$GW_PORT/__admin/mappings" >/dev/null && break; sleep 1; done
curl -sf -X POST "localhost:$GW_PORT/__admin/mappings" -H 'Content-Type: application/json' -d '
{"request":{"method":"POST","url":"/v1/inference/chat"},
 "response":{"status":200,"headers":{"Content-Type":"application/json"},
  "jsonBody":{"content":"Refunds are accepted within 30 days [source: refunds-policy].",
    "provider":"stub","model":"stub-model","finishReason":"STOP",
    "usage":{"inputTokens":120,"outputTokens":14,"cachedInputTokens":0},
    "cost":{"inputCost":"0.00012000","outputCost":"0.00002800","currency":"USD"}}}}' >/dev/null
curl -sf -X POST "localhost:$GW_PORT/__admin/mappings" -H 'Content-Type: application/json' -d '
{"request":{"method":"GET","url":"/v1/health"},
 "response":{"status":200,"headers":{"Content-Type":"application/json"},
  "jsonBody":{"status":"UP","providers":{"stub":"UP"}}}}' >/dev/null

# Provisioning: environment variables only. application.yml is not edited.
log "starting runtime (Caffeine) on $RT_PORT"
# Optional: RECORDER_JAR loads the harness-owned T3 recorder from outside the
# runtime's source tree, through PropertiesLauncher and loader.path.
if [[ -n "${RECORDER_JAR:-}" ]]; then
  log "loading recorder $(shasum -a 256 "$RECORDER_JAR" | cut -d' ' -f1)"
  LAUNCH=(-cp "$JAR" -Dloader.path="$RECORDER_JAR" -Dt3.instance=smoke
          -Dt3.recorder.out="${RECORDER_OUT:-$OUT/recorder.jsonl}" org.springframework.boot.loader.launch.PropertiesLauncher)
else
  LAUNCH=(-jar "$JAR")
fi
env SERVER_PORT=$RT_PORT \
    RUNTIME_ENVIRONMENT=integration \
    RUNTIME_SECURITY_MODE=NONE \
    RUNTIME_CACHE_PROVIDER=caffeine \
    MODEL_GATEWAY_URL="http://localhost:$GW_PORT" \
    "$JAVA_HOME/bin/java" "${LAUNCH[@]}" > "$OUT/runtime.log" 2>&1 &
RT_PID=$!
for _ in $(seq 90); do curl -sf "localhost:$RT_PORT/v1/ready" > "$OUT/ready.json" 2>/dev/null && break; sleep 1; done
log "ready: $(cat "$OUT/ready.json" 2>/dev/null || echo 'NOT READY')"

request() {
  curl -s -o "$OUT/$1.json" -w '%{http_code}' -X POST "localhost:$RT_PORT/v1/chat" \
    -H 'Content-Type: application/json' \
    -H 'X-Enterprise-AI-Application: retail-dashboard' \
    -H 'X-Enterprise-AI-Use-Case: policy-qa' \
    -H 'X-Enterprise-AI-Environment: integration' \
    -H 'X-Enterprise-AI-Region: australia' \
    -H 'X-Enterprise-AI-Tenant: acme' \
    -d '{"promptId":"policy-qa","messages":[{"role":"user","content":"What is the refund window?"}]}'
}
gateway_calls() {
  curl -s -X POST "localhost:$GW_PORT/__admin/requests/count" -H 'Content-Type: application/json' \
    -d '{"method":"POST","url":"/v1/inference/chat"}' | sed -n 's/.*"count" *: *\([0-9]*\).*/\1/p'
}

log "request 1: HTTP $(request first); gateway calls: $(gateway_calls)"
log "request 2: HTTP $(request second); gateway calls: $(gateway_calls)"
log "first response:  $(cat "$OUT/first.json")"
log "second response: $(cat "$OUT/second.json")"
log "runtime repository status after run: $(git -C "$RUNTIME" status --short . | wc -l | tr -d ' ') changed files"
