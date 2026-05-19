import subprocess
import os
import shlex

P = "video-edits/projects/project_001_noface"
B = f"{P}/v6_build"
FOOTAGE = f"{P}/sources/footage"
PHOTOS = f"{P}/sources/photos"

os.makedirs(f"{B}/segs", exist_ok=True)

W, H = 1080, 1920
# Frame for video clips: 900x1400 centered on black
FW, FH = 900, 1400
FX = (W - FW) // 2  # 90
FY = (H - FH) // 2  # 260

shots = [
    # M1 (0-6.36) Hook
    (0.0,  2.0,   "png_zoom",          f"{PHOTOS}/cover_green_dragon_clean.png",     0.7, 0.95),
    (2.0,  4.0,   "png_slide_right",   f"{PHOTOS}/cover_black_mustache_clean.png",   None, None),
    (4.0,  6.36,  "png_two_covers",    None, None, None),
    # M2 (6.36-18.18) Night market
    (6.36, 9.0,   "video_letterbox",   f"{FOOTAGE}/IMG_0620_night_market_lanterns.mp4", 0, None),
    (9.0,  11.5,  "video_frame",       f"{FOOTAGE}/IMG_0468.mp4", 0, 1.0),
    (11.5, 14.0,  "video_frame",       f"{FOOTAGE}/IMG_0932.mp4", 0.5, 1.0),
    (14.0, 16.5,  "video_frame",       f"{FOOTAGE}/IMG_0506.mp4", 0, 1.05),
    (16.5, 18.18, "video_frame",       f"{FOOTAGE}/IMG_0468.mp4", 2.5, 1.2),
    # M3 (18.18-31.82) Process
    (18.18, 21.0, "video_frame",       f"{FOOTAGE}/IMG_1110.mp4", 0, 1.1),
    (21.0, 23.5,  "video_frame",       f"{FOOTAGE}/IMG_0932.mp4", 3.0, 1.0),
    (23.5, 26.0,  "video_frame",       f"{FOOTAGE}/IMG_0468.mp4", 1.0, 1.3),
    (26.0, 28.5,  "video_frame",       f"{FOOTAGE}/IMG_1110.mp4", 0.3, 1.4),
    (28.5, 31.82, "png_zoom",          f"{PHOTOS}/cover_black_mustache_clean.png", 1.0, 1.1),
    # M4 (31.82-43.64) Value/120
    (31.82, 34.0, "png_zoom",          f"{PHOTOS}/cover_green_dragon_clean.png", 0.85, 1.0),
    (34.0, 37.5,  "black",             None, None, None),
    (37.5, 41.0,  "black",             None, None, None),
    (41.0, 43.64, "png_zoom",          f"{PHOTOS}/cover_green_dragon_clean.png", 0.9, 1.05),
    # M5 (43.64-48.6) Finale CTA
    (43.64, 46.0, "png_zoom",          f"{PHOTOS}/cover_green_dragon_clean.png", 0.95, 1.1),
    (46.0, 48.6,  "png_two_covers",    None, None, None),
]

