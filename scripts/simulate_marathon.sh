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
    #    We can use this idea to select multiple shows!

# ALWAYS SOURCE OUR CONFIG
source config/channel_simulator.cfg

# BEGIN PROGRAM LOOP
while true;
    do
        # PLAY OUR SHOW  
        scripts/play_show.sh "$TEST_DIR"

        # RUN SOME COMMERCIALS!
        scripts/play_commercials,sh
    done