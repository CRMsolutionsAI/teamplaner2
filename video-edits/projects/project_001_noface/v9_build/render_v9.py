"""v9 render — v8 + text overlap fix in M3 + NATALIA later."""
import subprocess
import os

P = "video-edits/projects/project_001_noface"
B = f"{P}/v9_build"
FOOTAGE = f"{P}/sources/footage"
PHOTOS = f"{P}/sources/photos"
STOCK = f"{P}/sources/stock"

os.makedirs(f"{B}/segs", exist_ok=True)

W, H = 1080, 1920
FW, FH = 900, 1400
FX, FY = (W - FW) // 2, (H - FH) // 2

# Premium hook: ONE filter_complex with xfade transitions + spring entrances
# Hook spans 0.0 → 6.36
HOOK_OUT = f"{B}/segs/seg_00_hook.mp4"

def render_hook():
    """Render 0.0-6.36s as a single segment with premium animations."""
    green = f"{PHOTOS}/cover_green_dragon_clean.png"
    black = f"{PHOTOS}/cover_black_mustache_clean.png"
    inside = f"{PHOTOS}/cover_black_open_inside.png"

    # Shot A (0.0-2.4): green dragon spring-in + Ken Burns
    #   zoom = 1.5 → 1.0 in 0.5s (punch-in), then 1.0 → 1.06 Ken Burns
    # Shot B (2.4-4.6): mustache cover slides from bottom-right with rotation
    # Shot C (4.6-6.36): two covers settled side-by-side with parallax
    # xfade between A→B (0.35s) and B→C (0.35s)

    filt = (
        # === SHOT A (green dragon, 0.0-2.4, spring punch-in + Ken Burns) ===
        f"[0:v]scale=900:-1,format=rgba,"
        f"zoompan=z='if(lt(on,15),1.5-0.5*pow(on/15,0.6),"
        f"if(lt(on,22),1.0-0.04*sin((on-15)*0.7),"
        f"1.0+0.06*(on-22)/50))':"
        f"d=1:x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':s=900x1170:fps=30,"
        f"trim=duration=2.4,setpts=PTS-STARTPTS,"
        f"fade=t=in:st=0:d=0.25:alpha=1[A_png];"
        f"color=c=black:s={W}x{H}:r=30:d=2.4[A_bg];"
        f"[A_bg][A_png]overlay=(W-w)/2:(H-h)/2:format=auto:eof_action=pass[A];"

        # === SHOT B (mustache, 2.4-4.6, slide-in from bottom-right with rotation) ===
        f"[1:v]scale=900:-1,format=rgba,"
        # rotate from -12deg to 0 in first 0.4s, then static
        f"rotate='if(lt(t,0.4),-12*PI/180*(1-t/0.4),0)':"
        f"c=none:ow=rotw(0):oh=roth(0),"
        f"trim=duration=2.2,setpts=PTS-STARTPTS[B_png];"
        # Place on black canvas with slide-in motion
        f"color=c=black:s={W}x{H}:r=30:d=2.2[B_bg];"
        f"[B_bg][B_png]overlay="
        f"x='if(lt(t,0.5),W-((W-(W-w)/2))*(t/0.5)+50*(1-t/0.5),(W-w)/2)':"
        f"y='if(lt(t,0.5),H-((H-(H-h)/2))*(t/0.5)+80*(1-t/0.5),(H-h)/2)':"
        f"format=auto:eof_action=pass,"
        f"fade=t=in:st=0:d=0.25[B];"

        # === SHOT C (two covers side-by-side with parallax sway, 4.6-6.36) ===
        f"[2:v]scale=-1:880,format=rgba[Cg];"
        f"[3:v]scale=-1:880,format=rgba[Cb];"
        f"color=c=black:s={W}x{H}:r=30:d=1.76[C_bg];"
        # Green: drifts slightly up over time; Black: drifts slightly down
        f"[C_bg][Cg]overlay="
        f"x='90+10*sin(t*1.2)':"
        f"y='(H-h)/2-30-15*t':format=auto:eof_action=pass[C1];"
        f"[C1][Cb]overlay="
        f"x='W-w-90-10*sin(t*1.2)':"
        f"y='(H-h)/2+30+15*t':format=auto:eof_action=pass,"
        f"fade=t=in:st=0:d=0.3[C];"

        # === xfade transitions ===
        # A (2.4s) → B (2.2s) with 0.35s overlap → at offset 2.4-0.35 = 2.05s
        f"[A][B]xfade=transition=fade:duration=0.35:offset=2.05[AB];"
        # AB total = 2.4 + 2.2 - 0.35 = 4.25s
        # AB → C (1.76s) with 0.35s overlap → offset 4.25 - 0.35 = 3.90s
        f"[AB][C]xfade=transition=fade:duration=0.35:offset=3.90[ABC];"
        # ABC total = 4.25 + 1.76 - 0.35 = 5.66s — need 6.36
        # Pad to 6.36 with tpad
        f"[ABC]tpad=stop_mode=clone:stop_duration=0.7[hook]"
    )

    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-t", "2.4", "-i", green,
        "-loop", "1", "-t", "2.2", "-i", black,
        "-loop", "1", "-t", "1.76", "-i", green,
        "-loop", "1", "-t", "1.76", "-i", black,
        "-filter_complex", filt,
        "-map", "[hook]", "-r", "30", "-t", "6.36",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
        HOOK_OUT
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("HOOK FAIL:", r.stderr[-2000:])
        return False
    print(f"OK hook -> {HOOK_OUT}")
    return True


