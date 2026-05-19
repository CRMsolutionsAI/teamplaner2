"""Build text overlay filter for v6."""

FONT_BOLD = "/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Bold.ttf"
FONT_BLACK = "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Black.ttf"
FONT_CAVEAT = "/home/user/teamplaner2/video-edits/fonts/Caveat.ttf"

W, H = 1080, 1920
WHITE = "white"
ORANGE = "0xFF5722"
BLACK = "black"

# Each text: (t_start, t_end, text, font, size, color, x, y, options)
# Cyrillic via UTF-8 escapes in single quotes
texts = [
    # M1 (0-6.36) Hook
    (0.4, 2.0,   "ОБРАТИ",         FONT_BOLD,  120, WHITE,  "80", "180", ""),
    (1.2, 3.0,   "ВНИМАНИЕ",       FONT_BOLD,  90,  ORANGE, "180", "320", ""),
    (4.0, 6.36,  "СЕЙФ",           FONT_BLACK, 200, WHITE,  "(w-tw)/2", "1480", "box=1:boxcolor=0xFF5722@0.95:boxborderw=30"),
    (4.5, 6.36,  "не сувенир",     FONT_CAVEAT, 70, ORANGE, "(w-tw)/2", "1720", ""),

    # M2 (6.36-18.18) Night market
    (6.6, 9.0,   "НОЧНОЙ",         FONT_BOLD,  130, WHITE,  "60", "200", ""),
    (7.2, 9.0,   "РЫНОК",          FONT_BOLD,  130, ORANGE, "340", "350", ""),
    (9.2, 11.5,  "ТЫ",             FONT_BOLD,  120, WHITE,  "100", "200", ""),
    (9.6, 11.5,  "СОЗДАЁШЬ",       FONT_BOLD,  110, ORANGE, "260", "340", ""),
    (11.7, 14.0, "СВОЮ",           FONT_BOLD,  100, WHITE,  "80", "220", ""),
    (12.1, 14.0, "СИСТЕМУ",        FONT_BOLD,  120, ORANGE, "260", "350", ""),
    (14.2, 16.5, "ЗНАЧКИ",         FONT_BOLD,  90,  WHITE,  "60", "240", ""),
    (14.6, 16.5, "ЛЕНТА",          FONT_BOLD,  90,  WHITE,  "280", "360", ""),
    (15.0, 16.5, "ЦВЕТ",           FONT_BOLD,  90,  ORANGE, "500", "480", ""),
    (16.7, 18.18, "+ВСЁ ТВОЁ",     FONT_BOLD,  100, ORANGE, "(w-tw)/2", "1500", "box=1:boxcolor=black@0.7:boxborderw=20"),

    # M3 (18.18-31.82) Process
    (18.4, 21.0, "МАСТЕР",         FONT_BLACK, 140, WHITE,  "(w-tw)/2", "180", ""),
    (21.2, 23.5, "ПАРУ МИНУТ",     FONT_BOLD,  90,  WHITE,  "(w-tw)/2", "200", ""),
    (21.6, 23.5, "+МАГИЯ",         FONT_CAVEAT, 130, ORANGE, "(w-tw)/2", "340", ""),
    (23.7, 26.0, "ТАКТИЛЬНО",      FONT_BOLD,  110, WHITE,  "(w-tw)/2", "200", ""),
    (24.1, 26.0, "НАДЁЖНО",        FONT_BOLD,  110, ORANGE, "(w-tw)/2", "340", ""),
    (26.2, 28.5, "СОЕДИНЯЕТ",      FONT_BOLD,  100, WHITE,  "60", "220", ""),
    (26.6, 28.5, "ВСЕ ДЕТАЛИ",     FONT_BOLD,  100, ORANGE, "180", "360", ""),
    (28.7, 31.82, "NATALIA",       FONT_BLACK, 90, ORANGE,  "(w-tw)/2", "1480", "box=1:boxcolor=white@0.95:boxborderw=25"),
    (29.2, 31.82, "имя на обложке", FONT_CAVEAT, 60, WHITE, "(w-tw)/2", "1680", ""),

    # M4 (31.82-43.64) Value/120 — NO her passport footage
    (32.0, 34.0, "ЦЕНА",           FONT_BLACK, 130, WHITE,  "(w-tw)/2", "200", ""),
    (34.2, 41.0, "120",            FONT_BLACK, 380, WHITE,  "(w-tw)/2", "550", "box=1:boxcolor=0xFF5722:boxborderw=40"),
    (35.0, 41.0, "БАТ",            FONT_BLACK, 110, ORANGE, "(w-tw)/2", "1020", ""),
    (37.0, 41.0, "= 161 ГРН",      FONT_CAVEAT, 110, WHITE, "(w-tw)/2", "1180", ""),
    (38.5, 41.0, "за уникальность", FONT_CAVEAT, 70, ORANGE, "(w-tw)/2", "1320", ""),
    (41.2, 43.64, "ЭМОЦИЯ",        FONT_BLACK, 130, WHITE,  "(w-tw)/2", "220", ""),
    (41.6, 43.64, "не чехол",      FONT_CAVEAT, 90, ORANGE, "(w-tw)/2", "390", ""),

    # M5 (43.64-48.6) Finale
    (43.84, 48.6, "ВАШ",           FONT_BLACK, 180, WHITE,  "(w-tw)/2", "180", ""),
    (44.0, 48.6,  "ПАСПОРТ",       FONT_BLACK, 200, WHITE,  "(w-tw)/2", "380", ""),
    (44.5, 48.6,  "— ваша история", FONT_CAVEAT, 120, ORANGE, "(w-tw)/2", "1600", ""),
    (46.5, 48.6,  "а во что одеты ваши документы?", FONT_CAVEAT, 60, WHITE, "(w-tw)/2", "1780", ""),
]

def escape_text(t):
    """Escape special chars for ffmpeg drawtext."""
    return t.replace('\\', '\\\\').replace("'", "\\'").replace(':', '\\:').replace(',', '\\,')

filter_parts = []
for i, (t0, t1, txt, font, size, color, x, y, opts) in enumerate(texts):
    esc = escape_text(txt)
    options = f"text='{esc}':fontfile={font}:fontsize={size}:fontcolor={color}:x={x}:y={y}:enable='between(t,{t0},{t1})'"
    if opts:
        options += ":" + opts
    filter_parts.append(f"drawtext={options}")

filter_chain = ",".join(filter_parts) + ",eq=contrast=1.10:saturation=1.06:gamma_r=0.97:gamma_b=1.03"
with open('/tmp/v6_text_filter.txt', 'w') as f:
    f.write(filter_chain)
print(f"Filter has {len(texts)} text events, length: {len(filter_chain)} chars")
