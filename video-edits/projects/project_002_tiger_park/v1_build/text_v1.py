"""project_002 tiger_park v1 — text overlays with phrase-synced timing."""

FONT_BOLD = "/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Bold.ttf"
FONT_BLACK = "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Black.ttf"
FONT_CAVEAT = "/home/user/teamplaner2/video-edits/fonts/Caveat.ttf"

WHITE = "white"
ORANGE = "0xFF5722"

# (t_start, t_end, text, font, size, color, x, y, options)
texts = [
    # M1 Hook — ПРОВЕРКА ПРОШИВКИ
    (3.5, 6.9, "ПРОВЕРКА",       FONT_BLACK, 160, WHITE,  "(w-tw)/2", "200", ""),
    (4.2, 6.9, "ПРОШИВКИ",       FONT_BLACK, 140, ORANGE, "(w-tw)/2", "380", "box=1:boxcolor=black@0.7:boxborderw=20"),

    # M2 System — 15 МИНУТ
    (13.0, 18.9, "15",           FONT_BLACK, 380, WHITE,  "(w-tw)/2", "550", "box=1:boxcolor=0xFF5722:boxborderw=40"),
    (13.5, 18.9, "МИНУТ",        FONT_BOLD,  130, ORANGE, "(w-tw)/2", "1020", ""),
    (14.0, 18.9, "истины",       FONT_CAVEAT, 80, WHITE,  "(w-tw)/2", "1180", ""),

    # M3 Energy — 5 words tier reveal
    (19.5, 24.9, "СИЛА",         FONT_BLACK, 110, WHITE,  "(w-tw)/2", "200", ""),
    (20.5, 24.9, "МОЩЬ",         FONT_BLACK, 110, ORANGE, "(w-tw)/2", "360", ""),
    (21.5, 24.9, "ВЛАСТЬ",       FONT_BLACK, 110, WHITE,  "(w-tw)/2", "520", ""),
    (22.5, 24.9, "ОПАСНОСТЬ",    FONT_BLACK, 110, ORANGE, "(w-tw)/2", "680", ""),
    (23.5, 24.9, "ПРЕДЕЛЬНОЕ УВАЖЕНИЕ", FONT_CAVEAT, 80, WHITE, "(w-tw)/2", "1500", ""),
    # Big title 5 ЭНЕРГИЙ at scene end
    (30.0, 33.9, "5",            FONT_BLACK, 300, WHITE,  "(w-tw)/2", "600", "box=1:boxcolor=0xFF5722:boxborderw=40"),
    (30.5, 33.9, "ЭНЕРГИЙ",      FONT_BLACK, 130, ORANGE, "(w-tw)/2", "950", ""),

    # M4 Lesson — НЕ ЩЕКОЧИ СИЛУ
    (39.0, 44.9, "НЕ ЩЕКОЧИ",    FONT_BLACK, 140, WHITE,  "(w-tw)/2", "1500", ""),
    (39.5, 44.9, "СИЛУ",         FONT_BLACK, 200, ORANGE, "(w-tw)/2", "1680", "box=1:boxcolor=black@0.7:boxborderw=20"),
    (45.0, 48.9, "гладь",        FONT_CAVEAT, 100, WHITE, "(w-tw)/2", "200", ""),
    (45.5, 48.9, "СИЛЬНЕЕ",      FONT_BLACK, 150, ORANGE, "(w-tw)/2", "330", ""),

    # M5 Climax — СИМВОЛ ДОВЕРИЯ
    (54.0, 57.9, "СИМВОЛ",       FONT_BLACK, 130, WHITE,  "(w-tw)/2", "200", ""),
    (54.5, 57.9, "ДОВЕРИЯ",      FONT_BLACK, 170, ORANGE, "(w-tw)/2", "380", "box=1:boxcolor=black@0.7:boxborderw=20"),

    # M6 Insight (58-68) — final CTA on black
    (63.0, 68.0, "МИР",          FONT_BLACK, 220, WHITE,  "(w-tw)/2", "500", ""),
    (63.4, 68.0, "У ТВОИХ",      FONT_BOLD,  130, WHITE,  "(w-tw)/2", "780", ""),
    (63.8, 68.0, "НОГ",          FONT_BLACK, 280, WHITE,  "(w-tw)/2", "980", "box=1:boxcolor=0xFF5722:boxborderw=40"),
    (65.5, 68.0, "если уважаешь чужие законы", FONT_CAVEAT, 70, ORANGE, "(w-tw)/2", "1450", ""),
]


def escape_text(t):
    return t.replace('\\', '\\\\').replace("'", "\\'").replace(':', '\\:').replace(',', '\\,')


parts = []
for (t0, t1, txt, font, size, color, x, y, opts) in texts:
    esc = escape_text(txt)
    s = f"drawtext=text='{esc}':fontfile={font}:fontsize={size}:fontcolor={color}:x={x}:y={y}:enable='between(t,{t0},{t1})'"
    if opts:
        s += ":" + opts
    parts.append(s)

chain = ",".join(parts) + ",eq=contrast=1.08:saturation=1.05"
with open('/tmp/v1_tiger_text.txt', 'w') as f:
    f.write(chain)
print(f"v1 tiger: {len(texts)} text events, filter len {len(chain)} chars")
