#!/bin/bash
# ::::::::::::::::::::::::::::::::::::::::::::.
# C H A N N E L  S I M U L A T O R
# `````````````````````````````````````````````
# TELEVISION BROADCAST SIMULATOR
# ©KEVAN PLEDGER 2023
# ::::::::::::::::::::::::::::::::::::::::::::.
#
# MENU
#    SIMPLE USER MENU WHICH ASKS FOR INPUT. USERS ARE REQUIRED TO SELECT MENU OPTION 1 ON FIRST RUN ANYTIME A NEW
#    TTY SESSION IS STARTED! USERS ARE ALSO REQUIRED TO HAVE A CONFIG FILE IN THE SAME DIRECTORY AS THIS SCRIPT!
#-----------------------------------------------------------------------------------------------

# ALWAYS SOURCE OUR CONFIG
source config/channel_simulator.cfg

# BEGIN MENU
echo "SELECT AN OPTION PLEASE:"
select MENU_OPTION in "Add/Refresh Directories" "Run ChannelSim" "Quit"
do
   case $MENU_OPTION in
	   "Add/Refresh Directories")
		   echo "$MENU_OPTION - Add/Refresh Directories"
           # SCAN THE CONFIG FILE
		   scripts/scan_config.sh
           echo "VALUE OF CS_CONFIG_FILE IS: $CS_CONFIG_FILE"
		   ;;
	   "Run ChannelSim")
		   echo "$MENU_OPTION - Run ChannelSim"
		   # SIMULATE MARATHON
           scripts/simulate_marathon.sh
		   ;;
	   "Quit")
		   echo "$MENU_OPTION - Quit"
		   break;;
	   *)
		   echo "Not a valid option";;
   esac
done
