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
import time
import sys

# Track our commercial breaks
comm_break = 0
resume = False  # Flag to indicate if we are resuming playback

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
print("--------------------------------------------------------")

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
            
            # --- CONFIG CHECKS ---
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

            # Check if commercials configuration file loads successfully
            commercials = config_parser.parse_list_of_files("commercials.txt")
            if commercials is None:
                print("[!ERROR] Commercials configuration file not found or empty.")
                break
            else:
                print("[SYSTEM] Commercials config loaded successfully!")

            print("[SYSTEM] CONFIGS LOADED")
            # --- CONFIG CHECKS END ---
            # --------------------------
            # --- MAIN PROGRAM BEGINS ---
            # Create the streamer process with the values from the config
            streamer_proc = streamer.startstream(
                stream_config.protocol,
                stream_config.ip,
                stream_config.port
            )

            # Choose a random video from the media dictionary
            active_video = media_controller.choose_random_video(media)
            print("[DEBUG] Active video chosen: " + str(active_video))

            # Get the timestamp for the chosen video file
            active_video_ts = media_controller.get_timestamps(active_video, comm_break)
            print("[DEBUG] Active video timestamp: " + str(active_video_ts))           

            # if the active_video_ts is none then we have no timestamps so set comm_break to -1 to indicate it
            if active_video_ts is None:
                print("[SYSTEM] No timestamp file found for current video. Playing from start.")
                comm_break = -1
                
                # Debug message
                print("[DEBUG] channelsim.py comm_break value is " + str(comm_break))

            # if comm_break is 0 then play from start up to first time stamp
            if comm_break == 0:
                print("[SYSTEM] Timestamp loaded. Playing from start to first alloted timestamp.")

            # Start the video stream with the first video and timestamp (if any)
            chansim_stream_proc = streamer.play_video(active_video, streamer_proc.stdin, active_video_ts) 
           
            # Check if the stream process was created successfully
            if chansim_stream_proc is None:
                print("[!ERROR] Failed to start the video stream process.")
                break

            # Enter continuous loop to keep stream alive
            try:
                while True:
                    # Check if the currrent video process has finished
                    # .poll() returns None if the process is still running
                    if chansim_stream_proc.poll() is not None:
                        # if we see none then video is finished, load new.
                        print("[SYSTEM] Detected end of a video's playback. Loading next video...")

                        # Increment the commercial break counter
                        comm_break += 1

                        # sleep for a moment to avoid weirdness
                        time.sleep(0.25)

                        # Grab our list of commercials to play.
                        list_of_ads = media_controller.gen_ads_w_bounds(
                            commercials,
                            max_ads=5,
                            min_ads=1,
                            max_duration=60
                        )

                        # For every ad in our list of ads, play it.
                        for ad in list_of_ads:
                            print("[SYSTEM] Now playing commercial: " + str(ad))
                            ad_process = streamer.play_video(ad, streamer_proc.stdin, None)

                            # Wait for the ad process to finish
                            ad_process.wait()
                            print("[SYSTEM] Commercial block finished.")

                        # After commercials, evaluate where to go next
                        # if the commercial break counter is less than the number of timestamps we have then assume no
                        # more commercial breaks are available and we need to load a new video.
                        if comm_break < len(active_video_ts):
                            # If there are more timestamps, get the next timestamp
                            active_video_ts = media_controller.get_timestamps(active_video, comm_break)
                            print("[DEBUG] Next timestamp for commercial break: " + str(active_video_ts))
                            resume = True  # Set resume to True to continue from the next timestamp
                        else:
                            # If no more timestamps, choose a new video
                            print("[SYSTEM] No more timestamps available. Choosing a new video.")
                            active_video = media_controller.choose_random_video(media)
                            print("[DEBUG] New active video chosen: " + str(active_video))
                            active_video_ts = media_controller.get_timestamps(active_video, comm_break)
                            print("[DEBUG] New active video timestamp: " + str(active_video_ts))
                            resume = False  # Reset resume to False for the new video

                        # Sleep for a moment to avoid busy waiting
                        time.sleep(1)  

                        # Load the new video and start streaming it and monitoring it.
                        chansim_stream_proc = streamer.play_video(active_video, streamer_proc.stdin, active_video_ts, resume) 


            except KeyboardInterrupt:
                print("[SYSTEM] Stream interrupted by user. Exiting...")
                if chansim_stream_proc and chansim_stream_proc.poll() is None:
                    chansim_stream_proc.terminate()  # Terminate the stream process if it's still running
                if streamer_proc and streamer_proc.poll() is None:
                    streamer_proc.terminate()
                break # Exit the loop after clean-up

            # Streamer is programmed to play from start if active_video_ts is None and comm_break is 0 but will
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