# Remaining shots (after hook, 6.36 → 48.6) — realigned for M4 voice sync
shots = [
    # M2 (6.36-18.94) Night market — interleave her footage + 2 Pexels stocks (food stand context)
    (6.36, 9.08,  "video_letterbox",   f"{FOOTAGE}/IMG_0620_night_market_lanterns.mp4", 0, None),
    (9.08, 12.10, "video_frame",       f"{STOCK}/nm_28515504_people_food_stand.mp4", 0.5, 1.0),  # STOCK: people at food stand
    (12.10, 13.49, "video_frame",      f"{FOOTAGE}/IMG_0468.mp4", 0, 1.0),
    (13.49, 15.12, "video_frame",      f"{STOCK}/nm_28515508_woman_food_stand.mp4", 0.3, 1.0),   # STOCK: woman at food stand
    (15.12, 17.59, "video_frame",      f"{FOOTAGE}/IMG_0506.mp4", 0, 1.05),
    (17.59, 18.94, "video_frame",      f"{FOOTAGE}/IMG_1110.mp4", 0, 1.1),
    # M3 (18.94-32.7) Process — MORE shots, faster cuts, detail switching
    (18.94, 20.77, "video_frame",      f"{FOOTAGE}/IMG_1110.mp4", 0.2, 1.1),   # мастер за работой
    (20.77, 22.5,  "video_frame",      f"{FOOTAGE}/IMG_0932.mp4", 3.0, 1.0),   # пару минут (process)
    (22.5, 24.0,   "video_frame",      f"{FOOTAGE}/IMG_0468.mp4", 1.0, 1.15),  # тактильно — close-up cover
    (24.0, 25.42,  "video_frame",      f"{FOOTAGE}/IMG_0506.mp4", 0.5, 1.2),   # надёжно — detail
    (25.42, 27.5,  "video_frame",      f"{FOOTAGE}/IMG_1110.mp4", 0.5, 1.3),   # соединяет детали
    (27.5, 29.8,   "video_frame",      f"{FOOTAGE}/IMG_0932.mp4", 5.0, 1.4),   # finishing touch
    (29.8, 32.7,   "png_zoom",         f"{PHOTOS}/cover_black_mustache_clean.png", 0.95, 1.08),  # NATALIA name reveal
    # M4 (32.7-40.88) Value/120 — voice "120 БАТ" at 33.05
    (32.7, 33.01,  "png_zoom",         f"{PHOTOS}/cover_green_dragon_clean.png", 0.92, 0.96),
    (33.01, 36.03, "black",            None, None, None),  # BIG 120 BAT reveal
    (36.03, 38.5,  "black",            None, None, None),  # = 161 ГРН
    (38.5, 40.88,  "png_zoom",         f"{PHOTOS}/cover_black_open_inside.png", 0.88, 0.98),  # NEW: open inside detail for "за уникальность"
    # M5 (40.88-48.6) Finale — more variety with open_inside PNG
    (40.88, 43.14, "png_zoom",         f"{PHOTOS}/cover_green_dragon_clean.png", 0.88, 1.04),  # ЭМОЦИЯ
    (43.14, 44.7,  "png_zoom",         f"{PHOTOS}/cover_green_dragon_clean.png", 0.95, 1.1),   # ВАШ ПАСПОРТ
    (44.7, 46.5,   "png_zoom",         f"{PHOTOS}/cover_black_open_inside.png", 0.92, 1.05),   # detail interior
    (46.5, 48.62,  "png_two_covers_finale", None, None, None),
]


