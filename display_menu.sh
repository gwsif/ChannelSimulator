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
echo "::::::::::::::::::::::::::::::::::::::::::::::::::::"

# ALWAYS SOURCE OUR CONFIG FIRST
source ""$1"/channel_simulator.cfg"

# DEBUG ECHOES
#echo "[INFO] FOUND CS CONFIG FILEPATH AT:$CS_CONFIG_FILE"

# BEGIN MENU
echo "SELECT AN OPTION PLEASE:"
select MENU_OPTION in "Start Headless Stream" "Stop Headless Stream" "Run ChannelSim" "Quit"
do
	case $MENU_OPTION in
		"Start Headless Stream")

		    # CHECK IF DISPLAY IS OPEN
		    CS_XVFB_STATUS=$(xdpyinfo -display :100 >/dev/null 2>&1 && echo "open" || echo "closed")

		    # IF XVFB DISPLAY IS NOT OPEN THEN START IT
			if [ ! "$CS_XVFB_STATUS" == "open" ]; 
			then
				# RUN THE COMMAND TO START THE HEADLESS DISPLAY
				nohup Xvfb $CS_XVFB_DISPLAY_NUM -screen 0 "${CS_XVFB_RES_WIDTH}x${CS_XVFB_RES_HEIGHT}x${CS_XVFB_COL_DEPTH}" > /dev/null 2>&1 &


			else
				echo "Xvfb on display $CS_XVFB_DISPLAY_NUM is already open!"
			fi

			# IF THIS HAS VARIABLE HAS DATA, WE HAVE AN OPEN STREAM!
			CS_STREAM_ALIVE="$(lsof -i :5000)"

			# IF THE THE STREAM VARIABLE IS EMPTY OR UNSET THEN THE STREAM IS NOT OPEN
			if [ -z "$CS_STREAM_ALIVE" ];
			then
				# SCREEN OPEN SO START FFMPEG STREAM IN THE BACKGROUND
				nohup ffmpeg -f x11grab -framerate 30 -video_size "${CS_XVFB_RES_WIDTH}x${CS_XVFB_RES_HEIGHT}" -i :100 -f pulse -i default -c:v libx264 -preset fast -maxrate 2500k -bufsize 5000k -g 60 -vf format=yuv420p -c:a aac -b:a 128k -f avi - | nc -lp $CS_NC_PORT > /dev/null 2>&1 &
			else
				# THE STREAM IS ALREADY OPEN SO ANNOUNCE TO CONSOLE!
				echo "[INFO] FFMPEG STREAM ALREADY RUNNING"
				echo "[INFO] CHECK USING (lsof -i $CS_NC_PORT)"
			fi
			;;

		"Stop Headless Stream")
			echo "$MENU_OPTION - Stop Headless Stream"

		    # CHECK IF DISPLAY IS OPEN
		    CS_XVFB_STATUS="$(xdpyinfo -display $CS_XVFB_DISPLAY_NUM >/dev/null 2>&1 && echo "open" || echo "closed")"

			# CHECK IF STREAM IS OPEN
			CS_NC_PID="$(pgrep -x "nc")"

		    # STOP XVFB IF DISPLAY IS OPEN
			#    NOTE: PKILL ON NC HERE MIGHT THROW ISSUES IF MORE THAN ONE PID IS PRESENT!
			if [[ "$CS_XVFB_STATUS" == "open" ]]; 
			then
				#sh -c $CS_XVFB_DISPLAY_NUM 'sudo pkill -f $1'
				#echo "we doing: pkill -f "Xvfb $CS_XVFB_DISPLAY_NUM""
				#echo "we doing: kill -9 "$CS_NC_PID""
        		sudo pkill -f "Xvfb $CS_XVFB_DISPLAY_NUM"
				sudo kill -9 "$CS_NC_PID"
				
				# IF FFMPEG IS STILL RUNNING, KILL IT
				sudo pkill -f ffmpeg

				# ANNOUNCE TO CONSOLE
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