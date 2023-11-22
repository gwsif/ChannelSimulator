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

# Setting variables
xvfb_process = None
i3_process = None
cs_comm_min = 5 # minimum number of commercials TODO move this to config file
cs_comm_max = 9 # maximum number of commercials TODO move this to config file
cs_show_path = "" # Filepath for folder containing episodes, TODO move this to config file
cs_comm_path = "" # Filepath for folder containing commercials TODO move this to config file

# Starts the display
    # Start Xvfb and i3 within the same 'with' block
def start_display():
    with open('/dev/null', 'w') as f:
        xvfb_process = subprocess.Popen(["nohup", "Xvfb", ":100", "-screen", "0", "1920x1080x24"], stdout=f, stderr=subprocess.STDOUT)

        # Wait for Xvfb to start
        time.sleep(1)

        # Set the DISPLAY environment variable
        os.environ["DISPLAY"] = ":100"

        # Start i3 window manager
        i3_process = subprocess.Popen(["i3", "-c" "/channelsim-i3-configuration.cfg"], stdout=f, stderr=subprocess.STDOUT)

        # Start ffmpeg stream
        ffmpeg_process = subprocess.Popen(["./csstream.sh", "1920", "1080", ":100", "5000"], stdout=f, stderr=subprocess.STDOUT)

# Runs a menu
def show_menu():
    print("CHANNELSIMULATOR::.")
    print("1) Local simulation")
    print("2) Headless simulation")
    print("3) Cleanup processes")
    print("4) Exit")

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
    # Scan the show filepath and fill an array with the file names
    # Generate a random number between 1 and the max number of files in the array
    # Play the episode using csplay.sh (# $1 = Expected Runtime, # $2 = Expected Filepath, # $3 = Expected Mediaplayer)    
    pass

# Plays commercials/gapless content on a back-to-back basis
def play_secondary_content():
    # TODO;;
    # Scan the commercial filepath and fill an array with the file names
    # Generate a random number between cs_comm_min and cs_comm_max
    # Enter a loop, while we are less than our random number
    # Generate a random number between 1 and the max number of files in the array
    # Play the commercial using csplay.sh (# $1 = Expected Runtime, # $2 = Expected Filepath, # $3 = Expected Mediaplayer)   
    pass

# Run show menu and define the options
show_menu()
option = int(input("Enter number choice: "))

# So long as the user hasn't entered the exit option, do menu stuff
while option != 4:
    if option == 1:
        # do option 1 stuff
        print("Option 1 has been called.")
    elif option == 2:
        # do option 2 stuff
        print("Option 2 has been called.")
        print("Starting virtual display...")
        start_display()
    elif option == 3:
        # do option 3 stuff
        print("Option 3 has been called.")
        #print("for now manually run 'sudo killall i3 Xvfb'")

        #subprocess.run(['sudo', 'killall', 'Xvfb', 'i3'], check=False)
        kill_process('Xvfb')
        kill_process('i3')
        kill_process('ffmpeg')
        kill_process('nc')
        
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



