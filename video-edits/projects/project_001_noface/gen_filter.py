#!/usr/bin/env python3
"""
Generate filter_complex for project_001 v7.
V7 changes:
  - Added 4 new own clips (IMG_5644, IMG_5635, IMG_5642, IMG_1756) to M4+finale
  - M4 tail (33.5-40s): IMG_5644 + IMG_7983(2s) + IMG_5642 — cuts every 2-2.5s
  - Finale (39.9-49.1s): IMG_5635 (3.1s) + IMG_1756 4K (3s) + cover_hero (3.1s)
  - fin_hero delayed to 46.0s (was 39.9s) — only 3s of static at very end
  - Input map: added [11-14] new clips, audio shifted to [15-19]
"""

BASE  = "/Users/natasa/teamplaner2/video-edits"
PRJ   = f"{BASE}/projects/project_001_noface"
RCB   = "/System/Volumes/Data/Applications/captions.app/Contents/Resources/RobotoCondensed-Bold.ttf"
CAV   = f"{BASE}/fonts/Caveat.ttf"

# ──────────────────────────────────────────────
#  INPUT INDEX MAP  (20 inputs total)
# [0]  loop1       cover_green_dragon_clean.png → M1 right + finale hero (split)
# [1]  loop1       cover_black_mustache_clean.png → M1 left cover
# [2]              nm_28515504                  → M2 night market people (ambient)
# [3]              IMG_0620 lanterns            → M2 own footage
# [4]              nm_28515508                  → M2 woman food (ambient)
# [5]              lw_34740034                  → M3 leather craft (ambient)
# [6]              IMG_0932.mp4                 → M3 hands (own, split)
# [7]              ch_36164500                  → M3 blacksmith (ambient)
# [8]  stream_loop IMG_1110.mp4                 → M4 own footage
# [9]              IMG_0506.mp4                 → M4 own footage
# [10] loop1       IMG_7983.png                 → M4 product photo (2s, 36-38s)
# [11]             IMG_5644_own.mov             → M4 new cut (33.5-36s)
# [12]             IMG_5635_own.mov             → Finale new cut (39.9-43s)
# [13]             IMG_5642_own.mov             → M4 tail new cut (38-40s)
# [14]             IMG_1756_own.mov             → Finale new cut 4K (43-46s)
# [15]             narrator_audio_53.5s         → audio
# [16]             music aqualina               → audio
# [17]             dust_swoosh SFX              → audio
# [18]             cartoon_bubble_pop           → audio
# [19]             film_title_transition        → audio
# ──────────────────────────────────────────────

SUBS = [
    (1.07,  3.20, "Обратите внимание на эту обложку.", False),
    (3.20,  4.31, "Это не просто сувенир из Таиланда —", False),
    (4.31,  7.28, "это «сейф» для моих документов,", True),
    (7.28,  8.80, "в котором им наконец-то спокойно.", False),
    (8.80, 10.70, "На ночных рынках это превращается", False),
    (10.70, 11.30, "в мини-перформанс.", True),
    (11.30, 12.85, "Ты не покупаешь готовое —", False),
    (12.85, 14.11, "ты создаёшь свою систему.", False),
    (14.11, 17.45, "Выбираешь цвет, аксессуары, ленту...", False),
    (17.45, 20.00, "Материал очень похож на кожу —", False),
    (20.00, 22.50, "я не поджигала для проверки,", False),
    (22.50, 24.50, "но тактильно это про надёжность.", True),
    (24.50, 25.80, "Пару минут магии,", False),
    (25.80, 27.63, "и мастер соединяет все детали воедино.", False),
    (27.63, 29.50, "Цена вопроса — 120 бат", True),
    (29.50, 31.74, "или всего 161 гривна.", False),
    (31.74, 33.50, "За эти деньги вы получаете", False),
    (33.50, 35.24, "не чехол, а эмоцию.", False),
    (35.24, 37.50, "Ваш паспорт ещё никогда не был", False),
    (37.50, 39.10, "таким красивым и персональным.", False),
    (39.10, 42.11, "Для меня это про уважение к своим границам.", False),
    (42.11, 45.01, "Даже самый скучный документ", False),
    (45.01, 47.61, "может стать частью твоей истории.", True),
]
# NOTE: last subtitle line removed — shown as large accent text instead