def render_segment(i, t0, t1, kind, src, p1, p2):
    duration = t1 - t0
    out = f"{B}/segs/seg_{i:02d}.mp4"

    if kind == "black":
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
            "-i", f"color=c=black:s={W}x{H}:r=30:d={duration}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
            out,
        ]
    elif kind == "png_zoom":
        zs, ze = p1, p2
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-loop", "1", "-t", f"{duration}", "-i", src,
            "-f", "lavfi", "-t", f"{duration}", "-i", f"color=c=black:s={W}x{H}:r=30",
            "-filter_complex",
            (f"[0:v]scale=-1:1050,setpts=PTS-STARTPTS,"
             f"zoompan=z='{zs}+({ze}-{zs})*on/{int(duration*30)}':"
             f"d=1:x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':s=800x1050:fps=30,"
             f"format=rgba[png];"
             f"[1:v][png]overlay=(W-w)/2:(H-h)/2:format=auto[out]"),
            "-map", "[out]", "-r", "30", "-t", f"{duration}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
            out,
        ]
    elif kind == "png_two_covers_finale":
        green = f"{PHOTOS}/cover_green_dragon_clean.png"
        black = f"{PHOTOS}/cover_black_mustache_clean.png"
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-loop", "1", "-t", f"{duration}", "-i", green,
            "-loop", "1", "-t", f"{duration}", "-i", black,
            "-f", "lavfi", "-t", f"{duration}", "-i", f"color=c=black:s={W}x{H}:r=30",
            "-filter_complex",
            (f"[0:v]scale=-1:900,format=rgba[g];"
             f"[1:v]scale=-1:900,format=rgba[b];"
             # Subtle parallax: green drifts up-left, black drifts down-right
             f"[2:v][g]overlay=x='120+8*sin(t*1.4)':y='(H-h)/2-50-6*t':format=auto:eof_action=pass[bg1];"
             f"[bg1][b]overlay=x='W-w-120-8*sin(t*1.4)':y='(H-h)/2+50+6*t':format=auto:eof_action=pass[out]"),
            "-map", "[out]", "-r", "30", "-t", f"{duration}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
            out,
        ]
    elif kind == "video_frame":
        trim_start, zoom = p1, p2
        scale_h = int(FH * zoom)
        scale_w = int(FW * zoom)
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{trim_start}", "-i", src,
            "-f", "lavfi", "-t", f"{duration}", "-i", f"color=c=black:s={W}x{H}:r=30",
            "-filter_complex",
            (f"[0:v]trim=duration={duration},setpts=PTS-STARTPTS,fps=30,"
             f"scale={scale_w}:{scale_h}:force_original_aspect_ratio=increase,crop={FW}:{FH},"
             f"format=yuv420p[fg];"
             f"[1:v][fg]overlay={FX}:{FY}[out]"),
            "-map", "[out]", "-r", "30", "-t", f"{duration}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
            out,
        ]
    elif kind == "video_letterbox":
        trim_start = p1
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{trim_start}", "-i", src,
            "-f", "lavfi", "-t", f"{duration}", "-i", f"color=c=black:s={W}x{H}:r=30",
            "-filter_complex",
            (f"[0:v]trim=duration={duration},setpts=PTS-STARTPTS,fps=30,"
             f"scale={W}:-2,format=yuv420p[fg];"
             f"[1:v][fg]overlay=0:(H-h)/2[out]"),
            "-map", "[out]", "-r", "30", "-t", f"{duration}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
            out,
        ]
    else:
        raise ValueError(f"Unknown kind: {kind}")

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"FAIL seg {i:02d} ({kind}): {r.stderr[-700:]}")
        return False
    print(f"OK   seg {i:02d} ({kind}) {duration:.2f}s")
    return True


if not render_hook():
    raise SystemExit(1)

ok = 0
for i, shot in enumerate(shots, start=1):
    if render_segment(i, *shot):
        ok += 1

print(f"\n{ok}/{len(shots)} secondary segments rendered.")

with open(f"{B}/concat.txt", "w") as f:
    f.write("file 'segs/seg_00_hook.mp4'\n")
    for i in range(1, len(shots) + 1):
        f.write(f"file 'segs/seg_{i:02d}.mp4'\n")
print(f"Wrote {B}/concat.txt")