def render_segment(i, t0, t1, kind, src, p1, p2):
    """Render a single segment to segs/seg_{i:02d}.mp4"""
    duration = t1 - t0
    out = f"{B}/segs/seg_{i:02d}.mp4"
    
    if kind == "black":
        cmd = [
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", f"color=c=black:s={W}x{H}:r=30:d={duration}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
            out
        ]
    
    elif kind == "png_zoom":
        zs, ze = p1, p2  # zoom start, zoom end
        # Use scale + crop animation OR zoompan
        # Simpler: load PNG, scale to height*ze, animate scale with t
        # PNG dimensions ~378x512 → scale to fit max 800 wide
        # Final height: 1050. Use zoompan effect.
        cmd = [
            "ffmpeg", "-y", "-loop", "1", "-t", f"{duration}", "-i", src,
            "-f", "lavfi", "-t", f"{duration}", "-i", f"color=c=black:s={W}x{H}:r=30",
            "-filter_complex",
            (f"[0:v]scale=-1:1050,setpts=PTS-STARTPTS,"
             f"zoompan=z='{zs}+({ze}-{zs})*on/{int(duration*30)}':d=1:x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':s=800x1050:fps=30,"
             f"format=rgba[png];"
             f"[1:v][png]overlay=(W-w)/2:(H-h)/2:format=auto[out]"),
            "-map", "[out]", "-r", "30", "-t", f"{duration}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
            out
        ]
    
    elif kind == "png_slide_right":
        # PNG slides in from right edge (off-screen) to centered
        cmd = [
            "ffmpeg", "-y", "-loop", "1", "-t", f"{duration}", "-i", src,
            "-f", "lavfi", "-t", f"{duration}", "-i", f"color=c=black:s={W}x{H}:r=30",
            "-filter_complex",
            (f"[0:v]scale=-1:1050,format=rgba[png];"
             f"[1:v][png]overlay=x='if(lt(t,0.5),W-(W-(W-w)/2)*(t/0.5),(W-w)/2)':y=(H-h)/2:format=auto[out]"),
            "-map", "[out]", "-r", "30", "-t", f"{duration}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
            out
        ]
    
    elif kind == "png_two_covers":
        # Both covers: green left, black right, both centered vertically
        green = f"{PHOTOS}/cover_green_dragon_clean.png"
        black = f"{PHOTOS}/cover_black_mustache_clean.png"
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-t", f"{duration}", "-i", green,
            "-loop", "1", "-t", f"{duration}", "-i", black,
            "-f", "lavfi", "-t", f"{duration}", "-i", f"color=c=black:s={W}x{H}:r=30",
            "-filter_complex",
            (f"[0:v]scale=-1:900,format=rgba[g];"
             f"[1:v]scale=-1:900,format=rgba[b];"
             f"[2:v][g]overlay=120:(H-h)/2-50:format=auto[bg1];"
             f"[bg1][b]overlay=W-w-120:(H-h)/2+50:format=auto[out]"),
            "-map", "[out]", "-r", "30", "-t", f"{duration}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
            out
        ]
    
    elif kind == "video_frame":
        # Video in 900x1400 frame, centered on black
        # p1 = trim_start, p2 = zoom factor
        trim_start, zoom = p1, p2
        # Scale to fit 900x1400 maintaining aspect, then crop and zoom
        scale_h = int(FH * zoom)
        scale_w = int(FW * zoom)
        cmd = [
            "ffmpeg", "-y", "-ss", f"{trim_start}", "-i", src,
            "-f", "lavfi", "-t", f"{duration}", "-i", f"color=c=black:s={W}x{H}:r=30",
            "-filter_complex",
            (f"[0:v]trim=duration={duration},setpts=PTS-STARTPTS,fps=30,"
             f"scale={scale_w}:{scale_h}:force_original_aspect_ratio=increase,crop={FW}:{FH},"
             f"format=yuv420p[fg];"
             f"[1:v][fg]overlay={FX}:{FY}[out]"),
            "-map", "[out]", "-r", "30", "-t", f"{duration}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
            out
        ]
    
    elif kind == "video_letterbox":
        # Horizontal video, scaled to 1080 wide, letterboxed on black
        trim_start = p1
        cmd = [
            "ffmpeg", "-y", "-ss", f"{trim_start}", "-i", src,
            "-f", "lavfi", "-t", f"{duration}", "-i", f"color=c=black:s={W}x{H}:r=30",
            "-filter_complex",
            (f"[0:v]trim=duration={duration},setpts=PTS-STARTPTS,fps=30,"
             f"scale={W}:-2,format=yuv420p[fg];"
             f"[1:v][fg]overlay=0:(H-h)/2[out]"),
            "-map", "[out]", "-r", "30", "-t", f"{duration}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
            out
        ]
    
    else:
        raise ValueError(f"Unknown kind: {kind}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FAIL seg {i:02d} ({kind}): {result.stderr[-500:]}")
        return False
    print(f"OK   seg {i:02d} ({kind}) {duration:.2f}s -> {out}")
    return True

# Render all segments
ok_count = 0
for i, shot in enumerate(shots):
    if render_segment(i, *shot):
        ok_count += 1
print(f"\n{ok_count}/{len(shots)} segments rendered.")

# Build concat list
with open(f"{B}/concat.txt", "w") as f:
    for i in range(len(shots)):
        f.write(f"file 'segs/seg_{i:02d}.mp4'\n")
print(f"Wrote {B}/concat.txt")
