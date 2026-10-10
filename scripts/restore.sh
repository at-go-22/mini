#!/usr/bin/env bash
set -euo pipefail

ARCHIVE="${1:-}"
if [ -z "$ARCHIVE" ]; then
  echo "Usage: $0 /path/to/backup.tar.gz" >&2
  exit 1
fi

if [ ! -f "$ARCHIVE" ]; then
  echo "Backup not found: $ARCHIVE" >&2
  exit 1
fi

tar -xzf "$ARCHIVE" -C .
echo "Restore complete from $ARCHIVE"
