#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${1:-${MAKEHUMAN_PLUGIN_DIR:-}}"

if [[ -z "${TARGET_DIR}" ]]; then
  echo "Usage: bin/install.sh /path/to/makehuman/plugins"
  echo "Or set MAKEHUMAN_PLUGIN_DIR."
  exit 1
fi

python "$(dirname "$0")/install.py" --target "${TARGET_DIR}"
