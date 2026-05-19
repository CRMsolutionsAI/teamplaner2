#!/usr/bin/env python3
"""
Generate filter_complex for project_001 v6.
FIXED v3 criticals:
  - [AUDIO] narrator split → copy1 for sidechain key, copy2 for mix
  - [VIDEO] removed pp_7010563 (passport stock) + sv_36861553 (street vendor stock)
             replaced with own footage: IMG_0506.mp4 + IMG_7983 (product photo)
  - [VIDEO] pexels kept ONLY for ambient: night market, leather craft, blacksmith
"""

BASE  = "/Users/natasa/teamplaner2/video-edits"
PRJ   = f"{BASE}/projects/project_001_noface"
RCB   = "/System/Volumes/Data/Applications/captions.app/Contents/Resources/RobotoCondensed-Bold.ttf"
CAV   = f"{BASE}/fonts/Caveat.ttf"

# ──────────────────────────────────────────────
#  INPUT INDEX MAP
# [0]  stream_loop  IMG_0468.mp4          → M1 hook
# [1]              nm_28515504            → M2 night market people (ambient)
# [2]              IMG_0620 lanterns      → M2 lanterns own footage
# [3]              nm_28515508            → M2 woman food (ambient)
# [4]              lw_34740034            → M3 leather craft (ambient)
# [5]              IMG_0932.mp4           → M3 hands (own footage, split)
# [6]              ch_36164500            → M3 blacksmith hammer (ambient)
# [7]  stream_loop  IMG_1110.mp4          → M4 product (own footage)
# [8]              IMG_0506.mp4           → M4 own footage (NO stock)
# [9]  loop 1      IMG_7983.png           → M4+finale product (own, split)
# [10] loop 1      cover_black_mustache   → finale slide
# [11] loop 1      cover_green_dragon     → finale slide
# [12]             narrator_audio_53.5s   → audio
# [13]             music aqualina         → audio
# [14]             dust_swoosh SFX        → audio
# [15]             cartoon_bubble_pop     → audio
# [16]             film_title_transition  → audio
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
    (47.61, 49.08, "А во что «одеты» ваши документы?", True),
]

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
    # M5 Finale
    (43.10, 49.08, "ВАШ",     200, "cw", 1280, "white", "rcb"),
    (43.60, 49.08, "ПАСПОРТ", 200, "cw", 1480, "white", "rcb"),
    (44.90, 49.08, "— ваша история", 110, "cw", 1700, "orange", "cav"),
]

def escape(s):
    s = s.replace("\\", "\\\\")
    s = s.replace("'", "’")   # curly apostrophe avoids shell issues
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
N   = "fps=30,"   # normalize fps

# ── 1. VIDEO CLIP PREPROCESSING ──────────────────────────────────
# M1 (0-6.4s): IMG_0468 looped, portrait 720×1280
parts.append(f"[0:v]{N}loop=loop=-1:size=147:start=0,trim=duration=6.4,setpts=PTS-STARTPTS+0.0/TB,{FIF}[c1]")
# M2 (6.4-16.8s): ambient night market + own footage
parts.append(f"[1:v]{N}trim=duration=3.4,setpts=PTS-STARTPTS+6.4/TB,{FIF}[c2]")   # nm_28515504
parts.append(f"[2:v]{N}trim=duration=3.5,setpts=PTS-STARTPTS+9.8/TB,scale=2667:1493,crop=840:1493[c3]")  # IMG_0620 horizontal
parts.append(f"[3:v]{N}trim=duration=3.5,setpts=PTS-STARTPTS+13.3/TB,{FIF}[c4]")  # nm_28515508
# M3 (16.8-28.8s): leather ambient + own footage + blacksmith ambient
parts.append(f"[4:v]{N}trim=duration=3.5,setpts=PTS-STARTPTS+16.8/TB,{FIF}[c5]")  # lw_34740034 leather
parts.append(f"[5:v]{N}split=2[img0932a][img0932b]")
parts.append(f"[img0932a]trim=end=3.5,setpts=PTS-STARTPTS+20.3/TB,{FIF}[c6]")     # IMG_0932 first 3.5s
parts.append(f"[6:v]{N}trim=duration=3.5,setpts=PTS-STARTPTS+23.8/TB,{FIF}[c7]")  # ch_36164500 blacksmith
parts.append(f"[img0932b]trim=start=4.0:end=5.8,setpts=PTS-STARTPTS+27.3/TB,{FIF}[c8]")  # IMG_0932 tail
# M4 (28.8-40.0s): OWN FOOTAGE ONLY (no passport/product stock)
parts.append(f"[7:v]{N}loop=loop=-1:size=66:start=0,trim=duration=3.2,setpts=PTS-STARTPTS+28.8/TB,{FIF}[c9]")  # IMG_1110
parts.append(f"[8:v]{N}trim=duration=3.83,setpts=PTS-STARTPTS+32.0/TB,{FIF}[c10]")  # IMG_0506 own
# IMG_7983 (own product photo) — split for M4 tail + finale
parts.append(f"[9:v]{N}scale=-2:1493,crop=840:1493,split=2[img7983a][img7983b]")
parts.append(f"[img7983a]trim=duration=4.17,setpts=PTS-STARTPTS+35.83/TB[c11]")    # M4 35.83-40.0
parts.append(f"[img7983b]setpts=PTS-STARTPTS+39.9/TB[fin_bg]")                      # M5 finale 39.9-49.1
# Finale cover cards (own product photos)
parts.append(f"[10:v]{N}colorkey=color=0xFFFFFF:similarity=0.12:blend=0.05,scale=440:-2[cov_black]")
parts.append(f"[11:v]{N}colorkey=color=0xFFFFFF:similarity=0.12:blend=0.05,scale=440:-2[cov_green]")

