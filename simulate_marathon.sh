#!/bin/bash
# ::::::::::::::::::::::::::::::::::::::::::::.
# C H A N N E L  S I M U L A T O R
# `````````````````````````````````````````````
# TELEVISION BROADCAST SIMULATOR
# ©KEVAN PLEDGER 2023
# ::::::::::::::::::::::::::::::::::::::::::::.
#
# SIMULATE MARATHON
#    SIMULATES A TELEVISED SERIES MARATHON. THIS CAN BE SET TO SEQUENTIAL MODE WHERE SHOWS WILL PLAY AND RESPECT THEIR EPISODIC ORDER
#    OR NONSEQUENTIAL MODE WHERE EPISODES OF THE SHOW WILL PLAY RANDOMLY. DURING COMMERCIAL BREAKS (IF A CSBREAK FILE IS PRESENT) AND/OR
#    AFTER EPISODES, THE COMMERCIALS FUNCTION IS RUN TO PLAY SOME COMMERCIALS BEFORE RETURNING TO PLAY THE EPISODE.

    # Idea here is that we will send the link of the show we want to play to
    #    play_show as parameter 1, for example we will call
    #       play_show $CS_SHOW_DIR 
    #    the function should then pass $CS_SHOW_DIR as $1 parameter to play_show function!!!
    #    We can

# TRAP CTRL-C FOR CLEANUP WHEN WE STOP
trap ctrl_c INT

# TRAP CTRL-C FOR CLEANUP WHEN WE STOP
function ctrl_c() {
    # IF CTRL+C COMBO IS DETECTED THEN USER WISHES TO QUIT
    echo "---------------------------------- ALERT ----------------------------------"
    echo "[INFO] CHANNELSIMULATOR WAS TOLD TO QUIT SO QUITTING!"
    echo "[INFO] PASSWORD MAY BE REQUIRED TO FULLY TERMINATE THE HEADLESS DISPLAY!"


    # KILL XVFB FFMPEG, & VLC. i3 GOES WITH XVFB AUTOMATICALLY
    sh -c "sudo killall Xvfb vlc ffmpeg"

    # ANNOUNCE EXIT TO CONSOLE
    echo "---CHANNEL SIMULATOR HAS EXITED---"
    exit 0
}

# ANNOUNCE SCRIPT EXECUTION
echo "[INFO] simulate_marathon.sh executing..."

# ALWAYS SOURCE OUR CONFIG
source ""$1"/channel_simulator.cfg"

# BEGIN PROGRAM LOOP
while true;
    do
        # PLAY OUR SHOW
        # PASS INSTALL PATH AS FIRST ARG!
        ./play_show.sh "$1"

        # RUN SOME COMMERCIALS
        #    PASS INSTALL PATH AS FIRST ARG!
        ./play_commercials.sh "$1"
    done