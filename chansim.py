# *****************************************************************************
# CHANNELSIMULATOR
# Copyright (C) 2023 Kevan Pledger
# *****************************************************************************
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
# ****************************************************************************

# Imports
import os
import subprocess
import time
import random
import math
from pymediainfo import MediaInfo

# Setting variables
xvfb_process = None
i3_process = None
cs_mediaplayer = "vlc"
cs_comm_min = 5 # minimum number of commercials TODO move this to config file
cs_comm_max = 9 # maximum number of commercials TODO move this to config file
cs_show_path = "/mnt/Shows/Cow and Chicken/" # Filepath for folder containing episodes, TODO move this to config file
cs_comm_path = "/mnt/Commercials/90s" # Filepath for folder containing commercials TODO move this to config file
cs_headless_res_width = 800 # Headless display resolution width TODO move this to config file
cs_headless_res_height = 600 # Headless display resolution height TODO move this to config file
cs_headles_col_depth = 24 # Headless display color depth (rec 24) TODO move this to config file
cs_headless_disp_num = ":100"
cs_headless_port_num = 8080

# Starts the display
    # Start Xvfb and i3 within the same 'with' block
def start_display():
    with open('/dev/null', 'w') as f:
        #xvfb_process = subprocess.Popen(["nohup", "Xvfb", ":100", "-screen", "0", "1920x1080x24"], stdout=f, stderr=subprocess.STDOUT)
        xvfb_process = subprocess.Popen(["nohup", "Xvfb", ":100", "-screen", "0", str(cs_headless_res_width) + "x" + str(cs_headless_res_height) + "x" + str(cs_headles_col_depth)], stdout=f, stderr=subprocess.STDOUT)

        # Wait for Xvfb to start
        print("[INFO] Pausing for Xvfb...")
        time.sleep(2)

        # Set the DISPLAY environment variable
        os.environ["DISPLAY"] = ":100"
        os.environ["I3SOCK"] = f"{os.environ['HOME']}/.i3/ipc-100"

        # binggpt
        env = os.environ.copy()
        env["DISPLAY"] = ":100"

        # Start i3 window manager
        this_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(this_dir, "channelsim-i3-configuration.cfg")
        i3_cmd = f'DISPLAY=:100 nohup i3 -c {config_path} > i3_stdout.log 2>&1 &'
        subprocess.Popen(i3_cmd, shell=True, preexec_fn=os.setpgrp)
        
        # Debug echoes
        print("[DEBUG] Detected config directory as: ", str(this_dir))
        print ("[DEBUG] Set absolute config path as: ", str(config_path))

        # Wait for i3 setup
        print("[INFO] Pausing for i3...")
        time.sleep(2)

        # Debug echoes
        print("[INFO] Launching stream...")
        # Start ffmpeg stream
        ffmpeg_process = subprocess.Popen(["./csstream.sh", str(cs_headless_res_width), str(cs_headless_res_height), str(cs_headless_disp_num), str(cs_headless_port_num)], stdout=f, stderr=subprocess.STDOUT)

# Restarts the stream
def restart_stream():
    # Start the ffmpeg stream
    ffmpeg_process = subprocess.Popen(["./csstream.sh", str(cs_headless_res_width), str(cs_headless_res_height), str(cs_headless_disp_num), str(cs_headless_port_num)], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

# Runs a menu
def show_menu():
    print("CHANNELSIMULATOR::.")
    print("1) Local simulation")
    print("2) Headless simulation")
    print("3) Cleanup processes")
    print("4) Restart stream")
    print("5) Exit")

# BingGPT function
def kill_process(process_name):
    try:
        subprocess.run(['sudo', 'killall', process_name], check=False)
        time.sleep(1)  # wait for a bit to allow the process to terminate
        if process_name in (line.split()[-1] for line in os.popen('ps aux')):
            subprocess.run(['sudo', 'killall', '-s', '9', process_name], check=False)  # send SIGKILL if the process is still running
        print(f"Killed all processes named {process_name}")
    except subprocess.CalledProcessError:
        print(f"Failed to kill processes named {process_name}")

# Plays a show/movie/non-commercial contnet
def play_primary_content():
    # TODO;;
    # Scan the show filepath (cs_show_path) and fill an array with the file names
    primary_files_list = os.listdir(cs_show_path)

    # Generate a random number between 1 and the max number of files in the array
    #chosen_seed = random.randrange(cs_comm_min, cs_comm_max, 1) #TODO FIX THIS!!!!
    chosen_seed = random.randrange(0, len(primary_files_list))

    # Assign our chosen episode
    chosen_filepath = primary_files_list[chosen_seed]
    #abs_chosen_filepath = os.path.abspath(chosen_filepath)
    abs_chosen_filepath = os.path.abspath(os.path.join(cs_show_path, chosen_filepath))
    print("[INFO] Chose file: " + abs_chosen_filepath)

    # Get the runtime of the chosen episode
    media_info = MediaInfo.parse(abs_chosen_filepath)
    chosen_duration_ms = media_info.tracks[0].duration
    chosen_duration_s = math.ceil(chosen_duration_ms / 1000) # turn ms to seconds
    print("[INFO] Determined Runtime: " + str(chosen_duration_s) + "s")

    # Play the episode using csplay.sh (# $1 = Expected Runtime, # $2 = Expected Filepath, # $3 = Expected Mediaplayer)
    play_process = subprocess.Popen(["./csplay.sh", str(chosen_duration_s), str(abs_chosen_filepath), str(cs_mediaplayer)], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

# Plays commercials/gapless content on a back-to-back basis
def play_secondary_content():
    # TODO;;
    # Scan the commercial filepath (cs_comm_path) and fill an array with the file names
    commercial_files_list = os.listdir(cs_comm_path)
    # Generate a random number between cs_comm_min and cs_comm_max
    # Enter a loop, while we are less than our random number
    # Generate a random number between 1 and the max number of files in the array
    # Get the runtime  of the commercial we chose
    # Play the commercial using csplay.sh (# $1 = Expected Runtime, # $2 = Expected Filepath, # $3 = Expected Mediaplayer)   
    pass

# Run show menu and define the options
show_menu()
option = int(input("Enter number choice: "))

# So long as the user hasn't entered the exit option, do menu stuff
while option != 5:
    if option == 1:
        # do option 1 stuff
        print("Option 1 has been called.")
    elif option == 2:
        # do option 2 stuff
        print("Option 2 has been called.")
        print("Starting virtual display...")
        
        # Start the headless display
        start_display()

        # Pause and announce status to console
        print ("[INFO] Waiting for display...")
        time.sleep(1)

        # Start the playback of primary content
        print ("[INFO] Beginning playback...")
        play_primary_content()

    elif option == 3:
        # do option 3 stuff
        print("Option 3 has been called.")
        #print("for now manually run 'sudo killall i3 Xvfb'")

        #subprocess.run(['sudo', 'killall', 'Xvfb', 'i3'], check=False)
        kill_process('Xvfb')
        kill_process('i3')
        kill_process('ffmpeg')
        kill_process('nc')

    elif option == 4:
        # restart the stream
        restart_stream()
        
    else:
        # Any other option is bad
        print("Invalid option.")

    # print for space
    print()

    # show the menu
    show_menu()

    # ask for options again
    option = int(input("Enter your option: "))

# Tell console we are shutting down
print("CHANNELSIMULATOR IS SHUTTING DOWN.")



