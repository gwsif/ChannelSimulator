#!/bin/bash
# ::::::::::::::::::::::::::::::::::::::::::::.
# C H A N N E L  S I M U L A T O R
# `````````````````````````````````````````````
# TELEVISION BROADCAST SIMULATOR
# ©KEVAN PLEDGER 2023
# ::::::::::::::::::::::::::::::::::::::::::::.
#
# DRAW DISPLAY SCRIPT
#    DRAWS THE XVFB HEADLESS DISPLAY AND THEN RUNS THE MAIN CHANSIM.SH SCRIPT ON IT.
# -----------------------------------------------------------------------------------

# VARIABLE CHEATSHEET
# $1 = $CS_INSTALL_PATH

# ALWAYS SOURCE OUR CONFIG FIRST
source ""$1"/channel_simulator.cfg"

# DEBUG ECHOES
echo "DOLLAR 1 IS: $1"

# ANNOUNCE HEADLESS TO CONSOLE
echo "[INFO] ATTEMPTING TO DRAW VIRTUAL DISPLAY."

# DRAW DISPLAY USING SUBSHELL
(nohup Xvfb $CS_XVFB_DISPLAY_NUM -screen 0 "${CS_XVFB_RES_WIDTH}x${CS_XVFB_RES_HEIGHT}x${CS_XVFB_COL_DEPTH}" > /dev/null 2>&1 &)

# ANNOUNCE TO CONSOLE
echo "[INFO] DISPLAY SHOULD HAVE BEEN STARTED WITH DISPLAY NUMBER $CS_XVFB_DISPLAY_NUM "

# START THE MAIN SCRIPT ON THE HEADLESS DISPLAY!
DISPLAY=:100 "$1"/display_menu.sh $1

