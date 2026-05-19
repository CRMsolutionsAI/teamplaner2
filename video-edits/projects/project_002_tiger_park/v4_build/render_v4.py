"""project_002 tiger v3 — dynamic cuts (22 shots), photo intercuts, fixed text positions, belly shot."""
import subprocess
import os

P = "video-edits/projects/project_002_tiger_park"
B = f"{P}/v4_build"
FOOTAGE = f"{P}/sources/footage"
PHOTOS = f"{P}/sources/photos_inline"

os.makedirs(f"{B}/segs", exist_ok=True)

W, H = 1080, 1920

LAYOUTS = {
    "FULL":   {"w": 1080, "h": 1920, "x": 0,   "y": 0},
    "CENTER": {"w": 720,  "h": 1200, "x": 180, "y": 360},
    "LEFT":   {"w": 600,  "h": 1000, "x": 40,  "y": 460},
    "RIGHT":  {"w": 600,  "h": 1000, "x": 440, "y": 460},
}

# kind: video_<LAYOUT> / photo_<LAYOUT> / BLACK
# (t0, t1, kind, src, trim_or_None, crop_face)
shots = [
    # M1 Hook (0-6)
    (0.0,   3.0,  "video_CENTER", "IMG_3489.mp4", 80,  False),
    (3.0,   6.0,  "BLACK",        None, None, False),
    # M2 Setting (6-22) — photos replaced with new clips
    (6.0,   9.0,  "video_RIGHT",  "IMG_3478_tiger_5s.mp4", 0,  False),
    (9.0,   12.0, "video_CENTER", "IMG_pool_wide.mov", 0, False),       # NEW: enclosure establishing
    (12.0,  16.0, "BLACK",        None, None, False),
    (16.0,  19.0, "video_LEFT",   "IMG_3489.mp4", 5,  False),
    (19.0,  22.0, "video_RIGHT",  "IMG_torso_close.mov", 0, False),     # NEW: close fur texture
    # M3 Process (22-44)
    (22.0,  26.0, "video_CENTER", "IMG_3489.mp4", 50, False),
    (26.0,  30.0, "video_LEFT",   "IMG_3485.mp4", 10, True),            # replaced photo
    (30.0,  34.0, "video_RIGHT",  "IMG_3489.mp4", 100, False),
    (34.0,  38.0, "video_LEFT",   "IMG_3485.mp4", 5, True),
    (38.0,  44.0, "video_CENTER", "IMG_3489.mp4", 130, False),
    # M4 5 Energies (44-60)
    (44.0,  48.0, "BLACK",        None, None, False),
    (48.0,  52.0, "video_CENTER", "IMG_3479_tiger_25s.mp4", 5, True),
    (52.0,  58.0, "BLACK",        None, None, False),
    (58.0,  60.0, "video_CENTER", "IMG_3489.mp4", 160, False),
    # M5 Lesson (60-78)
    (60.0,  66.0, "video_RIGHT",  "IMG_3489.mp4", 30, False),
    (66.0,  72.0, "BLACK",        None, None, False),
    (72.0,  78.0, "video_LEFT",   "IMG_3489.mp4", 90, False),
    # M6 Climax (78-95) — photos replaced
    (78.0,  83.0, "video_CENTER", "IMG_3489.mp4", 150, False),
    (83.0,  87.0, "video_CENTER", "IMG_torso_close.mov", 1, False),     # NEW: anatomy close (replaces belly photo)
    (87.0,  92.0, "BLACK",        None, None, False),
    (92.0,  95.0, "video_CENTER", "IMG_pool_swim.mov", 0, False),       # NEW: ⭐ tiger in pool — earth-inь meets fire
    # M7 Insight (95-108.2)
    (95.0,  101.0, "video_CENTER", "IMG_3489.mp4", 195, False),
    (101.0, 108.21,"BLACK",        None, None, False),
]


def render_segment(i, t0, t1, kind, src, trim, crop_face):
    duration = t1 - t0
    out = f"{B}/segs/seg_{i:02d}.mp4"

    if kind == "BLACK":
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r=30:d={duration}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
            out,
        ]
    elif kind.startswith("video_"):
        layout = kind.split("_")[1]
        L = LAYOUTS[layout]
        src_path = f"{FOOTAGE}/{src}"
        face_crop = "crop=iw:ih*0.75:0:ih*0.25," if crop_face else ""
        vf = (
            f"trim=duration={duration},setpts=PTS-STARTPTS,fps=30,"
            f"{face_crop}"
            f"scale={L['w']}:{L['h']}:force_original_aspect_ratio=increase,crop={L['w']}:{L['h']},"
            f"format=yuv420p"
        )
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
    elif kind.startswith("photo_"):
        layout = kind.split("_")[1]
        L = LAYOUTS[layout]
        src_path = f"{PHOTOS}/{src}"
        face_crop = "crop=iw:ih*0.7:0:ih*0.30," if crop_face else ""
        vf = (
            f"{face_crop}"
            f"scale={L['w']}:{L['h']}:force_original_aspect_ratio=increase,crop={L['w']}:{L['h']},"
            f"format=yuv420p,fps=30"
        )
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-loop", "1", "-t", f"{duration}", "-i", src_path,
            "-f", "lavfi", "-t", f"{duration}", "-i", f"color=c=black:s={W}x{H}:r=30",
            "-filter_complex",
            f"[0:v]{vf}[fg];[1:v][fg]overlay={L['x']}:{L['y']}[out]",
            "-map", "[out]", "-r", "30", "-t", f"{duration}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
            out,
        ]
    else:
        raise ValueError(kind)

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"FAIL seg {i:02d}: {r.stderr[-500:]}")
        return False
    print(f"OK   seg {i:02d} ({kind}) {duration:.2f}s")
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
