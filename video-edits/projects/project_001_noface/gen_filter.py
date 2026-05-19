#!/usr/bin/env python3
"""Generate filter_complex for project_001 v5 final render."""

import sys

BASE  = "/Users/natasa/teamplaner2/video-edits"
PRJ   = f"{BASE}/projects/project_001_noface"
RCB   = "/System/Volumes/Data/Applications/captions.app/Contents/Resources/RobotoCondensed-Bold.ttf"
CAV   = f"{BASE}/fonts/Caveat.ttf"

# ──────────────────────────────────────────────
#  SUBTITLE LINES  (sped-up times = orig / 1.09)
#  hi=True  →  orange font (iOS-highlighter feel)
# ──────────────────────────────────────────────
SUBS = [
    (1.07,  3.20, "Обратите внимание на эту обложку.", False),
    (3.20,  4.31, "Это не просто сувенир из Таиланда —", False),
    (4.31,  7.28, "это «сейф» для моих документов,", True),   # key: сейф
    (7.28,  8.80, "в котором им наконец-то спокойно.", False),
    (8.80, 10.70, "На ночных рынках это превращается", False),
    (10.70, 11.30, "в мини-перформанс.", True),               # key
    (11.30, 12.85, "Ты не покупаешь готовое —", False),
    (12.85, 14.11, "ты создаёшь свою систему.", False),
    (14.11, 17.45, "Выбираешь цвет, аксессуары, ленту...", False),
    (17.45, 20.00, "Материал очень похож на кожу —", False),
    (20.00, 22.50, "я не поджигала для проверки,", False),
    (22.50, 24.50, "но тактильно это про надёжность.", True),  # key
    (24.50, 25.80, "Пару минут магии,", False),
    (25.80, 27.63, "и мастер соединяет все детали воедино.", False),
    (27.63, 29.50, "Цена вопроса — 120 бат", True),            # key: 120
    (29.50, 31.74, "или всего 161 гривна.", False),
    (31.74, 33.50, "За эти деньги вы получаете", False),
    (33.50, 35.24, "не чехол, а эмоцию.", False),
    (35.24, 37.50, "Ваш паспорт ещё никогда не был", False),
    (37.50, 39.10, "таким красивым и персональным.", False),
    (39.10, 42.11, "Для меня это про уважение к своим границам.", False),
    (42.11, 45.01, "Даже самый скучный документ", False),
    (45.01, 47.61, "может стать частью твоей истории.", True),  # key
    (47.61, 49.08, "А во что «одеты» ваши документы?", True),
]

# ──────────────────────────────────────────────
#  ACCENT TEXT  (diagonal scatter + display text)
#  Each: (t_in, t_out, text, fontsize, x, y, color, font)
#    font: 'rcb'=Roboto Condensed Bold  'cav'=Caveat
# ──────────────────────────────────────────────
ACCENTS = [
    # M1 Hook 0-6.4s — diagonal scatter 3 words
    (0.46, 5.90, "ОБРАТИ",    130, 60,  220, "white", "rcb"),
    (0.76, 5.90, "ВНИМАНИЕ",  110, 230, 380, "orange", "rcb"),
    (1.06, 5.90, "НА",         90, 550, 530, "white", "rcb"),
    (1.80, 5.90, "не сувенир", 85, "cw", 1620, "white", "cav"),
    (3.20, 5.90, "СЕЙФ",      200, "cw", 1440, "white", "rcb"),

    # M2 Night market 6.4-16.8s — diagonal scatter
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

    # M3 Process 16.8-29.3s — diagonal scatter
    (16.80, 21.20, "МАСТЕР",  140, 60,  210, "white", "rcb"),
    (17.10, 21.20, "+МАГИЯ",  100, 300, 370, "orange", "rcb"),
    (17.40, 21.20, "НАДЁЖНОСТЬ", 78, 550, 520, "white", "rcb"),
    # NATALIA box (iOS highlighter style)
    (21.56, 23.40, "NATALIA",  90, "cw", 210, "orange", "rcb"),
    (21.90, 23.40, "выбивают имя", 70, "cw", 370, "white", "cav"),
    (22.48, 23.40, "ТУК-ТУК", 130, "cw", 1640, "orange", "rcb"),
    # Diagonal: РУЧНАЯ СБОРКА
    (23.40, 26.80, "РУЧНАЯ",  130, 60,  210, "white", "rcb"),
    (23.70, 26.80, "СБОРКА",  130, 240, 370, "orange", "rcb"),
    (24.80, 26.80, "тактильная надёжность", 70, "cw", 1630, "white", "cav"),

    # M4 Price 29.3-40.4s
    (27.80, 40.20, "ЦЕНА",     90, "cw", 120, "white", "rcb"),
    (28.30, 40.20, "120",      320, "cw", 240, "white", "rcb"),  # box added below
    (28.70, 40.20, "БАТ",     120, "cw", 590, "orange", "rcb"),
    (29.30, 40.20, "= 161 ГРН", 85, "cw", 730, "white", "cav"),

    # M5 Finale 40.4-49.08s
    (43.10, 49.08, "ВАШ",     200, "cw", 1280, "white", "rcb"),
    (43.60, 49.08, "ПАСПОРТ", 200, "cw", 1480, "white", "rcb"),
    (44.90, 49.08, "— ваша история", 110, "cw", 1700, "orange", "cav"),
]

