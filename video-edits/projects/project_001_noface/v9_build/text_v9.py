"""v7 text overlays — realigned to voice phrase starts (lead -0.15s)."""

FONT_BOLD = "/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Bold.ttf"
FONT_BLACK = "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Black.ttf"
FONT_CAVEAT = "/home/user/teamplaner2/video-edits/fonts/Caveat.ttf"

WHITE = "white"
ORANGE = "0xFF5722"

# Voice phrase starts detected via silencedetect:
# P1 0.95 | P2 3.21 | P3 9.08 | P4 12.10 | P5 13.49 | P6 15.12 | P7 17.59 |
# P8 18.94 | P9 20.77 | P10 25.57 | P11 33.01 ("120 БАТ") | P12 36.03 |
# P13 36.64 | P14 40.88 | P15 43.14 | P16 46.63

texts = [
    # M1 Hook
    (0.6, 2.7,   "ОБРАТИ",         FONT_BOLD,  120, WHITE,  "80", "180", ""),
    (1.3, 3.0,   "ВНИМАНИЕ",       FONT_BOLD,  90,  ORANGE, "180", "320", ""),
    (3.0, 6.36,  "СЕЙФ",           FONT_BLACK, 200, WHITE,  "(w-tw)/2", "1480", "box=1:boxcolor=0xFF5722@0.95:boxborderw=30"),
    (3.6, 6.36,  "не сувенир",     FONT_CAVEAT, 70, ORANGE, "(w-tw)/2", "1720", ""),

    # M2 Night market — phrase-synced
    (8.90, 11.0, "НОЧНОЙ",         FONT_BOLD,  130, WHITE,  "60", "200", ""),
    (9.40, 11.0, "РЫНОК",          FONT_BOLD,  130, ORANGE, "340", "350", ""),
    (11.90, 13.30, "ТЫ",           FONT_BOLD,  120, WHITE,  "100", "200", ""),
    (12.20, 13.30, "СОЗДАЁШЬ",     FONT_BOLD,  110, ORANGE, "260", "340", ""),
    (13.29, 14.83, "СВОЮ",         FONT_BOLD,  100, WHITE,  "80", "220", ""),
    (13.60, 14.83, "СИСТЕМУ",      FONT_BOLD,  120, ORANGE, "260", "350", ""),
    (14.95, 17.30, "ЗНАЧКИ",       FONT_BOLD,  90,  WHITE,  "60", "240", ""),
    (15.40, 17.30, "ЛЕНТА",        FONT_BOLD,  90,  WHITE,  "280", "360", ""),
    (16.00, 17.30, "ЦВЕТ",         FONT_BOLD,  90,  ORANGE, "500", "480", ""),
    (17.40, 18.94, "+ВСЁ ТВОЁ",    FONT_BOLD,  100, ORANGE, "(w-tw)/2", "1500", "box=1:boxcolor=black@0.7:boxborderw=20"),

    # M3 Process
    (18.78, 20.77, "МАСТЕР",       FONT_BLACK, 140, WHITE,  "(w-tw)/2", "180", ""),
    (20.62, 22.5,  "ПАРУ МИНУТ",   FONT_BOLD,  90,  WHITE,  "(w-tw)/2", "200", ""),
    (20.95, 22.5,  "+МАГИЯ",       FONT_CAVEAT, 130, ORANGE, "(w-tw)/2", "340", ""),
    # ТАКТИЛЬНО / НАДЁЖНО — spread further vertically + each pinned to its own shot
    (22.5, 24.0,   "ТАКТИЛЬНО",    FONT_BOLD,  100, WHITE,  "(w-tw)/2", "200", ""),
    (24.0, 25.42,  "НАДЁЖНО",      FONT_BOLD,  100, ORANGE, "(w-tw)/2", "440", ""),
    (25.42, 27.5,  "СОЕДИНЯЕТ",    FONT_BOLD,  100, WHITE,  "60", "220", ""),
    (25.80, 27.5,  "ВСЕ ДЕТАЛИ",   FONT_BOLD,  100, ORANGE, "180", "360", ""),
    # NATALIA moved later — voice says the name around 30s, not 28.5
    (29.80, 32.7,  "NATALIA",      FONT_BLACK, 90, ORANGE,  "(w-tw)/2", "1480", "box=1:boxcolor=white@0.95:boxborderw=25"),
    (30.15, 32.7,  "имя на обложке", FONT_CAVEAT, 60, WHITE, "(w-tw)/2", "1680", ""),

    # M4 Value/120 — voice says "120 БАТ" at 33.05
    (32.70, 33.40, "ЦЕНА",         FONT_BLACK, 130, WHITE,  "(w-tw)/2", "200", ""),
    (32.90, 36.0,  "120",          FONT_BLACK, 380, WHITE,  "(w-tw)/2", "550", "box=1:boxcolor=0xFF5722:boxborderw=40"),
    (33.30, 36.0,  "БАТ",          FONT_BLACK, 110, ORANGE, "(w-tw)/2", "1020", ""),
    (35.90, 40.5,  "= 161 ГРН",    FONT_CAVEAT, 110, WHITE, "(w-tw)/2", "1180", ""),
    (36.90, 40.5,  "за уникальность", FONT_CAVEAT, 70, ORANGE, "(w-tw)/2", "1320", ""),  # voice P 37.05
    (40.70, 42.83, "ЭМОЦИЯ",       FONT_BLACK, 130, WHITE,  "(w-tw)/2", "220", ""),
    (41.10, 42.83, "не чехол",     FONT_CAVEAT, 90, ORANGE, "(w-tw)/2", "390", ""),

    # M5 Finale
    (42.94, 46.27, "ВАШ",          FONT_BLACK, 180, WHITE,  "(w-tw)/2", "180", ""),
    (43.20, 46.27, "ПАСПОРТ",      FONT_BLACK, 200, WHITE,  "(w-tw)/2", "380", ""),
    (44.0, 46.27,  "— ваша история", FONT_CAVEAT, 120, ORANGE, "(w-tw)/2", "1600", ""),
    (46.43, 48.6,  "а во что одеты ваши документы?", FONT_CAVEAT, 60, WHITE, "(w-tw)/2", "1780", ""),
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

chain = ",".join(parts) + ",eq=contrast=1.10:saturation=1.06:gamma_r=0.97:gamma_b=1.03"
with open('/tmp/v7_text_filter.txt', 'w') as f:
    f.write(chain)
print(f"v7: {len(texts)} text events, filter length {len(chain)} chars")
