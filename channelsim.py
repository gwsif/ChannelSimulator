# Channel Simulator 0.4.0
# Copyright 2025 Kevan Pledger
# A simple channel simulator that uses FFmpeg to stream media files over RTP.


# todo next: stop playing video at first timestamp and start the commercial break

import os
import subprocess
import config_parser
import streamer
import streamconfig
import random
import pathlib
import media_controller

# Track our commercial breaks
comm_break = 0

# welcome message
print("STARTING CHANNEL SIMULATOR 0.4.0...")

# Load the configuration settings
print("[DEBUG] Attempting to load main configuration file...")
raw_config = config_parser.parse_config("config.txt")
stream_config = streamconfig.StreamConfig(raw_config)

# Check if the main configuration file loaded successfully
if stream_config is None:
    print("[!ERROR] Configuration file not found or empty.")
    exit(1)

# otherwise, print success message
print("[SYSTEM] Primary config loaded successfully!")

# Check if the media configuration file loads successfully
print("[DEBUG] Attempting to load media configuration file...")
media = config_parser.parse_config("media.txt")

# Check if the media configuration file loaded successfully
if media is None:
    print("[!ERROR] Media configuration file not found or empty.")
    exit(1)

# otherwise, print success message
print("[SYSTEM] Media config loaded successfully!")

# Print system status and continue to main program
print("[SYSTEM] CONFIGS LOADED! Starting Channel Simulator...")
print("\n")

#############
# ENTRY MENU
while True:
    print("\nChannel Simulator 0.4.0")
    print("Copyright 2025 Kevan Pledger")
    print("1) START CHANNEL SIMULATOR")
    print("2) VIEW STREAM VIA FFPLAY") 
    print("3) RELOAD CONFIGURATION FROM FILE")
    print("4) EXIT")

    choice = input("Enter your choice: ")
    match choice:
        # Start Channel Simulator
        case "1":
            print("[DEBUG] Option (1) to start channel simulator selected")

            # Load the main configuration file
            print("[DEBUG] Attempting to load main configuration file...")
            raw_config = config_parser.parse_config("config.txt")
            stream_config = streamconfig.StreamConfig(raw_config)

            # Check if the main configuration file loaded successfully
            if stream_config is None:
                print("[!ERROR] Configuration file not found or empty.")
                break
            else:
                print("[SYSTEM] Primary config loaded successfully!")
            
            # Check if the media configuration file loads successfully
            print("[DEBUG] Attempting to load media configuration file...")
            media = config_parser.parse_config("media.txt")
            if media is None:
                print("[!ERROR] Media configuration file not found or empty.")
                break
            else:
                print("[SYSTEM] Media config loaded successfully!")

            print("[SYSTEM] CONFIGS LOADED")

            # Create the streamer process with the values from the config
            streamer_proc = streamer.startstream(
                stream_config.protocol,
                stream_config.ip,
                stream_config.port
            )

            ############
            # Choose a random video from the media dictionary
            active_video = media_controller.choose_random_video(media)
            print("[DEBUG] Active video chosen: " + str(active_video))

            # Get the timestamp for the chosen video file
            active_video_ts = media_controller.get_timestamps(active_video, comm_break)
            print("[DEBUG] Active video timestamp: " + str(active_video_ts))
        
            # Load the chosen video into the stream and, if its the start of the show
            #    (ie comm_break == 0), play it from the start and not the active_video_ts!
            
            if active_video_ts is None or comm_break == 0:
                print("[DEBUG] No timestamp found or this is the first commercial break, playing from start.")
                active_video_ts = None
            
            # Streamer will play from start if active_video_ts is None and comm_break is 0 but will
            #   play video if active_video_ts is not None AND comm_break is greater than 0 (meaning
            #   we are in a commercial break)
            streamer.play_video(active_video, streamer_proc.stdin, active_video_ts)

            # Advance the commercial break counter
            comm_break += 1

        # View stream via FFPLAY
        case "2":
            print("[DEBUG] Option (3) to view stream via FFPLAY selected")
            # Run ffplay command
            subprocess.run([
                "ffplay",
                stream_config.get_stream_url()
            ])

        # Reload the configuration from file
        case "3":
            print("[DEBUG] Option (3) to reload configuration from file selected")

            # Track if we have an error
            haserror = False

            # Issue the reload commands
            raw_config = config_parser.parse_config("config.txt")
            stream_config = streamconfig.StreamConfig(raw_config)

            if stream_config is None:
                print("[!ERROR] Configuration file not found or empty.")
                haserror = True
            else:
                print("[SYSTEM] Primary config reloaded successfully!")
            
            media = config_parser.parse_config("media.txt")
            if media is None:
                print("[!ERROR] Media configuration file not found or empty.")
                haserror = True
            else:
                print("[SYSTEM] Media config reloaded successfully!")

            # Check if we had an error
            if haserror:
                print("[!ERROR] One or more configuration files could not be reloaded!")

            # Otherwise, print success message
            print ("[SYSTEM] ALL CONFIGS RELOADED")

        # Exit the program
        case "4":
            print("[DEBUG] Option () to exit selected")
            break