#!/bin/bash
# Session-start hook for video-edits.
# Converts storyboard (.tsv / .csv / .xlsx) → README.md per project.
# Synchronous, fast (<5s), only runs in remote (cloud) env.

set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(pwd)}"

# openpyxl needed only if any project has script_plan.xlsx and no faster format
if find video-edits/projects -maxdepth 3 -name "script_plan.xlsx" 2>/dev/null | grep -q .; then
  if ! python3 -c "import openpyxl" 2>/dev/null; then
    pip install --quiet --disable-pip-version-check openpyxl >/dev/null 2>&1 || {
      echo "Session-start hook: failed to install openpyxl (xlsx projects may skip)" >&2
    }
  fi
fi

python3 .claude/hooks/convert_xlsx_to_readme.py video-edits/projects || true
