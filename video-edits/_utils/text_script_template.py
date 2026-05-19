"""Template for text_vN.py scripts. Copy + adapt per project.

Key feature: integrated `check_text_width` to catch sidebar overflow
BEFORE rendering (saves a 3-minute ffmpeg roundtrip).

Usage in project:
    1. Copy this file to projects/<X>/vN_build/text_v1.py
    2. Replace `texts` list with project-specific events
    3. Replace `LAYOUT_AT_TIME` lookup with project's shot timeline
    4. Run: python3 text_v1.py
       → if any text overflows, you'll see WARN before render
"""
import sys
from pathlib import Path

# Make _utils importable from build directory
_UTILS = Path(__file__).resolve().parents[2] / "_utils"
sys.path.insert(0, str(_UTILS.parent))
from _utils.check_text_width import check_drawtext
from _utils.align_transcript import load_aligned, time_of_phrase

FONT_BOLD   = "/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Bold.ttf"
FONT_BLACK  = "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Black.ttf"
FONT_CAVEAT = "/home/user/teamplaner2/video-edits/fonts/Caveat.ttf"

WHITE  = "white"
ORANGE = "0xFF5722"


# ---------------------------------------------------------------------------
# 1. Shot layout timeline — copy from render_vN.py shots[] in synced format
#    For each (t_start, t_end) range, what layout is the canvas?
# ---------------------------------------------------------------------------
SHOT_LAYOUTS = [
    # (t_start, t_end, layout_name)
    (0.0,   3.0,   "CENTER"),
    (3.0,   6.0,   "BLACK"),
    # ... fill in for each shot
]


def layout_at(t: float) -> str:
    for t0, t1, layout in SHOT_LAYOUTS:
        if t0 <= t < t1:
            return layout
    return "BLACK"


# ---------------------------------------------------------------------------
# 2. Load aligned transcript — point to voice + transcript paths.
#    Use time_of_phrase("keyword") to anchor titles to exact spoken words.
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
VOICE_WAV = PROJECT_ROOT / "v1_build" / "voice.wav"  # adjust if non-v1
TRANSCRIPT = PROJECT_ROOT / "sources" / "transcript.txt"

phrases = []
if VOICE_WAV.exists() and TRANSCRIPT.exists():
    phrases = load_aligned(VOICE_WAV, TRANSCRIPT)
    print(f"# Loaded {len(phrases)} aligned phrases", file=sys.stderr)


def at(keyword: str, lead: float = 0.15) -> float:
    """Find time when voice says `keyword`, minus lead-in. Falls back to 0 if not found."""
    t = time_of_phrase(phrases, keyword)
    if t is None:
        print(f"  ⚠  '{keyword}' not found in transcript", file=sys.stderr)
        return 0.0
    return max(0.0, t - lead)


# ---------------------------------------------------------------------------
# 3. Text events — (t0, t1, text, font, size, color, x, y, opts)
#    Use at("keyword") to lock title to actual voice timing.
# ---------------------------------------------------------------------------
texts = [
    # Example: title locked to actual spoken word, no manual guessing
    # (at("встреча с тигром"), at("встреча с тигром") + 3, "ТИГРОМ", FONT_BLACK, 170, ORANGE, ...),
    (0.5, 2.9, "встреча с",  FONT_CAVEAT, 90,  WHITE,  "(w-tw)/2", "180", ""),
    (1.0, 2.9, "ТИГРОМ",     FONT_BLACK,  170, ORANGE, "(w-tw)/2", "260",
        "box=1:boxcolor=black@0.7:boxborderw=15"),
]


# ---------------------------------------------------------------------------
# 3. Pre-render width check — runs BEFORE filter chain is written
# ---------------------------------------------------------------------------
def escape_text(t):
    return t.replace('\\', '\\\\').replace("'", "\\'").replace(':', '\\:').replace(',', '\\,')


print("=== check_text_width: pre-render validation ===", file=sys.stderr)
warns = 0
for evt in texts:
    t0, t1, txt, font, size, color, x, y, opts = evt
    layout = layout_at(t0)
    if not check_drawtext(txt, font, size, x, y, layout):
        warns += 1
if warns:
    print(f"⚠  {warns} text events will overflow. Fix BEFORE rendering "
          f"(move TOP/BOTTOM full-width or shrink font).", file=sys.stderr)
else:
    print("✓ all text events fit their layout slots", file=sys.stderr)


# ---------------------------------------------------------------------------
# 4. Build ffmpeg filter chain
# ---------------------------------------------------------------------------
FADE = 0.25  # 250ms fade-in per CLAUDE.md premium-paradigm

parts = []
for (t0, t1, txt, font, size, color, x, y, opts) in texts:
    esc = escape_text(txt)
    alpha = f"if(lt(t,{t0+FADE}),(t-{t0})/{FADE},1)"
    s = (f"drawtext=text='{esc}':fontfile={font}:fontsize={size}:fontcolor={color}:"
         f"x={x}:y={y}:enable='between(t,{t0},{t1})':alpha='{alpha}'")
    if opts:
        s += ":" + opts
    parts.append(s)

# Teal-orange cinematic grade per CLAUDE.md
chain = ",".join(parts) + (
    ",eq=contrast=1.10:saturation=1.10"
    ",colorbalance=rs=-0.04:bs=0.05:rm=0.03:bm=-0.04:rh=0.05:bh=-0.05"
)

# Adjust output path per project
out_path = '/tmp/text_filter.txt'
with open(out_path, 'w') as f:
    f.write(chain)
print(f"\nWrote filter chain → {out_path}", file=sys.stderr)
print(f"  {len(texts)} text events, {len(chain)} chars", file=sys.stderr)
