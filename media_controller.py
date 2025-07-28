# media_controller

import os
import subprocess
import config_parser
import streamer
import streamconfig
import random
import pathlib


def choose_random_video(media):
    """Selects a random video from the media configuration."""

    if not media:
        print("[!ERROR] Media configuration is empty or not provided.")
        return None

    video_paths = list(media.values())

    if not video_paths:
        print("[!ERROR] No videos found in the media configuration.")
        return None
    
    # Choose a random video from the list
    chosen_video = random.choice(video_paths)
    print("[SYSTEM] MEDIA CHOSEN: " + str(chosen_video))
    
    return str(chosen_video)

def get_timestamps(videofile, comm_break):
    """Retrieves the timestamp for the specified commercial break in the video file."""
    
    # Initialize an empty dictionary to hold timestamps
    active_video_timestamps = {}

    # Build our string for the active video timestamp file path if it exists
    active_video_ts_file = pathlib.Path(os.path.splitext(videofile)[0] + ".csv")
    
    # Check to see if timestamps file exists
    if active_video_ts_file.exists():

        # Config file exists, so we can load the timestamps
        print("[SYSTEM] FOUND timestamp file for current video:")
        print("[DEBUG] TS file found at " + str(active_video_ts_file))
        
        # get the timestamps of the chosen video
        active_video_timestamps = config_parser.parse_timestamps(str(active_video_ts_file))
        
        return str(active_video_timestamps[comm_break])
    
    # Debug message if the timestamp file does not exist
    #print("[!ERROR] Ran get_timestamps but timestamp file does not exist for the current video.")
    #print("[!ERROR] Tried to use." + str(active_video_ts_file))
    #print("[!ERROR] Got " + str(active_video_timestamps[comm_break]) + " as the timestamp.")
    return None
    
    
def play_video(videofile, timestamp=None):
    """Plays the provided video file using the streamer."""
    
    comm_break = 0  # Default commercial break index

    # Check to see if timestamps file exists
    active_video_ts_file = pathlib.Path(os.path.splitext(videofile["videos"][0])[0] + ".csv")
    if active_video_ts_file.exists():
        # Config file exists, so we can load the timestamps
        print("[SYSTEM] FOUND timestamp file for current video:")
        print("[DEBUG] TS file found at " + str(active_video_ts_file))

        # Get the timestamps of the chosen video
        active_video_timestamps = config_parser.parse_timestamps(str(active_video_ts_file))

        # Set our timestamp to the corresponding commercial break in the list
        if comm_break <= len(active_video_timestamps):
            timestamp = active_video_timestamps[comm_break]
            print("[DEBUG] Current timestamp chosen for video now playing: " + str(timestamp))

    # Load the chosen video into the stream
    streamer.play_video(media["videos"][0], streamer.streamer.stdin, timestamp)

    return None

def play_advertisements(adslist):
#todo make it play a random number of commercials pulled from an ads list

    return None