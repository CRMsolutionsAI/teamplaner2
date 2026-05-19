"""project_002 tiger v3 — text positions FIXED:
sidebar text NEVER >5 chars, anything wider goes TOP (y<420) or BOTTOM (y>1480) full canvas.
Titles re-aligned to actual voice timing in M6/M7.
"""

FONT_BOLD = "/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Bold.ttf"
FONT_BLACK = "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Black.ttf"
FONT_CAVEAT = "/home/user/teamplaner2/video-edits/fonts/Caveat.ttf"

WHITE = "white"
ORANGE = "0xFF5722"

# Window layouts (recap):
# CENTER y=360-1560 → text TOP y<300 or BOTTOM y>1620
# LEFT x=40-640 → text on RIGHT x>720 max 320px wide, OR TOP/BOTTOM full width
# RIGHT x=440-1040 → text on LEFT x<400 max 380px wide, OR TOP/BOTTOM full width
# BLACK → full canvas

texts = [
    # 0-3 CENTER: top text
    (0.5, 2.9, "встреча с",          FONT_CAVEAT, 90,  WHITE,  "(w-tw)/2", "180", ""),
    (1.0, 2.9, "ТИГРОМ",             FONT_BLACK,  170, ORANGE, "(w-tw)/2", "260", "box=1:boxcolor=black@0.7:boxborderw=15"),

    # 3-6 BLACK: hook with promise
    (3.0, 5.9, "ПРОВЕРКА",           FONT_BLACK, 180, WHITE,  "(w-tw)/2", "600", ""),
    (3.5, 5.9, "ПРОШИВКИ",           FONT_BLACK, 160, ORANGE, "(w-tw)/2", "830", "box=1:boxcolor=black@0.7:boxborderw=20"),
    (4.5, 5.9, "одно правило, которое работает везде", FONT_CAVEAT, 60, WHITE, "(w-tw)/2", "1100", ""),

    # 6-9 RIGHT (window x=440-1040): text LEFT side, short words only
    (6.3, 8.9, "TIGER",              FONT_BLACK, 130, WHITE,  "40", "720", ""),
    (6.8, 8.9, "WORLD",              FONT_BLACK, 130, ORANGE, "40", "880", ""),

    # 9-12 photo CENTER: bottom text (full width, longer phrase OK)
    (9.3, 11.9, "1,5 часа от Бангкока", FONT_CAVEAT, 80, WHITE,  "(w-tw)/2", "1680", ""),

    # 12-16 BLACK: 15 МИНУТ
    (12.0, 15.9, "15",               FONT_BLACK, 400, WHITE,  "(w-tw)/2", "500", "box=1:boxcolor=0xFF5722:boxborderw=40"),
    (12.5, 15.9, "МИНУТ",            FONT_BOLD,  130, ORANGE, "(w-tw)/2", "1000", ""),
    (13.0, 15.9, "истины",           FONT_CAVEAT, 80, WHITE,  "(w-tw)/2", "1160", ""),

    # 16-19 LEFT (window x=40-640): text TOP full width (was clipping problem)
    (16.3, 18.9, "ОДИН НА ОДИН",     FONT_BLACK, 110, WHITE,  "(w-tw)/2", "200", ""),
    (16.8, 18.9, "с хищником",       FONT_CAVEAT, 70, ORANGE, "(w-tw)/2", "340", ""),

    # 19-22 photo CENTER: bottom
    (19.3, 21.9, "10-15 минут",      FONT_CAVEAT, 80, WHITE,  "(w-tw)/2", "1680", ""),

    # 22-26 CENTER: top text
    (22.3, 25.9, "ВЫБОР",            FONT_BLACK, 140, WHITE,  "(w-tw)/2", "200", ""),

    # 26-30 photo: bottom text
    (26.3, 29.9, "котята или хищник", FONT_CAVEAT, 75, ORANGE, "(w-tw)/2", "1680", ""),

    # 30-34 RIGHT (window right): text LEFT, short only
    (30.3, 33.9, "ПРАВИЛА",          FONT_BLACK, 110, WHITE,  "40", "780", ""),
    (30.8, 33.9, "ДОМА",             FONT_BLACK, 140, ORANGE, "40", "920", "box=1:boxcolor=black@0.7:boxborderw=15"),

    # 34-38 LEFT (window left): text TOP/BOTTOM full width (was clipping "К ЭМОЦИЯМ")
    (34.3, 37.9, "от процесса",      FONT_CAVEAT, 80, WHITE, "(w-tw)/2", "200", ""),
    (34.8, 37.9, "К ЭМОЦИЯМ",        FONT_BLACK, 110, ORANGE, "(w-tw)/2", "340", "box=1:boxcolor=black@0.5:boxborderw=10"),

    # 38-44 CENTER: top + bottom
    (38.3, 43.9, "пять",             FONT_CAVEAT, 80, WHITE, "(w-tw)/2", "200", ""),
    (38.8, 43.9, "ЭНЕРГИЙ ПЛАНЕТЫ", FONT_BLACK, 80, ORANGE, "(w-tw)/2", "320", ""),

    # 44-48 BLACK: tier reveal
    (44.5, 47.9, "СИЛА",             FONT_BLACK, 130, WHITE,  "(w-tw)/2", "320", ""),
    (45.0, 47.9, "МОЩЬ",             FONT_BLACK, 130, ORANGE, "(w-tw)/2", "510", ""),
    (45.5, 47.9, "ВЛАСТЬ",           FONT_BLACK, 130, WHITE,  "(w-tw)/2", "700", ""),
    (46.0, 47.9, "ОПАСНОСТЬ",        FONT_BLACK, 130, ORANGE, "(w-tw)/2", "890", ""),
    (46.5, 47.9, "ЖЕЛАНИЕ",          FONT_BLACK, 130, WHITE,  "(w-tw)/2", "1080", ""),

    # 48-52 CENTER: top+bottom
    (48.3, 51.9, "не страх",         FONT_CAVEAT, 90, WHITE, "(w-tw)/2", "200", ""),
    (48.8, 51.9, "УВАЖЕНИЕ",         FONT_BLACK, 130, ORANGE, "(w-tw)/2", "1640", ""),

    # 52-58 BLACK: 5 ЭНЕРГИЙ card
    (52.0, 57.9, "5",                FONT_BLACK, 350, WHITE,  "(w-tw)/2", "550", "box=1:boxcolor=0xFF5722:boxborderw=40"),
    (52.5, 57.9, "ЭНЕРГИЙ",          FONT_BLACK, 140, ORANGE, "(w-tw)/2", "980", ""),
    (53.5, 57.9, "одного существа",  FONT_CAVEAT, 70, WHITE, "(w-tw)/2", "1140", ""),

    # 58-60 CENTER: top
    (58.2, 59.9, "ПРЕДЕЛЬНОЕ",       FONT_BOLD, 100, WHITE,  "(w-tw)/2", "200", ""),

    # 60-66 RIGHT (window right): text LEFT short
    (60.3, 65.9, "ГЛАВНЫЙ",          FONT_BLACK, 100, WHITE,  "40", "780", ""),
    (60.8, 65.9, "УРОК",             FONT_BLACK, 200, ORANGE, "40", "920", "box=1:boxcolor=black@0.7:boxborderw=15"),

    # 66-72 BLACK: BIG RULE
    (66.0, 71.9, "НЕ ЩЕКОЧИ",        FONT_BLACK, 150, WHITE,  "(w-tw)/2", "550", ""),
    (66.5, 71.9, "СИЛУ",             FONT_BLACK, 250, WHITE,  "(w-tw)/2", "780", "box=1:boxcolor=0xFF5722:boxborderw=40"),
    (68.0, 71.9, "правило работает:", FONT_CAVEAT, 60, WHITE, "(w-tw)/2", "1160", ""),
    (69.0, 71.9, "переговоры • команда • отношения", FONT_CAVEAT, 55, ORANGE, "(w-tw)/2", "1240", ""),

    # 72-78 LEFT (window left): text TOP/BOTTOM full width
    (72.3, 77.9, "гладь",            FONT_CAVEAT, 100, WHITE, "(w-tw)/2", "200", ""),
    (72.8, 77.9, "СИЛЬНЕЕ",          FONT_BLACK, 150, ORANGE, "(w-tw)/2", "340", "box=1:boxcolor=black@0.5:boxborderw=10"),
    (74.0, 77.9, "сила требует УВЕРЕННОСТИ", FONT_BOLD, 60, WHITE, "(w-tw)/2", "1680", ""),

    # 78-83 CENTER: top
    (78.3, 82.9, "признаёшь",        FONT_CAVEAT, 80, WHITE, "(w-tw)/2", "200", ""),
    (78.8, 82.9, "ВЕС",              FONT_BLACK, 180, ORANGE, "(w-tw)/2", "1620", ""),

    # 83-87 PHOTO belly: text bottom — voice says "открывает живот" here
    (83.3, 86.9, "ОТКРЫВАЕТ",        FONT_BLACK, 130, WHITE,  "(w-tw)/2", "1640", "box=1:boxcolor=black@0.5:boxborderw=10"),
    (84.0, 86.9, "ЖИВОТ",            FONT_BLACK, 180, ORANGE, "(w-tw)/2", "1780", "box=1:boxcolor=black@0.5:boxborderw=15"),

    # 87-92 BLACK: СИМВОЛ ДОВЕРИЯ card — voice resolves here
    (87.0, 91.9, "СИМВОЛ",           FONT_BLACK, 150, WHITE,  "(w-tw)/2", "600", ""),
    (87.5, 91.9, "ДОВЕРИЯ",          FONT_BLACK, 190, ORANGE, "(w-tw)/2", "830", "box=1:boxcolor=black@0.7:boxborderw=20"),
    (89.0, 91.9, "которое нельзя купить", FONT_CAVEAT, 65, WHITE, "(w-tw)/2", "1170", ""),

    # 92-95 PHOTO lying: top text
    (92.3, 94.9, "земля-инь",        FONT_CAVEAT, 80, WHITE, "(w-tw)/2", "200", ""),
    (92.8, 94.9, "и ПЛАМЯ",          FONT_BLACK, 110, ORANGE, "(w-tw)/2", "320", ""),

    # 95-101 CENTER: top+bottom
    (95.3, 100.9, "если уважаешь",   FONT_CAVEAT, 80, WHITE, "(w-tw)/2", "200", ""),
    (95.8, 100.9, "ЧУЖИЕ ЗАКОНЫ",    FONT_BLACK, 100, ORANGE, "(w-tw)/2", "1640", ""),

    # 101-108 BLACK: final CTA
    (101.0, 108.2, "МИР",            FONT_BLACK, 240, WHITE,  "(w-tw)/2", "500", ""),
    (101.4, 108.2, "У ТВОИХ",        FONT_BOLD,  130, WHITE,  "(w-tw)/2", "790", ""),
    (101.8, 108.2, "НОГ",            FONT_BLACK, 300, WHITE,  "(w-tw)/2", "970", "box=1:boxcolor=0xFF5722:boxborderw=40"),
    (103.0, 108.2, "уважай • владей силой • действуй", FONT_CAVEAT, 60, ORANGE, "(w-tw)/2", "1480", ""),
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
with open('/tmp/v4_tiger_text.txt', 'w') as f:
    f.write(chain)
print(f"v3 tiger: {len(texts)} text events, filter len {len(chain)} chars")
