#!/bin/bash
# ::::::::::::::::::::::::::::::::::::::::::::.
# C H A N N E L  S I M U L A T O R
# `````````````````````````````````````````````
# TELEVISION BROADCAST SIMULATOR
# ©KEVAN PLEDGER 2023
# ::::::::::::::::::::::::::::::::::::::::::::.
#
# DISPLAY VIDEO SCRIPT
#    INGESTS A URL OR FILEPATH AS $1, PERFORMS TRANSFORMATIONS ON IT
#    VIA X-VIDEO-FRAME-BUFFER (XVFB) AND DYNAMICALLY CHOOSES WHETHER 
#    OR NOT TO DISPLAY A VIDEO OVER A NETWORK PATH OR LOCALLY VIA THE
#    DESIRED MEDIAPLAYER AS SET IN THE CONFIGURATION FILE.
# ------------------------------------------------------------------------

# VARIABLE CHEATSHEET
# $1 = $CS_SHOW_SELECTED -OR- $CS_COMM_SELECTED
# $2 = $CS_SHOW_DIR -OR- $CS_COMM_DIR
# $3 = $CS_INSTALLATION_PATH
# $4 = $CS_SHOW_RUNTIME -OR- $CS_COMM_RUNTIME

# ANNOUNCE SCRIPT EXECUTION
echo "[INFO] display_video.sh executing..."

# ALWAYS SOURCE OUR CONFIG FIRST
source ""$3"/channel_simulator.cfg"

# CHANGE DIRECTORY BACK TO GIVEN DIRECTORY
cd "$2"

# DEBUG ECHOES
#echo "---- DISPLAY VIDEO DEBUG BLOCK--------------"
#echo "[DEBUG] DISPLAY VIDEO - GOT GOLLARTWO OF $2"
#echo "[DEBUG] DISPLAY VIDEO - GOT DOLLARONE OF $1"
#echo "[DEBUG] DISPLAY VIDEO - GOT DOLLARTHR OF $3"
#echo "--------------------------------------------"

# FILEPATH is DIR/FILE ($2/$1)
CS_FILEPATH=$(echo "$2"'/'"$1")
#echo "CS_FILEPATH= $CS_FILEPATH"

# CHECK IF WE ARE SET TO LOCAL OR HEADLESS DISPLAY METHOD
if [[ $CS_METHOD == "local" ]];
then
    # IF WE ARE SET TO LOCAL MODE THEN ANNOUNCE FILEPATH WE ARE PLAYING
    echo "[INFO] PLAYING FILE:$CS_FILEPATH"

    # AND CALL THE PLAYBACK COMMAND HERE!
    #timeout "$4" "$CS_MEDIAPLAYER" -I dummy --qt-minimal-view --no-qt-name-in-title --no-video-title-show --no-video-deco --no-embedded-video --fullscreen "$CS_FILEPATH"
    #timeout 10s "$CS_MEDIAPLAYER" -I dummy --scale $CS_VIDEO_SCALED --qt-minimal-view --no-qt-name-in-title --no-video-deco --no-embedded-video "$CS_FILEPATH" &>/dev/null 
    timeout "$4" ffplay -fs "$CS_FILEPATH"


