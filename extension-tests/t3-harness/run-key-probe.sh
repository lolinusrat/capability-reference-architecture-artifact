#!/usr/bin/env bash
# T3 assertion B5-keys: run KeyProbe in two separate JVM processes and compare.
#
# NOT TO BE RUN before the T3 protocol is frozen. Running it computes the
# B5-keys observation.
#
# Usage: run-key-probe.sh <output-dir>
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
HISTORIES="$HERE/../t3-histories.json"
RUNTIME="${PROTOTYPES:-$HOME/Desktop/AI Projects}/Enterprise_AI_Runtime_Service"
OUT="${1:?output directory required}"
mkdir -p "$OUT"
# Absolute, because Maven runs inside the runtime repository and would resolve a
# relative path there (T3 initial run, attempt 1).
OUT="$(cd "$OUT" && pwd)"

# The JDK Maven uses. On this machine /usr/bin/java is Apple's stub.
JAVA_HOME="${JAVA_HOME:-$(mvn -v | sed -n 's/.*runtime: //p')}"
JAVA="$JAVA_HOME/bin/java"; JAVAC="$JAVA_HOME/bin/javac"

# Build runtime-common and runtime-cache from the current source, so the probe
# never runs against stale classes or a stale jar in ~/.m2. No runtime source is
# modified; the probe is compiled outside the runtime's source tree.
( cd "$RUNTIME" && mvn -q -o -pl runtime-cache -am test-compile )

# Current build output first, then the module's third-party test classpath.
CP_FILE="$OUT/classpath.txt"
( cd "$RUNTIME" && mvn -q -o -pl runtime-cache dependency:build-classpath \
    -Dmdep.includeScope=test -Dmdep.outputFile="$CP_FILE" )
THIRD_PARTY="$(tr ':' '\n' < "$CP_FILE" | grep -v '/com/enterprise/ai/' | paste -sd: -)"
CP="$RUNTIME/runtime-cache/target/classes:$RUNTIME/runtime-common/target/classes:$RUNTIME/runtime-common/target/test-classes:$THIRD_PARTY"

"$JAVAC" -d "$OUT/classes" -cp "$CP" "$HERE/KeyProbe.java"

# Two separate processes, started one after the other.
"$JAVA" -cp "$OUT/classes:$CP" KeyProbe "$HISTORIES" "$OUT/keys-jvm-a.tsv"
"$JAVA" -cp "$OUT/classes:$CP" KeyProbe "$HISTORIES" "$OUT/keys-jvm-b.tsv"

# Compare history lines only; the header lines record the JVM and are expected to differ.
diff <(grep -v '^#' "$OUT/keys-jvm-a.tsv") <(grep -v '^#' "$OUT/keys-jvm-b.tsv") \
    > "$OUT/keys-diff.txt" && echo "B5-keys: all 20 keys identical across JVMs" \
    || echo "B5-keys: keys differ across JVMs; see $OUT/keys-diff.txt"
