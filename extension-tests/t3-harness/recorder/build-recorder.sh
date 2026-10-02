#!/usr/bin/env bash
# Build the T3 recorder jar from its source, against the runtime's current build.
# Usage: build-recorder.sh <output-dir>   (prints the jar path)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
RUNTIME="${PROTOTYPES:-$HOME/Desktop/AI Projects}/Enterprise_AI_Runtime_Service"
OUT="${1:?output directory required}"; mkdir -p "$OUT/classes"
# Absolute, because Maven runs inside the runtime repository and would resolve a
# relative path there (T3 initial run, attempt 1).
OUT="$(cd "$OUT" && pwd)"
JAVA_HOME="${JAVA_HOME:-$(mvn -v | sed -n 's/.*runtime: //p')}"

( cd "$RUNTIME" && mvn -q -o -pl runtime-api -am compile )
( cd "$RUNTIME" && mvn -q -o -pl runtime-api dependency:build-classpath \
    -Dmdep.includeScope=compile -Dmdep.outputFile="$OUT/classpath.txt" )
THIRD_PARTY="$(tr ':' '\n' < "$OUT/classpath.txt" | grep -v '/com/enterprise/ai/' | paste -sd: -)"
CP="$RUNTIME/runtime-common/target/classes:$THIRD_PARTY"

# Match the runtime's own target release: Spring's bytecode reader rejects class
# files newer than it supports, and the runtime builds with a newer JDK than it targets.
RELEASE="$(sed -n 's:.*<java.version>\([0-9]*\)</java.version>.*:\1:p' "$RUNTIME/pom.xml" | head -1)"
"$JAVA_HOME/bin/javac" --release "$RELEASE" -d "$OUT/classes" -cp "$CP" "$HERE/src/t3harness/T3RecorderAutoConfiguration.java"
mkdir -p "$OUT/classes/META-INF/spring"
cp "$HERE/src/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports" \
   "$OUT/classes/META-INF/spring/"
( cd "$OUT/classes" && "$JAVA_HOME/bin/jar" cf "$OUT/t3-recorder.jar" . )
echo "$OUT/t3-recorder.jar"
