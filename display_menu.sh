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
# -----------------------------------------------------------------------------------------------

# ANNOUNCE SCRIPT EXECUTION
echo "[INFO] display_menu.sh executing..."

# ALWAYS SOURCE OUR CONFIG FIRST
source ""$1"/channel_simulator.cfg"

# DEBUG ECHOES
echo "in display menu value of CS CONFIG FILE IS: $CS_CONFIG_FILE"

# BEGIN MENU
echo "SELECT AN OPTION PLEASE:"
select MENU_OPTION in "Start Headless Stream" "Stop Headless Stream" "Run ChannelSim" "Quit"
do
	case $MENU_OPTION in
		"Start Headless Stream")
		    # CHECK IF DISPLAY IS OPEN
		    CS_XVFB_STATUS=$(xdpyinfo -display :100 >/dev/null 2>&1 && echo "open" || echo "closed")

		    # Start Xvfb if the display is not open
			if [ ! "$CS_XVFB_STATUS" == "open" ]; 
			then
				# NEED TO INVOKE XVFB WITH ROOT SO WE PROMPT USER!
				#if [ $(id -u) != 0 ];
				#then
				#	echo "ROOT PRIVILEGES ARE REQUIRED TO CREATE VIRTUAL DISPLAY!"
				#	sudo -b -E Xvfb $CS_XVFB_DISPLAY_NUM -screen 0 "${CS_XVFB_RES_WIDTH}x${CS_XVFB_RES_HEIGHT}x${CS_XVFB_COL_DEPTH}"
				#	
				#	# SLEEP 1s TO ALLOW FOR XVFB SETUP
				#	sleep 1
				#fi
				#
				# NOW START FFMPEG STREAM IN THE BACKGROUND
				# this causes an infinite loop/memory leak. BAD!
				#while true;
				#do
				#	ffmpeg -f x11grab -framerate 30 -video_size "${CS_XVFB_RES_WIDTH}x${CS_XVFB_RES_HEIGHT}" -i :100 -f pulse -i default -c:v libx264 -preset fast -maxrate 2500k -bufsize 5000k -g 60 -vf format=yuv420p -c:a aac -b:a 128k -f avi - | nc -lp 5000 &
				#done &
			
				# ANNOUNCE CHANGE TO CONSOLE
				echo "XVFB DISPLAY $CS_XVFB_DISPLAY_NUM LAUNCHED!"
			else
				echo "Xvfb on display $CS_XVFB_DISPLAY_NUM is already open!"
			fi			
			;;
		"Stop Headless Stream")
			echo "$MENU_OPTION - Stop Headless Stream"

		    # CHECK IF DISPLAY IS OPEN
		    CS_XVFB_STATUS=$(xdpyinfo -display :100 >/dev/null 2>&1 && echo "open" || echo "closed")

		    # STOP XVFB IF DISPLAY IS OPEN
			if [ "$CS_XVFB_STATUS" == "open" ]; 
			then
        		sudo pkill -f "Xvfb $CS_XVFB_DISPLAY_NUM"
				echo "XVFB DISPLAY $CS_XVFB_DISPLAY_NUM TERMINATED"
			else
				echo "Xvfb on display $CS_XVFB_DISPLAY_NUM is already closed."
			fi
			;;
	   "Run ChannelSim")
			echo "$MENU_OPTION - Run ChannelSim"

			# SIMULATE MARATHON AND PASS INSTALL DIRECTORY
			./simulate_marathon.sh "$1"
			;;
	   "Quit")
			echo "$MENU_OPTION - Quit"
			break;;
	   *)
		   echo "Not a valid option";;
   esac
done
