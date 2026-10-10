#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-./backups}"
mkdir -p "$BACKUP_DIR"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
ARCHIVE="$BACKUP_DIR/pihole-unbound-$STAMP.tar.gz"

if [ -d ./data ]; then
  tar -czf "$ARCHIVE" \
    --sort=name \
    -C . \
    ./data \
    ./config \
    .env 2>/dev/null || true
else
  tar -czf "$ARCHIVE" \
    --sort=name \
    -C . \
    ./config \
    .env 2>/dev/null || true
fi

echo "$ARCHIVE"