# ── 2. BLACK CANVAS BASE ──────────────────────────────────────────
parts.append("color=c=black:s=1080x1920:r=30:d=49.1[base]")

# ── 3. OVERLAY CHAIN ─────────────────────────────────────────────
prev = "base"
clips = ["c1","c2","c3","c4","c5","c6","c7","c8","c9","c10","c11","fin_bg"]
for i, clip in enumerate(clips):
    out = f"l{i+1:02d}"
    parts.append(f"[{prev}][{clip}]overlay=120:214[{out}]")
    prev = out

# Cover card slide-in for finale
parts.append(
    f"[{prev}][cov_black]overlay="
    f"x='if(gte(t\\,40.5)\\,min(40\\,(-440+(t-40.5)/0.5*480))\\,-440)'"
    f":y=190:enable='gte(t,40.4)'[l_cb]"
)
parts.append(
    f"[l_cb][cov_green]overlay="
    f"x='if(gte(t\\,41.2)\\,max(640\\,(1080-(t-41.2)/0.5*440))\\,1080)'"
    f":y=190:enable='gte(t,41.1)'[l_cg]"
)

# ── 4. TEXT OVERLAYS ─────────────────────────────────────────────
text_cmds = []
# 120 price box
text_cmds.append(
    "drawbox=x=310:y=240:w=460:h=320:color=0xFF5722@1.0:t=fill"
    ":enable='between(t\\,28.30\\,40.20)'"
)
# NATALIA box
text_cmds.append(
    "drawbox=x=200:y=195:w=680:h=110:color=0x000000@1.0:t=fill"
    ":enable='between(t\\,21.56\\,23.40)'"
)
# Accent text
for args in ACCENTS:
    t_in, t_out, text, size, x, y, color, font = args
    text_cmds.append(accent_cmd(t_in, t_out, text, size, x, y, color, font))
# Subtitles
for t_in, t_out, text, hi in SUBS:
    text_cmds.append(sub_cmd(t_in, t_out, text, hi))
# Color grade
text_cmds.append("eq=contrast=1.12:saturation=1.08:gamma_r=0.96:gamma_g=1.0:gamma_b=1.04")

filter_v = "[l_cg]" + ",".join(text_cmds) + "[v_out]"

# ── 5. AUDIO — CRITICAL FIX ──────────────────────────────────────
# narrator MUST be split: copy1 → sidechain key, copy2 → final mix
audio_parts = []

# Narrator: atempo + loudnorm + SPLIT
audio_parts.append(
    "[12:a]atempo=1.09,"
    "loudnorm=I=-16:TP=-1.5:LRA=11,"
    "asplit=2[narrator][narrator_sc]"
)
# Music: sidechain ducked under narrator
audio_parts.append("[13:a]volume=0.1[mraw]")
audio_parts.append(
    "[mraw][narrator_sc]sidechaincompress="
    "threshold=0.02:ratio=14:attack=8:release=400:"
    "makeup=1:level_sc=2[mducked]"
)
# SFX events (in ms): text reveals + price accent + finale
SFX_MS = [1060, 6400, 10700, 13000, 17000]
audio_parts.append(f"[14:a]asplit=5[sfxA][sfxB][sfxC][sfxD][sfxE]")
for lbl, ms, vol in zip(["A","B","C","D","E"], SFX_MS, [0.25,0.25,0.22,0.22,0.25]):
    audio_parts.append(f"[sfx{lbl}]adelay={ms}|{ms},volume={vol}[sfx{lbl.lower()}]")
audio_parts.append(f"[15:a]adelay=28300|28300,volume=0.35[sfxf]")    # price bubble
audio_parts.append(f"[16:a]adelay=40400|40400,volume=0.20[sfxg]")    # finale transition
# Final mix: narrator (full volume) + ducked music + SFX
audio_parts.append(
    "[narrator][mducked][sfxa][sfxb][sfxc][sfxd][sfxe][sfxf][sfxg]"
    "amix=inputs=9:normalize=0:duration=first[a_out]"
)

# ── COMBINE ALL ──────────────────────────────────────────────────
all_parts = parts + [filter_v] + audio_parts
out_file = f"{PRJ}/filter_v5.txt"
with open(out_file, "w", encoding="utf-8") as f:
    f.write(";\n".join(all_parts))

print(f"Written: {out_file}")
print(f"Parts: {len(all_parts)}")
