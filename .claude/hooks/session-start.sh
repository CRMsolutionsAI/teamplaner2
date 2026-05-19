#!/bin/bash
# Session-start hook for video-edits.
# Converts script_plan.xlsx → README.md for each project automatically.
# Synchronous (fast, <5s). Only runs in remote (cloud) env.

set -euo pipefail

# Only run in Claude Code on the web (remote env)
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(pwd)}"

# Ensure openpyxl available (fast no-op if already installed)
if ! python3 -c "import openpyxl" 2>/dev/null; then
  pip install --quiet --disable-pip-version-check openpyxl >/dev/null 2>&1 || {
    echo "Session-start hook: failed to install openpyxl" >&2
    exit 0
  }
fi

# Convert xlsx → README for every project that needs it
python3 .claude/hooks/convert_xlsx_to_readme.py video-edits/projects || true
