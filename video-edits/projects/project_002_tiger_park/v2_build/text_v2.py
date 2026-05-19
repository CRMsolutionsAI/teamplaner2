"""project_002 tiger_park v2 — text positioned around windows (not over them)."""

FONT_BOLD = "/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Bold.ttf"
FONT_BLACK = "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Black.ttf"
FONT_CAVEAT = "/home/user/teamplaner2/video-edits/fonts/Caveat.ttf"

WHITE = "white"
ORANGE = "0xFF5722"

# Position rules:
# CENTER layout (window 720x1200 at x=180-900 y=360-1560): text top (y<300) or bottom (y>1620)
# LEFT layout (window 600x1000 at x=40-640 y=460-1460): text on right (x≥720)
# RIGHT layout (window 600x1000 at x=440-1040 y=460-1460): text on left (x≤400)
# BLACK: text fills center
# FULL: text at top (y<200) or bottom (y>1700) safe zones

texts = [
    # 0-3 CENTER (window): top text
    (0.5, 2.9, "встреча с",          FONT_CAVEAT, 90,  WHITE,  "(w-tw)/2", "180", ""),
    (1.0, 2.9, "ТИГРОМ",             FONT_BLACK,  170, ORANGE, "(w-tw)/2", "260", "box=1:boxcolor=black@0.7:boxborderw=15"),

    # 3-6 BLACK: hook with promise of value
    (3.0, 5.9, "ПРОВЕРКА",           FONT_BLACK, 180, WHITE,  "(w-tw)/2", "600", ""),
    (3.5, 5.9, "ПРОШИВКИ",           FONT_BLACK, 160, ORANGE, "(w-tw)/2", "830", "box=1:boxcolor=black@0.7:boxborderw=20"),
    (4.5, 5.9, "одно правило, которое работает везде", FONT_CAVEAT, 60, WHITE, "(w-tw)/2", "1100", ""),

    # 6-12 RIGHT (window x=440-1040): text on left side (x<400)
    (6.5, 11.9, "TIGER",              FONT_BLACK, 130, WHITE,  "40", "700", ""),
    (7.0, 11.9, "WORLD",              FONT_BLACK, 140, ORANGE, "40", "860", ""),
    (8.0, 11.9, "Ратчабури",          FONT_CAVEAT, 70, WHITE,  "40", "1050", ""),

    # 12-16 BLACK
    (12.0, 15.9, "15",                FONT_BLACK, 400, WHITE,  "(w-tw)/2", "500", "box=1:boxcolor=0xFF5722:boxborderw=40"),
    (12.5, 15.9, "МИНУТ",             FONT_BOLD,  130, ORANGE, "(w-tw)/2", "1000", ""),
    (13.0, 15.9, "истины",            FONT_CAVEAT, 80, WHITE,  "(w-tw)/2", "1160", ""),

    # 16-22 LEFT (window x=40-640): text on right (x>720)
    (16.5, 21.9, "ОДИН",              FONT_BLACK, 130, WHITE,  "720", "680", ""),
    (17.0, 21.9, "НА ОДИН",           FONT_BLACK, 140, ORANGE, "720", "830", ""),
    (18.0, 21.9, "с хищником",        FONT_CAVEAT, 70, WHITE,  "720", "1000", ""),

    # 22-30 CENTER: top text
    (22.5, 29.9, "ВЫБОР",             FONT_BLACK, 140, WHITE,  "(w-tw)/2", "200", ""),
    (23.0, 29.9, "котята или хищник", FONT_CAVEAT, 75, ORANGE, "(w-tw)/2", "1640", ""),

    # 30-37 RIGHT: text left
    (30.5, 36.9, "ПРАВИЛА",           FONT_BLACK, 130, WHITE,  "40", "700", ""),
    (31.0, 36.9, "ДОМА",              FONT_BLACK, 160, ORANGE, "40", "850", "box=1:boxcolor=black@0.7:boxborderw=15"),

    # 37-44 LEFT: text right
    (37.5, 43.9, "от процесса",       FONT_CAVEAT, 80, WHITE, "720", "680", ""),
    (38.5, 43.9, "К ЭМОЦИЯМ",         FONT_BLACK, 110, ORANGE, "720", "820", ""),

    # 44-48 BLACK: tier-text reveal of 5 energies
    (44.5, 47.9, "СИЛА",              FONT_BLACK, 130, WHITE,  "(w-tw)/2", "320", ""),
    (45.0, 47.9, "МОЩЬ",              FONT_BLACK, 130, ORANGE, "(w-tw)/2", "510", ""),
    (45.5, 47.9, "ВЛАСТЬ",            FONT_BLACK, 130, WHITE,  "(w-tw)/2", "700", ""),
    (46.0, 47.9, "ОПАСНОСТЬ",         FONT_BLACK, 130, ORANGE, "(w-tw)/2", "890", ""),
    (46.5, 47.9, "ЖЕЛАНИЕ",           FONT_BLACK, 130, WHITE,  "(w-tw)/2", "1080", ""),

    # 48-53 CENTER: top text
    (48.5, 52.9, "не страх",          FONT_CAVEAT, 80, WHITE,  "(w-tw)/2", "200", ""),
    (49.0, 52.9, "УВАЖЕНИЕ",          FONT_BLACK, 120, ORANGE, "(w-tw)/2", "1640", ""),

    # 53-58 BLACK: "5 ЭНЕРГИЙ" card
    (53.0, 57.9, "5",                 FONT_BLACK, 350, WHITE,  "(w-tw)/2", "550", "box=1:boxcolor=0xFF5722:boxborderw=40"),
    (53.5, 57.9, "ЭНЕРГИЙ",           FONT_BLACK, 140, ORANGE, "(w-tw)/2", "980", ""),
    (54.5, 57.9, "одного существа",   FONT_CAVEAT, 70, WHITE, "(w-tw)/2", "1140", ""),

    # 58-60 CENTER: brief
    (58.2, 59.9, "ПРЕДЕЛЬНОЕ",        FONT_BOLD, 100, WHITE,  "(w-tw)/2", "200", ""),

    # 60-67 RIGHT: text left
    (60.5, 66.9, "ГЛАВНЫЙ",           FONT_BLACK, 130, WHITE,  "40", "700", ""),
    (61.0, 66.9, "УРОК",              FONT_BLACK, 200, ORANGE, "40", "860", "box=1:boxcolor=black@0.7:boxborderw=15"),

    # 67-75 BLACK: BIG RULE card — main value
    (67.0, 74.9, "НЕ ЩЕКОЧИ",         FONT_BLACK, 150, WHITE,  "(w-tw)/2", "550", ""),
    (67.5, 74.9, "СИЛУ",              FONT_BLACK, 250, WHITE,  "(w-tw)/2", "780", "box=1:boxcolor=0xFF5722:boxborderw=40"),
    (69.0, 74.9, "правило работает:",  FONT_CAVEAT, 60, WHITE, "(w-tw)/2", "1160", ""),
    (70.0, 74.9, "переговоры • команда • отношения", FONT_CAVEAT, 55, ORANGE, "(w-tw)/2", "1240", ""),

    # 75-83 LEFT: text right
    (75.5, 82.9, "гладь",              FONT_CAVEAT, 100, WHITE, "720", "680", ""),
    (76.0, 82.9, "СИЛЬНЕЕ",            FONT_BLACK, 150, ORANGE, "720", "820", ""),
    (77.0, 82.9, "сила требует",       FONT_CAVEAT, 65, WHITE, "720", "1020", ""),
    (77.5, 82.9, "УВЕРЕННОСТИ",        FONT_BOLD, 70, ORANGE, "720", "1100", ""),

    # 83-91 CENTER: top text
    (83.5, 90.9, "признаёшь",          FONT_CAVEAT, 80, WHITE, "(w-tw)/2", "200", ""),
    (84.0, 90.9, "ВЕС",                FONT_BLACK, 180, ORANGE, "(w-tw)/2", "1620", ""),

    # 91-98 FULL: top safe zone
    (91.5, 97.9, "ОТКРЫВАЕТ",          FONT_BLACK, 130, WHITE, "(w-tw)/2", "120", "box=1:boxcolor=black@0.8:boxborderw=15"),
    (92.0, 97.9, "ЖИВОТ",              FONT_BLACK, 180, ORANGE, "(w-tw)/2", "1700", "box=1:boxcolor=black@0.8:boxborderw=15"),

    # 98-104 BLACK: СИМВОЛ ДОВЕРИЯ card
    (98.0, 103.9, "СИМВОЛ",            FONT_BLACK, 150, WHITE,  "(w-tw)/2", "600", ""),
    (98.5, 103.9, "ДОВЕРИЯ",           FONT_BLACK, 190, ORANGE, "(w-tw)/2", "830", "box=1:boxcolor=black@0.7:boxborderw=20"),
    (100.0, 103.9, "которое нельзя купить", FONT_CAVEAT, 65, WHITE, "(w-tw)/2", "1170", ""),

    # 104-108.2 BLACK: final CTA — actionable
    (104.0, 108.2, "МИР",              FONT_BLACK, 240, WHITE,  "(w-tw)/2", "500", ""),
    (104.4, 108.2, "У ТВОИХ",          FONT_BOLD,  130, WHITE,  "(w-tw)/2", "790", ""),
    (104.8, 108.2, "НОГ",              FONT_BLACK, 300, WHITE,  "(w-tw)/2", "970", "box=1:boxcolor=0xFF5722:boxborderw=40"),
    (106.0, 108.2, "уважай • владей силой • действуй", FONT_CAVEAT, 60, ORANGE, "(w-tw)/2", "1480", ""),
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
with open('/tmp/v2_tiger_text.txt', 'w') as f:
    f.write(chain)
print(f"v2 tiger: {len(texts)} text events, filter len {len(chain)} chars")
