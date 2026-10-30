
import json
import argparse
import subprocess
from pathlib import Path

# Load Viral Forge settings
with open("config.json", "r") as file:
    config = json.load(file)

def create_short(input_video, start_time=0):
    input_path = Path(input_video)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Video not found: {input_video}"
        )

    if not config.get("source_type") == "licensed":
        raise ValueError("Only licensed sources are allowed.")

    duration = int(config.get("video_duration", 45))

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "viral_forge_short.mp4"

    command = [
        "ffmpeg",
        "-y",
        "-ss", str(start_time),
        "-i", str(input_path),
        "-t", str(duration),
        "-vf",
        "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        str(output_file)
    ]

    subprocess.run(command, check=True)

    print("Viral Forge Short created!")
    print(f"Output: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video", help="Input licensed video file")
    parser.add_argument("--start", type=int, default=0)

    args = parser.parse_args()

    create_short(args.video, args.start)
