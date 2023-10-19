#!/bin/bash
# ::::::::::::::::::::::::::::::::::::::::::::.
# C H A N N E L  S I M U L A T O R
# `````````````````````````````````````````````
# TELEVISION BROADCAST SIMULATOR
# ©KEVAN PLEDGER 2023
# ::::::::::::::::::::::::::::::::::::::::::::.
#
# PLAY SHOW SCRIPT
#    PLAYS A SINGLE SHOW SEGMENT. IF A CSBREAK FILE IS FOUND, THEN IT WILL PLAY THE VIDEO UNTIL THE FIRST ENCOUNTERED
#    TIMESTAMP IN THE CSBREAK FILE, AND THEN PLAY COMMERCIALS. IF THERE IS NO NEXT ENTRY IN THE CSBREAK FILE, THE ENDING DURATION
#    IS CALCULATED TO BE THE TOTAL LENGTH OF THE VIDEO SUBTRACTED BY THE LAST TIMESTAMPS VALUE PLUS OUR OFFSET. IF NO CSBREAK FILE
#    IS FOUND THEN IT WILL PLAY THE ENTIRE EPISODE FOLLOWED BY EXACTLY ONE SET OF COMMERCIALS. A BLOCK IS CONSIDERED AS FINISHED 
#    WHEN THE FINAL PORTION OF THE EPISODE PLAYS. SHOW BROADCASTS WILL ALWAYS START WITH ONE AD-BLOCK PRIOR TO BROADCAST!
#--------------------------------------------------------------------------------------

# ANNOUNCE SCRIPT EXECUTION
echo "[INFO] RUNNING play_show.sh"

# RESET OUR CONF LOAD STATE TO CHECK FOR VALID CONFIGURATION FILE
CS_CONF_LOAD_STATE=0

# DEBUG ECHOES
#echo "[DEBUG] PLAY SHOW - GOT DOLLARONE OF $1"
#echo "[DEBUG] PLAY SHOW - GOT GOLLARTWO OF $2"
#echo "[DEBUG] PLAY SHOW - GOT DOLLARTHR OF $3"

# ALWAYS SOURCE OUR CONFIG FIRST!
source ""$1"/channel_simulator.cfg"

# ANNOUNCE CONFIG LOAD STATE
if [ $CS_CONF_LOAD_STATE -eq 1 ];
    then
        echo "[INFO] SHOW SCRIPT ANNOUNCES CONF LOAD SUCCESS!"
    else
        echo "[WARNING] SHOW SCRIPT FAILED TO LOAD CONFIGURATION!"
        echo "[DEBUG] INSTALLATION DIRECTORY EXPECTED AT:$1"
        echo "[DEBUG] GOT INSTALLATION DIRECTORY OF "$1"/channel_simulator.cfg"

fi

# ANNOUNCE START OF SHOW BLOCK TO CONSOLE
echo "----------- SHOW BLOCK STARTING -----------"

# CHANGE INTO THE SHOW DIRECTORY
cd "$CS_SHOW_DIR"

# DEBUG ECHOES
echo "[DEBUG] FROM PLAY SHOW.SH - CS_SHOW_DIR is $CS_SHOW_DIR"

# GET FILEPATHS OF ALL SUPPORTED MEDIA FILES IN THE GIVEN DIRECTORY AND IN 
#    ALL SUBDIRECTORIES RECURSIVELY AND STORE THEM IN AN ARRAY
CS_SHOW_MASTERLIST=$(find . -regex ".*\.\(avi\|webm\|mp4\|mkv\|mpg\|mpeg\)")
for show in *
    do
        CS_SHOW_MASTERLIST=("${CS_SHOW_MASTERLIST[@]}" "$show")
    done
    
# GENERATE A RANDOM NUMBER SEED BETWEEN CS_SHOW_MIN AND CS_SHOW_MAX
# ASSUME WE WILL ALWAYS HAVE THIS MANY SHOWS
CS_SHOW_MIN=1
    
# GET THE NUMBER OF MEDIA FILES IN THE GIVEN DIRECTORY AND IN ALL SUBDIRECTORIES 
#    RECURSIVELY AND THEN ADD ONE TO ACCOUNT FOR THE ARRAY LENGTH!
CS_SHOW_MAX=$(expr $(find . -regex ".*\.\(avi\|webm\|mp4\|mkv\|mpg\|mpeg\)" | wc -l) - 1)
#echo "in case of fire CS_SHOW_MAX value is: $CS_SHOW_MAX"

# GENERATE A RANDOM NUMBER BETWEEN OUR MINIMUM AND MAXIMUM NUMBERS
CS_SHOW_RAND_SEED=$(shuf -i "$CS_SHOW_MIN-$CS_SHOW_MAX" -n 1)

# GET OUR RANDOM EPISODE
CS_SHOW_SELECTED="${CS_SHOW_MASTERLIST[$CS_SHOW_RAND_SEED]}"

# GET THE RUNTIME OF OUR RANDOM EPISODE
CS_SHOW_RUNTIME=$(mediainfo --Inform="General;%Duration%" "$CS_SHOW_SELECTED")

# RUNTIME IS IN MILLISECONDS, CHANGE TO SECONDS FOR TIMEOUT
CS_SHOW_RUNTIME=$(expr $CS_SHOW_RUNTIME / 1000)
    
# ANNOUNCE SELECTED FILE TO CONSOLE
#echo "---- PLAY SHOW DEBUG BLOCK--------------"
#echo "[DEBUG] SELECTED FILE: $CS_SHOW_SELECTED"
#echo "[DEBUG] RUNTIME: $CS_SHOW_RUNTIME"
#echo "[DEBUG] BEGINNING PLAYBACK VIA: $CS_MEDIAPLAYER"
#echo "----------------------------------------"

# CALL DISPLAY VIDEO AND PASS THE SELECTED FILE FIRST AND THE SHOWS DIRECTORY AS THE SECOND ARGUMENT
"$1"/display_video.sh "$CS_SHOW_SELECTED" "$CS_SHOW_DIR" "$1" "$CS_SHOW_RUNTIME"

# PURGE SELECTED AND MASTERLIST!
CS_SHOW_SELECTED=""
CS_SHOW_MASTERLIST=()

# ANNOUNCE END OF SHOW
echo "----------- SHOW BLOCK ENDING -----------"