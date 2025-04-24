import subprocess
import sys
from pathlib import Path

# Config
VIDEO_PATH = Path("/home/Kion/Videos/ChannelSimVids/2-stupid-dogs-complete/S01E01 Door Jam-Goldflipper-Where's The Bone.mp4")
LOGO_PATH = Path("/home/Kion/Videos/ChannelSimVids/2-stupid-dogs-complete/logo.png")
MULTICAST_ADDRESS = "239.255.0.1"
PORT = 1234

# Validate files
if not VIDEO_PATH.exists():
    sys.exit(f"Video file does not exist: {VIDEO_PATH}")
if not LOGO_PATH.exists():
    sys.exit(f"Logo file does not exist: {LOGO_PATH}")

# Build the ffmpeg command
ffmpeg_command = [
    "ffmpeg",
    "-re",
    "-i", str(VIDEO_PATH),
    "-i", str(LOGO_PATH),
    "-filter_complex", f"overlay=10:10",
    "-c:v", "mpeg2video", "-b:v", "1500k",
    "-c:a", "mp2", "-b:a", "192k",
    "-f", "mpegts",
    f"udp://{MULTICAST_ADDRESS}:{PORT}?pkt_size=1316"
]

# Run it
try:
    subprocess.run(ffmpeg_command, check=True)
except subprocess.CalledProcessError as e:
    print("FFMPEG exited with an error:", e)
