import subprocess
import random

playlist = [
    "/home/Kion/Videos/ChannelSimVids/2-stupid-dogs-complete/S01E01 Door Jam-Goldflipper-Where's The Bone.mp4",
    "/home/Kion/Videos/ChannelSimVids/2-stupid-dogs-complete/S01E02 Cornflakes-Greg-Home Is Where Your Head Is.mp4",
    "/home/Kion/Videos/ChannelSimVids/2-stupid-dogs-complete/S01E03 Vegas Buffet-Quark-Love In The Park.mp4"
]

# Main FFmpeg stream to multicast
streamer = subprocess.Popen([
    "ffmpeg",
    "-re",
    "-f", "mpegts",
    "-i", "-",
    "-c", "copy",
    "-f", "mpegts",
    "udp://239.255.0.1:1234?pkt_size=1316"
], stdin=subprocess.PIPE)

try:
    while True:
        file = random.choice(playlist)
        print(f"Now playing: {file}")

        feeder = subprocess.Popen([
            "ffmpeg",
            "-re",
            "-i", file,
            "-vf", "scale=640:480",  # scale if needed
            "-c:v", "mpeg2video",
            "-q:v", "2",              # quality: 1-31 (lower is better)
            "-b:v", "1500k",          # bitrate for smoother playback
            "-maxrate", "2000k",
            "-bufsize", "4000k",
            "-c:a", "mp2",
            "-b:a", "192k",
            "-ar", "48000",
            "-f", "mpegts",
            "-"
        ], stdout=streamer.stdin)

        feeder.wait()
except KeyboardInterrupt:
    print("Stopping stream...")
    streamer.stdin.close()
    streamer.wait()
