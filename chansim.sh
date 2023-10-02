#!/bin/bash
#
# C H A N N E L  S I M U L A T O R
# ========================================================================                                                                                                                                                              
# BASH VERSION 0.25.4 - ©KEVAN PLEDGER 2023
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

# CHECK FOR EXISTENCE OF CONFIG 
if [[ -f ""$CS_INSTALL_PATH"/channel_simulator.cfg" ]];
    then
        # IF WE HAVE A CONFIG FILE THEN SOURCE IT
        source channel_simulator.cfg

        # AND ANNOUNCE OUR SUCCESS TO CONSOLE
        echo "[SUCCESS] CONFIG FILE FOUND AT:$CS_INSTALL_PATH"

        # CHECK DESIRED VIEWING METHOD
        if [[ $CS_METHOD == "headless" ]];
            then
            # ANNOUNCE TO CONSOLE
            echo "[INFO] HEADLESS MODE DETECTED..."

            # RUN DRAW DISPLAY TO DRAW XVFB AND EXECUTE CHANSIM.SH
            ./draw_display.sh "$CS_INSTALL_PATH"

            elif [[ $CS_METHOD == "local" ]];
            then
            # ANNOUNCE TO CONSOLE
            echo "[INFO] LOCAL MODE DETECTED..."
            
            # RUN CHANSIM.SH
            ./display_menu.sh "$CS_INSTALL_PATH"
            else
            # IF WE HAVE ANY OTHER VALUE WE AREN'T VALID
            echo "[WARNING] INVALID METHOD SETTING:$CS_METHOD"
            echo "[WARNING] CS_METHOD MUST BE SET TO 'headless' OR 'local' IN THE CONFIG FILE!"
        fi
        
    else
        # IF ITS BROKE, BREAK IT MORE AND ERROR
        echo "[WARNING] INVALID OR MISSING CONFIG FILE!"
        echo "[DEBUG] OUR INSTALL PATH VALUE IS:$CS_INSTALL_PATH"
        echo "---------- BREAKING-------------"
        break
fi