def escape(s):
    """Escape text for ffmpeg drawtext."""
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
    bcolor = "0x000000AA"
    a = fade(t_in, t_out)
    txt = escape(text)
    return (
        f"drawtext=fontfile={RCB}\\:text='{txt}'\\:fontcolor={color}\\:fontsize=60"
        f"\\:x=(w-text_w)/2\\:y=1728"
        f"\\:enable='between(t\\,{t_in:.2f}\\,{t_out:.2f})'\\:alpha='{a}'"
        f"\\:box=1\\:boxcolor={bcolor}\\:boxborderw=14"
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

# ── 1. VIDEO CLIP PREPROCESSING ─────────────────────────────────
# Frame-in-frame: scale to height=1493, crop to 840x1493, place at x=120,y=214
FIF = "scale=-2:1493,crop=840:1493"

# [0] IMG_0468 — looped, 6.4s, t=0
N = "fps=30,"  # normalize fps before any processing
parts.append(f"[0:v]{N}loop=loop=-1:size=147:start=0,trim=duration=6.4,setpts=PTS-STARTPTS+0.0/TB,{FIF}[c1]")
# [1] nm_28515504 people food stand — trim 3.4s, t=6.4
parts.append(f"[1:v]{N}trim=duration=3.4,setpts=PTS-STARTPTS+6.4/TB,{FIF}[c2]")
# [2] IMG_0620 lanterns (horizontal 1280x720) — crop portrait, 3.5s, t=9.8
parts.append(f"[2:v]{N}trim=duration=3.5,setpts=PTS-STARTPTS+9.8/TB,scale=2667:1493,crop=840:1493[c3]")
# [3] nm_28515508 woman food — 3.5s, t=13.3
parts.append(f"[3:v]{N}trim=duration=3.5,setpts=PTS-STARTPTS+13.3/TB,{FIF}[c4]")
# [4] lw_34740034 leather — 3.5s, t=16.8
parts.append(f"[4:v]{N}trim=duration=3.5,setpts=PTS-STARTPTS+16.8/TB,{FIF}[c5]")
# [5] IMG_0932 — split for two uses
parts.append(f"[5:v]{N}split=2[img0932a][img0932b]")
parts.append(f"[img0932a]trim=end=3.5,setpts=PTS-STARTPTS+20.3/TB,{FIF}[c6]")
parts.append(f"[img0932b]trim=start=4.0:end=5.8,setpts=PTS-STARTPTS+27.0/TB,{FIF}[c8]")
# [6] ch_36164500 blacksmith — 3.5s, t=23.8
parts.append(f"[6:v]{N}trim=duration=3.5,setpts=PTS-STARTPTS+23.8/TB,{FIF}[c7]")
# [7] IMG_1110 — looped 3.2s, t=28.8
parts.append(f"[7:v]{N}loop=loop=-1:size=66:start=0,trim=duration=3.2,setpts=PTS-STARTPTS+28.8/TB,{FIF}[c9]")
# [8] pp_7010563 passport — 4.5s, t=32.0
parts.append(f"[8:v]{N}trim=duration=4.5,setpts=PTS-STARTPTS+32.0/TB,{FIF}[c10]")
# [9] sv_36861553 street vendor — 3.4s, t=36.5
parts.append(f"[9:v]{N}trim=duration=3.4,setpts=PTS-STARTPTS+36.5/TB,{FIF}[c11]")

# Finale PNGs [10]=IMG_7983 [11]=cover_black [12]=cover_green
parts.append(f"[10:v]{N}scale=-2:1493,crop=840:1493,setpts=PTS-STARTPTS+39.9/TB[fin_bg]")
# Cover cards: colorkey white bg → transparent, then scale
parts.append(f"[11:v]{N}colorkey=color=0xFFFFFF:similarity=0.12:blend=0.05,scale=440:-2[cov_black]")
parts.append(f"[12:v]{N}colorkey=color=0xFFFFFF:similarity=0.12:blend=0.05,scale=440:-2[cov_green]")

# ── 2. BLACK CANVAS BASE ──────────────────────────────────────────
parts.append("color=c=black:s=1080x1920:r=30:d=49.1[base]")

# ── 3. OVERLAY CHAIN ─────────────────────────────────────────────
prev = "base"
clips = ["c1","c2","c3","c4","c5","c6","c7","c8","c9","c10","c11","fin_bg"]
for i, clip in enumerate(clips):
    out = f"l{i+1:02d}"
    parts.append(f"[{prev}][{clip}]overlay=120:214[{out}]")
    prev = out

# Cover card overlays for finale (slide in from sides)
# Black cover: slides from left x=-440→40 over 0.5s starting t=40.5
# x expr can't use commas in overlay, use if-based expr
parts.append(
    f"[{prev}][cov_black]overlay="
    f"x='if(gte(t\\,40.5)\\,min(40\\,(-440+(t-40.5)/0.5*480))\\,-440)'"
    f":y=190:enable='gte(t,40.4)'[l_cb]"
)
# Green cover: slides from right x=1080→640 over 0.5s starting t=41.2
parts.append(
    f"[l_cb][cov_green]overlay="
    f"x='if(gte(t\\,41.2)\\,max(640\\,(1080-(t-41.2)/0.5*440))\\,1080)'"
    f":y=190:enable='gte(t,41.1)'[l_cg]"
)

# ── 4. TEXT OVERLAYS ─────────────────────────────────────────────
text_cmds = []

# 120-price box (iOS highlighter style: drawbox behind 120)
text_cmds.append(
    "drawbox=x=310:y=240:w=460:h=320:color=0xFF5722@1.0:t=fill"
    ":enable='between(t\\,28.30\\,40.20)'"
)

# Accent text
for args in ACCENTS:
    t_in, t_out, text, size, x, y, color, font = args
    text_cmds.append(accent_cmd(t_in, t_out, text, size, x, y, color, font))

# NATALIA box extra: drawbox behind NATALIA text
text_cmds.append(
    "drawbox=x=200:y=195:w=680:h=110:color=0x000000@1.0:t=fill"
    ":enable='between(t\\,21.56\\,23.40)'"
)

# Subtitles
for t_in, t_out, text, hi in SUBS:
    text_cmds.append(sub_cmd(t_in, t_out, text, hi))

# Color grade
text_cmds.append("eq=contrast=1.12:saturation=1.08:gamma_r=0.96:gamma_g=1.0:gamma_b=1.04")

# Chain all text commands onto video
prev_v = "l_cg"
filter_v = "[" + prev_v + "]" + ",".join(text_cmds) + "[v_out]"

# ── 5. AUDIO ─────────────────────────────────────────────────────
audio_parts = []

# Narrator: atempo 1.09
audio_parts.append("[13:a]atempo=1.09[narrator]")

# Music: sidechain ducked under narrator
audio_parts.append("[14:a]volume=0.1[mraw]")
audio_parts.append("[mraw][narrator]sidechaincompress=threshold=0.02:ratio=14:attack=8:release=400:makeup=1:level_sc=2[mducked]")

# SFX events (in ms):  t_in_sped × 1000
sfx_events = [1060, 6400, 10700, 13000, 17000, 28300, 40400]
audio_parts.append(f"[15:a]asplit=5[sfxA][sfxB][sfxC][sfxD][sfxE]")
audio_parts.append(f"[sfxA]adelay={sfx_events[0]}|{sfx_events[0]},volume=0.25[sfx1]")
audio_parts.append(f"[sfxB]adelay={sfx_events[1]}|{sfx_events[1]},volume=0.25[sfx2]")
audio_parts.append(f"[sfxC]adelay={sfx_events[2]}|{sfx_events[2]},volume=0.22[sfx3]")
audio_parts.append(f"[sfxD]adelay={sfx_events[3]}|{sfx_events[3]},volume=0.22[sfx4]")
audio_parts.append(f"[sfxE]adelay={sfx_events[4]}|{sfx_events[4]},volume=0.25[sfx5]")
audio_parts.append(f"[16:a]adelay={sfx_events[5]}|{sfx_events[5]},volume=0.35[sfx6]")
audio_parts.append(f"[17:a]adelay={sfx_events[6]}|{sfx_events[6]},volume=0.2[sfx7]")
audio_parts.append(
    "[narrator][mducked][sfx1][sfx2][sfx3][sfx4][sfx5][sfx6][sfx7]"
    "amix=inputs=9:normalize=0:duration=first[a_out]"
)

# ── COMBINE ALL ──────────────────────────────────────────────────
all_parts = parts + [filter_v] + audio_parts
filter_str = ";\n".join(all_parts)

out_file = f"{PRJ}/filter_v5.txt"
with open(out_file, "w", encoding="utf-8") as f:
    f.write(filter_str)

print(f"Written: {out_file}")
print(f"Lines: {len(all_parts)}")
