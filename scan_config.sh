#!/bin/bash
# ::::::::::::::::::::::::::::::::::::::::::::.
# C H A N N E L  S I M U L A T O R
# `````````````````````````````````````````````
# TELEVISION BROADCAST SIMULATOR
# ©KEVAN PLEDGER 2023
# ::::::::::::::::::::::::::::::::::::::::::::.
#
# CONFIGURATION LOADER SCRIPT
#    LOADS CONFIGURATION FILES FROM ~/config AND SETS ENVIRONMENT
# VARIABLES NECESSARY FOR THE OPERATION OF CHANNEL SIMULATOR!
# ---------------------------------------------------------------------

# CHANGE DIRECTORIES BACK TO CHANSIM
cd $HOME/ChannelSimulator

# ANNOUNCE STATE CHANGE TO CONSOLE
echo "---READING CONFIGURATION FILE---"

# CHECK FOR EXISTENCE OF CONFIG FILE!
if ! test -f channel_simulator.cfg;
	then
		echo "MISSING OR INVALID CONFIGURATION FILE!"
	else

		# SOURCE CONFIG HERE - ONLY EXCEPTION
		source channel_simulator.cfg

		# ANNOUNCE DISCOVERY OF CONFIG FILE
		echo "CHANNEL SIM CONFIG FILE FOUND AT:"
		echo "$CS_CONFIG_FILE"

		# ANNOUNCE DETECTIONS
		echo "MODE SELECTION: $CS_MODE"
        echo "MEDIA PLAYER: $CS_MEDIAPLAYER"
		echo "COMMERCIAL DIR: $CS_COMM_DIR"
		echo "COMMERCIAL MIN: $CS_COMM_MIN"
		echo "COMMERCIAL MAX: $CS_COMM_MAX"
fi

