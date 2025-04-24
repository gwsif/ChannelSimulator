# ChannelSimulator Version 0.4.0-alpha
# Copyright 2025 Kevan Pledger

# IMPORTS
import os
import subprocess
import config_parser
import streamer


# ENTRY MENU
while True:
    print("1) START CHANNEL SIMULATOR")
    print("2) RELOAD CONFIGURATION")
    print("3) PRINT CONFIGURATION")
    print("4) QUIT")

    choice = input("Enter your choice: ")
    match choice:
        # START CHANNEL SIMULATOR
        case "1":
            print("[DEBUG] We have chosen to start channel simulator")

            # Load the main configuration file
            print ("")
            configuration = config_parser.parse_config("config.txt")
            
            # Check if the main configuration file loaded successfully
            if configuration is None:
                print("[!ERROR] Configuration file not found or empty.")
                break
            else:
                print ("[SYSTEM] Primary config loaded successfully!")

            # Check if the media configuration file loads successfully
            media = config_parser.parse_config("media.txt")
            if media is None:
                print("[!ERROR] Media configuration file not found or empty.")
                break
            else:
                print ("[SYSTEM] Media config loaded successfully!")
            print ("CONFIGS LOADED")

            # Now start the stream with the values
            stream_process = streamer.startstream(configuration["protocol"], configuration["ip"], configuration["port"])
            print ("[SYSTEM] Stream pipe built successfully!")

            # Choose a video from our key:value store (here for now)
            index = 0
            while index < len(media):
                active_video = media["video" + str(index)]
                index += 1

            print ("MEDIA CHOSEN:" + str(active_video))

            # load videos into the stream
            streamer.play_media(active_video, stream_process.stdin)
            print ("MEDIA LOADED")

        # RELOAD THE CONFIGURATION
        case "2":
            print("we have chosen to reload the configuration")
            # Issue reload command
            configuration = config_parser.parse_config("config.txt")
            media = config_parser.parse_config("media.txt")

        # PRINT THE CONFIGURATION    
        case "3":
            print("we have chosen to print the configuration")
            # Print the current configuration key:value stores
            print("CURRENT PRIMARY CONFIG:")
            print(configuration)
            print("CURRENT MEDIA CONFIG:")
            print(media)

        case "4":
            print("Exiting Channel Simulator...")
            # say goodbye!
            break
        case _:
            print("Invalid choice, please try again!")