ACCENTS = [
    # M1 Hook 0-6.4s diagonal scatter
    (0.46, 5.90, "ОБРАТИ",    130, 60,  220, "white", "rcb"),
    (0.76, 5.90, "ВНИМАНИЕ",  110, 230, 380, "orange", "rcb"),
    (1.06, 5.90, "НА",         90, 550, 530, "white", "rcb"),
    (1.80, 5.90, "не сувенир", 85, "cw", 1620, "white", "cav"),
    (3.20, 5.90, "СЕЙФ",      200, "cw", 1440, "white", "rcb"),
    # M2 Night market diagonal scatter
    (6.15, 9.50, "НОЧНОЙ",    120, 60,  190, "white", "rcb"),
    (6.45, 9.50, "РЫНОК",     120, 340, 340, "orange", "rcb"),
    (6.75, 9.50, "ТАИЛАНД",    90, 620, 490, "white", "rcb"),
    (8.30, 9.50, "= мини-перформанс", 80, "cw", 1630, "white", "cav"),
    (10.09, 13.50, "ТЫ",      140, 60,  210, "white", "rcb"),
    (10.39, 13.50, "СОЗДАЁШЬ",120, 230, 360, "orange", "rcb"),
    (10.70, 13.50, "СВОЮ СИСТЕМУ", 80, 500, 510, "white", "rcb"),
    (11.90, 13.50, "свою систему", 80, "cw", 1630, "white", "cav"),
    (14.10, 15.40, "ЗНАЧКИ",  130, 60,  190, "white", "rcb"),
    (14.40, 15.40, "+ ленты + цвета", 78, "cw", 1630, "orange", "cav"),
    # M3 Process diagonal scatter
    (16.80, 21.20, "МАСТЕР",  140, 60,  210, "white", "rcb"),
    (17.10, 21.20, "+МАГИЯ",  100, 300, 370, "orange", "rcb"),
    (17.40, 21.20, "НАДЁЖНОСТЬ", 78, 550, 520, "white", "rcb"),
    (21.56, 23.40, "NATALIA",  90, "cw", 210, "orange", "rcb"),
    (21.90, 23.40, "выбивают имя", 70, "cw", 370, "white", "cav"),
    (22.48, 23.40, "ТУК-ТУК", 130, "cw", 1640, "orange", "rcb"),
    (23.40, 26.80, "РУЧНАЯ",  130, 60,  210, "white", "rcb"),
    (23.70, 26.80, "СБОРКА",  130, 240, 370, "orange", "rcb"),
    (24.80, 26.80, "тактильная надёжность", 70, "cw", 1630, "white", "cav"),
    # M4 Price
    (27.80, 40.20, "ЦЕНА",     90, "cw", 120, "white", "rcb"),
    (28.30, 40.20, "120",      320, "cw", 240, "white", "rcb"),
    (28.70, 40.20, "БАТ",     120, "cw", 590, "orange", "rcb"),
    (29.30, 40.20, "= 161 ГРН", 85, "cw", 730, "white", "cav"),
    # M5 Finale — multi-tier over video clips (43-46s)
    (43.10, 46.00, "ВАШ",     200, "cw", 1280, "white", "rcb"),
    (43.60, 46.00, "ПАСПОРТ", 200, "cw", 1480, "white", "rcb"),
    (44.90, 46.00, "— ваша история", 110, "cw", 1700, "orange", "cav"),
    # CTA question — large 3-tier on black canvas (46-49.1s), no image
    (46.10, 49.08, "А во что",        120, "cw", 650, "white", "rcb"),
    (46.40, 49.08, "«одеты»",         150, "cw", 800, "orange", "rcb"),
    (46.70, 49.08, "ваши документы?", 85,  "cw", 980, "white", "rcb"),
]

def escape(s):
    s = s.replace("\\", "\\\\")
    s = s.replace("'", "'")
    s = s.replace(":", "\\:")
    s = s.replace(",", "\\,")
    return s

def fade(t_in, t_out, fade_dur=0.3):
    fi = t_in
    fo = t_out - fade_dur
    return (f"if(lt(t\\,{fi+fade_dur:.2f})\\,max(0\\,(t-{fi:.2f})/{fade_dur:.2f})\\,"
            f"if(gt(t\\,{fo:.2f})\\,max(0\\,1-(t-{fo:.2f})/{fade_dur:.2f})\\,1))")

