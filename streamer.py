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
        "-map", "0:v:0",
        "-map", "0:a:0",
        "-f", "rtp_mpegts",
        "-metadata", "service_name=Channel-Simulator-0.4",
        "-metadata", "service_provider=Channel-Simulator",
        f"{protocol}://{ip}:{port}?pkt_size=1316"
    ], stdin=subprocess.PIPE)

    print("WELCOME TO CHANNEL SIMULATOR 0.4.0!")
    print("Your stream is now available at: " + protocol + "://" + ip + ":" + str(port))
    return streamer  # Return the streamer process

# PLAY VIDEO FUNCTION
def play_video(file, output_pipe,timestamp, resume=False):
    """Plays a single media file and pipes the MPEG-TS stream to the provided pipe. If a timestamp is provided, it will play until that timestamp. 
    If resume is True, it will resume playback from the provided timestamp."""
    try:
        if resume:
        # if resume is true echo that we are resume playback from the timestamp.
            print(f"Resuming Playback: {file}")
            print(f"[DEBUG] next timestamp is {timestamp}")
        else:
            # if resume is false echo that we are playing the video from the start until the timestamp
            print(f"Now playing: {file} from start until {timestamp}")

        # Prepare the ffmpeg command to feed the video file
        feeder = ["ffmpeg", "-re"]

        # if resume is false, try to start the video from the beginning
        if not resume:
            if timestamp:
                feeder += ["-to", str(timestamp)]

        # Otherwise, if resume is true, we will start the video from the timestamp
        else:
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
            "-c:a", "aac",
            "-b:a", "128k",
            "-ar", "48000",
            "-f", "mpegts",
            "-"
        ]

        process = subprocess.Popen(feeder, stdout=output_pipe, stderr=subprocess.DEVNULL)

        # Return the process object so the caller can monitor it
        return process

    except Exception as e:
        print(f"[!ERROR] An error occurred while playing video: {e}")
    except KeyboardInterrupt:
        print("Stream interrupted by user.")
        return None