elif [[ $CS_METHOD == "headless" ]];
then
    # HEADLESS MODE SET! CHECK IF WE'VE ALREADY DRAWN THE DISPLAY!
    echo "display check!"
    CS_XVFB_STATUS=$(xdpyinfo -display :100 >/dev/null 2>&1 && echo "open" || echo "closed")
    echo "display is: $CS_XVFB_STATUS"
    if [ $CS_XVFB_STATUS == "closed" ];
    then
        echo "[NOTICE] XVFB DISPLAY $CS_XVFB_DISPLAY_NUM IS NOT CURRENTLY RUNNING!"
    else
        # WE HAVE A RUNNING DISPLAY SO VALIDATE OUR FILE PATH, SCALE THE VIDEO, AND THEN PLAY IT!
        if [[ -f "$CS_FILEPATH" ]]; 
        then

            # IF FILEPATH EXISTS, GRAB THE DIMENSIONS
            CS_VIDEO_DIMENSIONS_RAW=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$1")

            # EXTRACT THE WIDTH AND HEIGHT DIMENSIONS FROM THE VIDEO INFO STRING
            IFS=',' read -ra CS_VIDEO_DIMENSIONS <<< "$CS_VIDEO_DIMENSIONS_RAW"
            CS_VIDEO_WIDTH="${CS_VIDEO_DIMENSIONS[0]}"
            CS_VIDEO_HEIGHT="${CS_VIDEO_DIMENSIONS[1]}"

            # DEBUG ECHOES
            echo "---- DISPLAY VIDEO DEBUG BLOCK--------------"
            echo "CS_VIDEO_WIDTH: $CS_VIDEO_WIDTH "
            echo "CS_VIDEO_HEIGHT: $CS_VIDEO_HEIGHT"
            echo "CS_XVFB_RES_WIDTH: $CS_XVFB_RES_WIDTH"
            echo "CS_XVFB_RES_HEIGHT: $CS_XVFB_RES_HEIGHT"
            echo "CS_VIDEO_SCALE_WIDTH: $CS_VIDEO_SCALE_WIDTH"
            echo "CS_VIDEO_SCALE_HEIGHT: $CS_XVFB_RES_HEIGHT"
            echo "--------------------------------------------"
            
            # CALCULATE SCALING FACTORS!
            CS_VIDEO_SCALE_WIDTH=$(expr $CS_XVFB_RES_WIDTH \* $CS_VIDEO_HEIGHT / $CS_XVFB_RES_HEIGHT)
            CS_VIDEO_SCALE_HEIGHT=$(expr $CS_XVFB_RES_HEIGHT \* $CS_VIDEO_WIDTH / $CS_XVFB_RES_WIDTH)
            
            # DEBUG ECHOES
            echo "---- DISPLAY VIDEO DEBUG BLOCK--------------"
            echo "CS_VIDEO_SCALE_WIDTH: $CS_VIDEO_SCALE_WIDTH"
            echo "CS_VIDEO_SCALE_HEIGHT: $CS_VIDEO_SCALE_HEIGHT"
            echo "--------------------------------------------"

            # USE THE SMALLER SCALING FACTOR TO FIT THE VIDEO WITHIN THE XVFB DISPLAY
            if [ "$CS_VIDEO_SCALE_WIDTH" -le "$CS_VIDEO_WIDTH" ];
                then
                    CS_VIDEO_SCALED="CS_VIDEO_SCALED=$CS_VIDEO_SCALE_WIDTH:-1"
                else
                    CS_VIDEO_SCALED="CS_VIDEO_SCALED=-1:$CS_VIDEO_SCALE_HEIGHT"
            fi
        
            # RUN OUR VIDEO HERE
            #    Old Logic Preserved temporarily
            #DISPLAY="$CS_XVFB_DISPLAY_NUM" timeout $4 "$CS_MEDIAPLAYER" -I dummy --width="$CS_VIDEO_SCALE_WIDTH" --height="$CS_VIDEO_SCALE_HEIGHT" --audio-filter normalizer --qt-minimal-view --no-qt-name-in-title --no-video-deco --no-embedded-video --no-osd "$CS_FILEPATH"
            #DISPLAY="$CS_XVFB_DISPLAY_NUM" timeout 10s "$CS_MEDIAPLAYER" -I dummy --width="$CS_VIDEO_SCALE_WIDTH" --height="$CS_VIDEO_SCALE_HEIGHT" --audio-filter normvol --qt-minimal-view --no-qt-name-in-title --no-video-deco --no-embedded-video --no-osd "$CS_FILEPATH"
            #DISPLAY="$CS_XVFB_DISPLAY_NUM" timeout 10s "$CS_MEDIAPLAYER" --fullscreen --audio-filter normvol --qt-minimal-view --no-qt-name-in-title --no-video-deco --no-embedded-video --no-osd "$CS_FILEPATH"
            DISPLAY="$CS_XVFB_DISPLAY_NUM" timeout $4 "$CS_MEDIAPLAYER" --fullscreen --audio-filter normvol --qt-minimal-view --no-qt-name-in-title --no-video-deco --no-embedded-video --no-osd "$CS_FILEPATH"
                        
            # If youtube url, we just resize it to our display
            # do some stuff ;;
        else
            # INVALID URL - THROW ERROR AND BREAK!
            echo "INVALID URL OR FILEPATH - PLEASE CHECK FILEPATHS OR URL LIST"
            break
        fi
    fi
else
    # IF WE ARE HERE WE DIDN'T PULL A VALID METHOD SETTING FROM THE CONFIG!
    echo "[WARNING] INVALID METHOD SETTING!"
    echo "[DEBUG] EXPECTED CS_METHOD VALUE OF headless OR local BUT GOT:$CS_METHOD"
#----#
fi