def sub_cmd(t_in, t_out, text, hi):
    color  = "0xFF5722" if hi else "0xFFFFFF"
    a = fade(t_in, t_out)
    txt = escape(text)
    return (
        f"drawtext=fontfile={RCB}\\:text='{txt}'\\:fontcolor={color}\\:fontsize=60"
        f"\\:x=(w-text_w)/2\\:y=1728"
        f"\\:enable='between(t\\,{t_in:.2f}\\,{t_out:.2f})'\\:alpha='{a}'"
        f"\\:box=1\\:boxcolor=0x000000AA\\:boxborderw=14"
    )

def accent_cmd(t_in, t_out, text, size, x, y, color, font):
    fontfile = RCB if font == "rcb" else CAV
    col = "0xFFFFFF" if color == "white" else "0xFF5722"
    xexpr = "(w-text_w)/2" if x == "cw" else str(x)
    a = fade(t_in, t_out)
    txt = escape(text)
    return (
        f"drawtext=fontfile={fontfile}\\:text='{txt}'\\:fontcolor={col}\\:fontsize={size}"
        f"\\:x={xexpr}\\:y={y}"
        f"\\:enable='between(t\\,{t_in:.2f}\\,{t_out:.2f})'\\:alpha='{a}'"
    )

# ──────────────────────────────────────────────
#  BUILD FILTER COMPLEX
# ──────────────────────────────────────────────
parts = []
FIF = "scale=-2:1493,crop=840:1493"
N   = "fps=30,"

# ── 1. VIDEO CLIP PREPROCESSING ──────────────────────────────────

# Cover PNGs (RGBA, no colorkey)
# green dragon: only for M1 hook (no finale hero — CTA is text-only)
parts.append("[0:v]fps=30,trim=duration=6.4,setpts=PTS-STARTPTS,scale=460:-2[m1_cg]")
parts.append("[1:v]fps=30,scale=420:-2,trim=duration=6.4,setpts=PTS-STARTPTS[m1_bm]")

# M2 (6.4-16.8s)
parts.append(f"[2:v]{N}trim=duration=3.4,setpts=PTS-STARTPTS+6.4/TB,{FIF}[c2]")
parts.append(f"[3:v]{N}trim=duration=3.5,setpts=PTS-STARTPTS+9.8/TB,{FIF}[c3]")
parts.append(f"[4:v]{N}trim=duration=3.5,setpts=PTS-STARTPTS+13.3/TB,{FIF}[c4]")

# M3 (16.8-28.8s)
parts.append(f"[5:v]{N}trim=duration=3.5,setpts=PTS-STARTPTS+16.8/TB,{FIF}[c5]")
parts.append(f"[6:v]{N}split=2[img0932a][img0932b]")
parts.append(f"[img0932a]trim=end=3.5,setpts=PTS-STARTPTS+20.3/TB,{FIF}[c6]")
parts.append(f"[7:v]{N}trim=duration=3.5,setpts=PTS-STARTPTS+23.8/TB,{FIF}[c7]")
parts.append(f"[img0932b]trim=start=4.0:end=5.8,setpts=PTS-STARTPTS+27.3/TB,{FIF}[c8]")

# M4 (28.8-40.0s) — 5 cuts, avg ~2.2s each for better rhythm
parts.append(f"[8:v]{N}loop=loop=-1:size=66:start=0,trim=duration=2.2,setpts=PTS-STARTPTS+28.8/TB,{FIF}[c9]")
# IMG_1110  28.8-31.0s
parts.append(f"[9:v]{N}trim=duration=2.5,setpts=PTS-STARTPTS+31.0/TB,{FIF}[c10]")
# IMG_0506  31.0-33.5s
parts.append(f"[11:v]{N}trim=duration=2.5,setpts=PTS-STARTPTS+33.5/TB,{FIF}[c11a]")
# IMG_5644  33.5-36.0s  NEW
parts.append(f"[10:v]{N}scale=-2:1493,crop=840:1493,trim=duration=2.0,setpts=PTS-STARTPTS+36.0/TB[c11b]")
# IMG_7983  36.0-38.0s  (2s only, was 4.17s)
parts.append(f"[13:v]{N}trim=duration=2.0,setpts=PTS-STARTPTS+38.0/TB,{FIF}[c11c]")
# IMG_5642  38.0-40.0s  NEW

