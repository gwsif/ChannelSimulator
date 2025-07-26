# This one is using RTP
import subprocess
import random

playlist = [
    r"C:\Users\blupu\OneDrive\Videos\Cartoons\Two Stupid Dogs\2 Stupid Dogs - 1x01 - (Door Jam) - (Goldflipper) - (Where's The Bone) -DarkDream-.mp4",
    r"C:\Users\blupu\OneDrive\Videos\Cartoons\Two Stupid Dogs\2 Stupid Dogs - 1x02 - (Cornflakes) - (Greg) - (Home Is Where Your Head Is) -DarkDream-.mp4",
    r"C:\Users\blupu\OneDrive\Videos\Cartoons\Two Stupid Dogs\2 Stupid Dogs - 1x03 - (Vegas Buffet) - (Quark) - (Love In The Park) -DarkDream-.mp4",
    r"C:\Users\blupu\OneDrive\Videos\Cartoons\Two Stupid Dogs\2 Stupid Dogs - 1x04 - (Show And Tell) - (Queen Bea) - (At The Drive In) -DarkDream-.mp4"
]

# Main FFmpeg stream to multicast
streamer = subprocess.Popen([
    "ffmpeg",
    "-re",
    "-f", "mpegts",
    "-i", "-",
    "-c", "copy",
    "-f", "rtp_mpegts",
    "-metadata", "service_name=Channel-Simulator-0.4",
    "-metadata", "service_provider=Channel-Simulator",
    "rtp://239.255.0.1:1234?pkt_size=1316"
], stdin=subprocess.PIPE)

try:
    while True:
        file = random.choice(playlist)
        print(f"Now playing: {file}")

        feeder_command = [
            "ffmpeg",
            "-re",
            "-i", file,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-g", "50",
            "-keyint_min", "25",
            "-sc_threshold", "0",
            "-b:v", "1500k",
            "-maxrate", "2000k",
            "-bufsize", "4000k",
            "-c:a", "copy",
            "-ar", "48000",
            "-f", "mpegts",
            "-"
        ]

        print("Feeder command being executed:")
        print(" ".join(feeder_command)) # This will show you the exact command string

        feeder = subprocess.Popen(feeder_command, stdout=streamer.stdin)

        feeder.wait()
except KeyboardInterrupt:
    print("Stopping stream...")
    streamer.stdin.close()
    streamer.wait()