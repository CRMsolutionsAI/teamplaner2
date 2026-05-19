#!/bin/bash
# start_iter.sh — bootstrap a new iteration directory with tracking artifacts.
#
# Usage: ./start_iter.sh <project_name> <vN>
#   e.g. ./start_iter.sh project_003_yoga v1
#
# What it does:
#   1. Creates projects/<project_name>/vN_build/segs/
#   2. Copies WORKFLOW_STATE template → vN_build/WORKFLOW_STATE.md (dated)
#   3. Ensures time_log.md exists in project root (creates from template if missing)
#   4. Appends a "v_N | started HH:MM" row to time_log.md
#   5. Echoes next-steps reminder
#
# Idempotent: re-running for existing iteration does NOT overwrite WORKFLOW_STATE.md.

set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: $0 <project_name> <vN>" >&2
  echo "  e.g. $0 project_003_yoga v1" >&2
  exit 1
fi

PROJ_NAME="$1"
ITER="$2"

# Resolve paths from this script's location
UTILS_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECTS_ROOT="$(cd "$UTILS_DIR/.." && pwd)/projects"
PROJ_DIR="$PROJECTS_ROOT/$PROJ_NAME"
BUILD_DIR="$PROJ_DIR/${ITER}_build"

if [ ! -d "$PROJ_DIR" ]; then
  echo "ERR: project does not exist: $PROJ_DIR" >&2
  echo "Create it first with sources/ + README.md (or script_plan.tsv)" >&2
  exit 2
fi

# 1. Build dir
mkdir -p "$BUILD_DIR/segs"
echo "✓ created $BUILD_DIR/segs/"

# 2. WORKFLOW_STATE.md (only if missing)
WS="$BUILD_DIR/WORKFLOW_STATE.md"
if [ ! -f "$WS" ]; then
  TODAY=$(date +%Y-%m-%d)
  NOW=$(date +%H:%M)
  sed -e "s/<имя>/$PROJ_NAME/g" \
      -e "s/vN/$ITER/g" \
      -e "s/YYYY-MM-DD HH:MM/$TODAY $NOW/g" \
      "$UTILS_DIR/workflow_state_template.md" > "$WS"
  echo "✓ created $WS"
else
  echo "• $WS already exists — skipping"
fi

# 3. time_log.md (only if missing)
TLOG="$PROJ_DIR/time_log.md"
if [ ! -f "$TLOG" ]; then
  sed "s/<project name>/$PROJ_NAME/g" "$UTILS_DIR/time_log_template.md" > "$TLOG"
  echo "✓ created $TLOG"
fi

# 4. Append iteration row to time_log.md
TODAY=$(date +%Y-%m-%d)
NOW=$(date +%H:%M)
# Find the "## Итерации" table and append. Simple: append a marker line that user can fill.
echo "" >> "$TLOG"
echo "<!-- ${ITER} started ${TODAY} ${NOW} — fill row in table above -->" >> "$TLOG"
echo "✓ logged ${ITER} start in $TLOG"

# 5. Reminder
cat <<EOF

📋 Next steps for ${PROJ_NAME} ${ITER}:
   1. Open $WS and start with Этап A (voice markers → storyboard → hook → photo policy)
   2. Use _utils/text_script_template.py as starter for ${ITER}_build/text_${ITER}.py
   3. Use check_text_width.py BEFORE rendering — saves ffmpeg roundtrips
   4. On approve: update time_log.md row + fill lessons_learned.md if final
EOF