# Finale (39.9-49.1s) — 2 video cuts then static cover
parts.append(f"[12:v]{N}trim=duration=3.1,setpts=PTS-STARTPTS+39.9/TB,{FIF}[cfin1]")
# IMG_5635  39.9-43.0s  NEW
parts.append(f"[14:v]{N}trim=duration=3.0,setpts=PTS-STARTPTS+43.0/TB,{FIF}[cfin2]")
# IMG_1756 4K  43.0-46.0s  NEW

# ── 2. BLACK CANVAS BASE ──────────────────────────────────────────
parts.append("color=c=black:s=1080x1920:r=30:d=49.1[base]")

# ── 3. OVERLAY CHAIN ─────────────────────────────────────────────
prev = "base"
clips = ["c2","c3","c4","c5","c6","c7","c8",
         "c9","c10","c11a","c11b","c11c",
         "cfin1","cfin2"]
for i, clip in enumerate(clips):
    out = f"l{i+1:02d}"
    parts.append(f"[{prev}][{clip}]overlay=120:214[{out}]")
    prev = out

# M1 covers (0-6.4s only, then pass through). No fin_hero — CTA is text-only.
parts.append(f"[{prev}][m1_bm]overlay=60:680:eof_action=pass[l_m1bm]")
parts.append("[l_m1bm][m1_cg]overlay=570:610:eof_action=pass[l_fin]")

# ── 4. TEXT OVERLAYS ─────────────────────────────────────────────
text_cmds = []
text_cmds.append(
    "drawbox=x=310:y=240:w=460:h=320:color=0xFF5722@1.0:t=fill"
    ":enable='between(t\\,28.30\\,40.20)'"
)
text_cmds.append(
    "drawbox=x=200:y=195:w=680:h=110:color=0x000000@1.0:t=fill"
    ":enable='between(t\\,21.56\\,23.40)'"
)
for args in ACCENTS:
    t_in, t_out, text, size, x, y, color, font = args
    text_cmds.append(accent_cmd(t_in, t_out, text, size, x, y, color, font))
for t_in, t_out, text, hi in SUBS:
    text_cmds.append(sub_cmd(t_in, t_out, text, hi))
text_cmds.append("eq=contrast=1.12:saturation=1.08:gamma_r=0.96:gamma_g=1.0:gamma_b=1.04")

filter_v = "[l_fin]" + ",".join(text_cmds) + "[v_out]"

# ── 5. AUDIO (indices +4 vs v6 due to 4 new video inputs) ────────
audio_parts = []
audio_parts.append(
    "[15:a]atempo=1.09,"
    "loudnorm=I=-16:TP=-1.5:LRA=11,"
    "volume=2.0,"
    "asplit=2[narrator][narrator_sc]"
)
audio_parts.append("[16:a]volume=0.06[mraw]")
audio_parts.append(
    "[mraw][narrator_sc]sidechaincompress="
    "threshold=0.02:ratio=20:attack=5:release=300:"
    "makeup=1:level_sc=2[mducked]"
)
SFX_MS = [1060, 6400, 10700, 13000, 17000]
audio_parts.append("[17:a]asplit=5[sfxA][sfxB][sfxC][sfxD][sfxE]")
for lbl, ms, vol in zip(["A","B","C","D","E"], SFX_MS, [0.25,0.25,0.22,0.22,0.25]):
    audio_parts.append(f"[sfx{lbl}]adelay={ms}|{ms},volume={vol}[sfx{lbl.lower()}]")
audio_parts.append("[18:a]adelay=28300|28300,volume=0.35[sfxf]")
audio_parts.append("[19:a]adelay=40400|40400,volume=0.20[sfxg]")
audio_parts.append(
    "[narrator][mducked][sfxa][sfxb][sfxc][sfxd][sfxe][sfxf][sfxg]"
    "amix=inputs=9:normalize=0:duration=first[a_out]"
)

# ── WRITE OUTPUT ─────────────────────────────────────────────────
all_parts = parts + [filter_v] + audio_parts
out_file = f"{PRJ}/filter_v5.txt"
with open(out_file, "w", encoding="utf-8") as f:
    f.write(";\n".join(all_parts))

print(f"Written: {out_file}")
print(f"Parts: {len(all_parts)}")
