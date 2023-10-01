#!/bin/bash
#
# C H A N N E L  S I M U L A T O R
# ========================================================================                                                                                                                                                              
# BASH VERSION 0.25.1 - ©KEVAN PLEDGER 2023
# ========================================================================
# ::::::::::::::::  !EDIT CONFIG FILE PRIOR TO RUNNING!  :::::::::::::::::
# ------------------------------------------------------------------------
# BEGIN MAIN PROGRAM
# --------------------

# ECHO GREETING
echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::."
echo "█▀▀ █░█ ▄▀█ █▄░█ █▄░█ █▀▀ █░░  █▀ █ █▀▄▀█ █░█ █░░ ▄▀█ ▀█▀ █▀█ █▀█"
echo "█▄▄ █▀█ █▀█ █░▀█ █░▀█ ██▄ █▄▄  ▄█ █ █░▀░█ █▄█ █▄▄ █▀█ ░█░ █▄█ █▀▄"
echo "TELEVISION BROADCAST SIMULATOR - BASH VERSION ©KEVAN PLEDGER 2023"
echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::."

# FIND INSTALL DIRECTORY OF CHANSIM
CS_INSTALL_PATH="$(pwd)"

# ECHO ATTEMPT TO CONSOLE
echo "[INFO] LOOKING FOR CONFIG FILE..."

# ALWAYS CHECK FOR EXISTENCE OF CONFIG
if [[ -f ""$CS_INSTALL_PATH"/channel_simulator.cfg" ]];
    then
        # IF WE HAVE A CONFIG FILE THEN SOURCE IT
        source channel_simulator.cfg

        # AND ANNOUNCE OUR SUCCESS TO CONSOLE
        echo "[SUCCESS] CONFIG FILE FOUND AT:$CS_INSTALL_PATH"

        # RUN OUR MENU AND PASS OUR INSTALL PATH
        ./display_menu.sh "$CS_INSTALL_PATH"
    else
        # IF ITS BROKE, BREAK IT AND ERROR
        echo "[WARNING] INVALID OR MISSING CONFIG FILE!"
        echo "[DEBUG] OUR INSTALL PATH VALUE IS:$CS_INSTALL_PATH"
        echo "---------- BREAKING-------------"
        break
fi
