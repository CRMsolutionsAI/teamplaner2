"""project_002 tiger_park v1 — render 14 shots from 4 source clips."""
import subprocess
import os

P = "video-edits/projects/project_002_tiger_park"
B = f"{P}/v1_build"
FOOTAGE = f"{P}/sources/footage"

os.makedirs(f"{B}/segs", exist_ok=True)

W, H = 1080, 1920

# Storyboard: 14 shots, 68s total
# Format: (t0, t1, kind, src, trim_start, crop_face)
# kind: "video_full" (no face crop), "video_no_face" (crop top to hide face), "black"
shots = [
    # M1 Hook (0-7)
    (0.0, 3.5, "video_full", "IMG_3489.mp4", 80, False),       # POV tiger fur close-up
    (3.5, 7.0, "video_full", "IMG_3478_tiger_5s.mp4", 0, False),  # Wide approach to enclosure
    # M2 System (7-19)
    (7.0, 13.0, "video_no_face", "IMG_3479_tiger_25s.mp4", 2, True),  # Tiger on platform (crop face)
    (13.0, 19.0, "video_full", "IMG_3489.mp4", 5, False),      # Inside enclosure POV
    # M3 Energy (19-34)
    (19.0, 25.0, "video_full", "IMG_3489.mp4", 60, False),     # Tiger lying, slow look
    (25.0, 30.0, "video_no_face", "IMG_3485.mp4", 4, True),    # Full tiger + her (face crop)
    (30.0, 34.0, "video_full", "IMG_3489.mp4", 120, False),    # Tiger eye/face close-up
    # M4 Lesson (34-49)
    (34.0, 39.0, "video_full", "IMG_3489.mp4", 30, False),     # Hand on fur
    (39.0, 45.0, "video_full", "IMG_3489.mp4", 90, False),     # Petting POV
    (45.0, 49.0, "video_full", "IMG_3489.mp4", 150, False),    # Firm petting
    # M5 Climax (49-58)
    (49.0, 54.0, "video_full", "IMG_3489.mp4", 170, False),    # Deep into fur
    (54.0, 58.0, "video_no_face", "IMG_3479_tiger_25s.mp4", 15, True),  # Tiger position shift
    # M6 Insight (58-68)
    (58.0, 63.0, "video_full", "IMG_3489.mp4", 195, False),    # Last petting
    (63.0, 68.1, "black", None, None, False),                  # CTA card on black
]


def render_segment(i, t0, t1, kind, src, trim, crop_face):
    duration = t1 - t0
    out = f"{B}/segs/seg_{i:02d}.mp4"

    if kind == "black":
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r=30:d={duration}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
            out,
        ]
    else:
        # All source clips are vertical (720x1280 or 960x1280)
        # Need to scale to 1080x1920 vertical
        src_path = f"{FOOTAGE}/{src}"
        if crop_face:
            # Crop top 25% to hide her face, then scale to fill
            vf = (
                f"trim=duration={duration},setpts=PTS-STARTPTS,fps=30,"
                f"crop=iw:ih*0.75:0:ih*0.25,"
                f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                f"format=yuv420p"
            )
        else:
            vf = (
                f"trim=duration={duration},setpts=PTS-STARTPTS,fps=30,"
                f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                f"format=yuv420p"
            )
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{trim}", "-i", src_path,
            "-vf", vf,
            "-r", "30", "-t", f"{duration}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
            "-an", out,
        ]

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
