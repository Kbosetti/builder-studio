#!/bin/sh
# Copies the shared integration (api/ + lib/) from this folder into other Mitchell landing page projects.
# Source of truth is here. Run after editing lib/ or api/, then deploy each target.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
for TARGET in "$@"; do
  mkdir -p "$TARGET/api" "$TARGET/lib"
  cp "$HERE"/api/*.js "$TARGET/api/"
  cp "$HERE"/lib/*.js "$TARGET/lib/"
  cp "$HERE/package.json" "$TARGET/package.json"
  echo "synced -> $TARGET"
done
