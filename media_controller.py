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
        
        # if we have another timestamp to use, then return it
        if comm_break < len(active_video_timestamps):
            return str(active_video_timestamps[comm_break])
        else:
            # we assume that no next timestamp exists so return None.
            return None
    
    # Debug message if the timestamp file does not exist
    #print("[!ERROR] Ran get_timestamps but timestamp file does not exist for the current video.")
    #print("[!ERROR] Tried to use." + str(active_video_ts_file))
    #print("[!ERROR] Got " + str(active_video_timestamps[comm_break]) + " as the timestamp.")
    return None

# Takes a list of video files representing commercial advertisements, a maximumn number of ads to play,
#    a minimum number of ads to play, and a maximum duration for the ads segment. Defaults to 5 ads, 
#    1 min duration, and 1 ad minimum. 
def gen_ads_w_bounds(media, max_ads=5, min_ads=1, max_duration=60):
#todo make it play a random number of commercials pulled from an ads list
    """Generates a list of ads to play based on the provided parameters."""
    # this function will look at a list of video files on a .txt file and 
    # choose a random number of them based on a maximum duration creterion
    # SCOPE CHECK: IT WILL NOT PLAY THE VIDEO FILES, JUST GENERATE A LIST OF THEM!
    if not media:
        print("[!ERROR] Media configuration for ads list is empty or not provided.")
        return None

    video_paths = list(media)

    if not video_paths:
        print("[!ERROR] No videos found in the ads list media configuration.")
        return None
    
    # Randomly choose a number of ads to play within the specified bounds (note duration is not actually checked here at the moment!!!!)
    num_ads = random.randint(min_ads, max_ads)
    print(f"[DEBUG] Generating {num_ads} ads from the list with a maximum duration of {max_duration} seconds.")
    list_of_ads = random.sample(video_paths, num_ads)
    print("[DEBUG] Generated ads list: " + str(list_of_ads))

    # Return the list of ads
    if not list_of_ads:
        print("[!ERROR] No ads were generated. Check the media configuration.")
        return None
    return list_of_ads