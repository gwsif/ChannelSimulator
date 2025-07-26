#streamer.py
import subprocess

streamer = None  # Global variable to hold the streamer process

# START STREAM FUNCTION
def startstream(protocol, ip, port):
    streamer = subprocess.Popen([
        "ffmpeg",
        "-re",
        "-f", "mpegts",
        "-i", "-",
        "-c", "copy",
        "-f", "rtp_mpegts",
        "-metadata", "service_name=Channel-Simulator-0.4",
        "-metadata", "service_provider=Channel-Simulator",
        f"{protocol}://{ip}:{port}?pkt_size=1316"
    ], stdin=subprocess.PIPE)

    print("WELCOME TO CHANNEL SIMULATOR 0.4.0!")
    print("Your stream is now available at: " + protocol + "://" + ip + ":" + str(port))
    return streamer  # Return the streamer process

def play_video(file, output_pipe,timestamp):
    """Plays a single media file and pipes the MPEG-TS stream to the provided pipe."""
    try:
        print(f"Now playing: {file}")

        # Prepare the ffmpeg command to feed the video file
        feeder = ["ffmpeg", "-re"]

        # if timestamp is provided, use it to seek to the correct position
        if timestamp:
            feeder += ["-ss", str(timestamp)]

        # Add the rest of the ffmpeg command
        feeder += [
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

        # Execute the feeder command
        feeder = subprocess.Popen(feeder, stdout=output_pipe, stderr=subprocess.PIPE)
        _, err = feeder_proc.communicate()
        print(err.decode())
        
        if feeder.returncode != 0:
            print(f"[!ERROR] Feeder process failed with return code {feeder.returncode}")

    except Exception as e:
        print(f"[!ERROR] An error occurred while playing video: {e}")
    except KeyboardInterrupt:
        print("Stream interrupted by user.")