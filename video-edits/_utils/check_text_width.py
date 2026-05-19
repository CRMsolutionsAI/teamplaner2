"""Text-width sanity check for drawtext events.

Usage:
    from video_edits._utils.check_text_width import check_drawtext

    check_drawtext(text, font_path, fontsize, x_pos, y_pos, layout="LEFT")

Raises a warning (not error) if text would overflow its slot.
"""
import os
import sys

try:
    from PIL import ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


# Canvas: 1080x1920
CANVAS_W = 1080
CANVAS_H = 1920

# Layout slots (where text CAN sit safely)
LAYOUT_TEXT_SLOTS = {
    # layout → list of (x_min, x_max, y_min, y_max) zones
    "CENTER": [
        (0,    1080, 0,    300),   # TOP full width
        (0,    1080, 1620, 1920),  # BOTTOM full width
    ],
    "LEFT":   [  # video at x=40-640 → sidebar RIGHT
        (720,  1040, 460,  1460),  # sidebar narrow
        (0,    1080, 0,    420),   # TOP full
        (0,    1080, 1480, 1920),  # BOTTOM full
    ],
    "RIGHT":  [  # video at x=440-1040 → sidebar LEFT
        (40,   400,  460,  1460),  # sidebar narrow
        (0,    1080, 0,    420),   # TOP full
        (0,    1080, 1480, 1920),  # BOTTOM full
    ],
    "FULL":   [
        (0,    1080, 0,    200),   # TOP narrow (over content)
        (0,    1080, 1700, 1920),  # BOTTOM narrow (over content)
    ],
    "BLACK":  [
        (0,    1080, 0,    1920),  # whole canvas
    ],
}


def measure_text_width(text: str, font_path: str, fontsize: int) -> int:
    """Return rendered pixel width of text in given font."""
    if HAS_PIL and os.path.exists(font_path):
        try:
            font = ImageFont.truetype(font_path, fontsize)
            bbox = font.getbbox(text)
            return bbox[2] - bbox[0]
        except Exception:
            pass
    # Fallback heuristic per font family (approximate)
    if "Caveat" in font_path:
        factor = 0.40
    elif "Bold" in font_path and "Condensed" in font_path:
        factor = 0.46
    elif "Black" in font_path:
        factor = 0.62
    else:
        factor = 0.55
    return int(len(text) * fontsize * factor)


def x_resolves_to(x_expr, text_width: int) -> int:
    """Resolve common ffmpeg x expressions to approximate pixel start."""
    if x_expr == "(w-tw)/2":
        return (CANVAS_W - text_width) // 2
    if isinstance(x_expr, (int, float)):
        return int(x_expr)
    try:
        return int(x_expr)
    except (ValueError, TypeError):
        return 0


def check_drawtext(text: str, font_path: str, fontsize: int,
                   x_expr, y_pos, layout: str = "BLACK") -> bool:
    """Check if text fits its layout slot. Returns True if OK, prints WARN if not."""
    width = measure_text_width(text, font_path, fontsize)
    x_start = x_resolves_to(x_expr, width)
    x_end = x_start + width
    y_pos = int(y_pos)

    slots = LAYOUT_TEXT_SLOTS.get(layout, LAYOUT_TEXT_SLOTS["BLACK"])
    for x_min, x_max, y_min, y_max in slots:
        if x_start >= x_min and x_end <= x_max and y_min <= y_pos <= y_max:
            return True

    print(f"  ⚠  WIDTH WARN: '{text}' (font_size {fontsize}) → "
          f"width ~{width}px, x={x_start}-{x_end}, y={y_pos}, layout={layout} "
          f"— does NOT fit any safe slot", file=sys.stderr)
    return False


def check_text_list(texts, layout_resolver=None):
    """Batch-check a text_v*.py events list.

    Args:
        texts: list of tuples (t0, t1, txt, font, size, color, x, y, opts)
        layout_resolver: callable (t0) -> layout name. If None, assume BLACK everywhere.
    """
    warns = 0
    for evt in texts:
        t0, t1, txt, font, size, color, x, y, opts = evt
        layout = layout_resolver(t0) if layout_resolver else "BLACK"
        if not check_drawtext(txt, font, size, x, y, layout):
            warns += 1
    print(f"check_text_width: {warns} warning(s) out of {len(texts)} events", file=sys.stderr)
    return warns


if __name__ == "__main__":
    # Self-test
    FB = "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Black.ttf"
    check_drawtext("ОДИН НА ОДИН", FB, 140, "720", "880", "LEFT")  # should WARN
    check_drawtext("ОДИН", FB, 130, "40", "780", "RIGHT")          # OK
    check_drawtext("ВО ЧТО ОДЕТЫ", FB, 110, "(w-tw)/2", "200", "LEFT")  # OK (top full)
