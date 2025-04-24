import subprocess
import random

def startstream(protocol,ip,port):
    # Main FFmpeg stream to multicast
    streamer = subprocess.Popen([
        "ffmpeg",
        "-re",
        "-f", "mpegts",
        "-i", "-",
        "-c", "copy",
        "-f", "mpegts",
        f"udp://{ip}:{port}?pkt_size=1316"
    ], stdin=subprocess.PIPE)

    print("Stream started. Avalable on: " + protocol + "://" + ip + ":" + str(port))
    return streamer  # Return the streamer process

def play_media(file, output_pipe):
    """Plays a single media file and pipes the MPEG-TS stream to the provided pipe."""
    try:
        while True:
            print(f"Now playing: {file}")

            feeder = subprocess.Popen([
                "ffmpeg",
                "-re",
                "-i", file,
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "23",
                "-maxrate", "1200k",
                "-bufsize", "2400k",
                "-c:a", "mp2",
                "-b:a", "128k",
                "-ar", "44100",
                "-f", "mpegts",
                "-"
            ], stdout=output_pipe, stderr=subprocess.PIPE)

            feeder.wait()
            if feeder.returncode != 0:
                print(f"FFmpeg (feeder) exited with code: {feeder.returncode}")

            # Optional delay before playing the same video again
            # time.sleep(1)

    except BrokenPipeError:
        print("Stream pipe closed.")
    except KeyboardInterrupt:
        print("Stopping media player.")