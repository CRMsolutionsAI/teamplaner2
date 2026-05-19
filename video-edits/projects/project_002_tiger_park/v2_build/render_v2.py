"""project_002 tiger_park v2 — window-in-black paradigm + natural voice (no silenceremove)."""
import subprocess
import os

P = "video-edits/projects/project_002_tiger_park"
B = f"{P}/v2_build"
FOOTAGE = f"{P}/sources/footage"

os.makedirs(f"{B}/segs", exist_ok=True)

W, H = 1080, 1920

# Layout windows (within 1080x1920 canvas)
LAYOUTS = {
    "FULL":   {"w": 1080, "h": 1920, "x": 0,   "y": 0},                  # no border
    "CENTER": {"w": 720,  "h": 1200, "x": 180, "y": 360},                # space top/bottom for text
    "LEFT":   {"w": 600,  "h": 1000, "x": 40,  "y": 460},                # text on right
    "RIGHT":  {"w": 600,  "h": 1000, "x": 440, "y": 460},                # text on left
}

# (t0, t1, layout, src, trim_start, crop_face)
# 18 shots, 108.2s total
shots = [
    # M1 Hook (0-6)
    (0.0,   3.0,   "CENTER", "IMG_3489.mp4", 80,  False),     # POV close-up tiger fur
    (3.0,   6.0,   "BLACK",  None, None, False),              # "ПРОВЕРКА ПРОШИВКИ" card
    # M2 Setting (6-22)
    (6.0,   12.0,  "RIGHT",  "IMG_3478_tiger_5s.mp4", 0,   False),  # Wide approach
    (12.0,  16.0,  "BLACK",  None, None, False),              # "15 МИНУТ ИСТИНЫ" card
    (16.0,  22.0,  "LEFT",   "IMG_3489.mp4", 5,   False),     # Inside enclosure
    # M3 Process (22-44)
    (22.0,  30.0,  "CENTER", "IMG_3489.mp4", 50,  False),     # Choice context
    (30.0,  37.0,  "RIGHT",  "IMG_3489.mp4", 100, False),     # Rangers
    (37.0,  44.0,  "LEFT",   "IMG_3485.mp4", 5,   True),      # To emotions
    # M4 5 Energies (44-60)
    (44.0,  48.0,  "BLACK",  None, None, False),              # Tier reveal: СИЛА/МОЩЬ/ВЛАСТЬ/...
    (48.0,  53.0,  "CENTER", "IMG_3479_tiger_25s.mp4", 5, True),  # Danger
    (53.0,  58.0,  "BLACK",  None, None, False),              # "5 ЭНЕРГИЙ" card
    (58.0,  60.0,  "CENTER", "IMG_3489.mp4", 160, False),     # Respect
    # M5 The Lesson (60-91)
    (60.0,  67.0,  "RIGHT",  "IMG_3489.mp4", 30,  False),     # Main lesson intro
    (67.0,  75.0,  "BLACK",  None, None, False),              # BIG RULE: "НЕ ЩЕКОЧИ СИЛУ"
    (75.0,  83.0,  "LEFT",   "IMG_3489.mp4", 90,  False),     # "Гладь сильнее"
    (83.0,  91.0,  "CENTER", "IMG_3489.mp4", 150, False),     # Recognizing weight
    # M6 Climax (91-104)
    (91.0,  98.0,  "FULL",   "IMG_3479_tiger_25s.mp4", 12, True),  # Big moment: tiger rolls
    (98.0,  104.0, "BLACK",  None, None, False),              # "СИМВОЛ ДОВЕРИЯ" card
    # M7 Insight (104-108.2)
    (104.0, 108.21, "BLACK", None, None, False),              # CTA "МИР У ТВОИХ НОГ"
]


def render_segment(i, t0, t1, layout, src, trim, crop_face):
    duration = t1 - t0
    out = f"{B}/segs/seg_{i:02d}.mp4"

    if layout == "BLACK":
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r=30:d={duration}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
            out,
        ]
    else:
        L = LAYOUTS[layout]
        src_path = f"{FOOTAGE}/{src}"
        # Build video filter: face crop (if needed) → scale to layout window → place on black canvas
        face_crop = "crop=iw:ih*0.75:0:ih*0.25," if crop_face else ""
        vf = (
            f"trim=duration={duration},setpts=PTS-STARTPTS,fps=30,"
            f"{face_crop}"
            f"scale={L['w']}:{L['h']}:force_original_aspect_ratio=increase,crop={L['w']}:{L['h']},"
            f"format=yuv420p"
        )
        # Overlay window on black canvas
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{trim}", "-i", src_path,
            "-f", "lavfi", "-t", f"{duration}", "-i", f"color=c=black:s={W}x{H}:r=30",
            "-filter_complex",
            f"[0:v]{vf}[fg];[1:v][fg]overlay={L['x']}:{L['y']}[out]",
            "-map", "[out]", "-r", "30", "-t", f"{duration}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
            "-an", out,
        ]

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"FAIL seg {i:02d}: {r.stderr[-500:]}")
        return False
    print(f"OK   seg {i:02d} ({layout}) {duration:.2f}s")
    return True


ok = 0
for i, shot in enumerate(shots):
    if render_segment(i, *shot):
        ok += 1
print(f"\n{ok}/{len(shots)} rendered.")

with open(f"{B}/concat.txt", "w") as f:
    for i in range(len(shots)):
        f.write(f"file 'segs/seg_{i:02d}.mp4'\n")
print(f"concat.txt written.")
