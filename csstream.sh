#!/bin/bash
# *****************************************************************************
# CHANNELSIMULATOR
# Copyright (C) 2023 Kevan Pledger
# *****************************************************************************
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
# ****************************************************************************

# $1 = Expected Video Width
# $2 = Expected Video Height
# $3 = Expected Xvfb Display Number (includes :)
# $4 = Expected Network Port For Playback

# Debug block
#echo "[DEBUG] Running csstream.sh"
#echo "[DEBUG] starting ffmpeg command"
#echo "[DEBUG] Vdeo Width: $1"
#echo "[DEBUG] Vdeo Height: $2"
#echo "[DEBUG] Display Number: $3"
#echo "[DEBUG] Port Number: $4"

# Launches ffmpeg stream via tcp stream over local ip and specified port (default)
nohup sh -c "ffmpeg -f x11grab -nostdin -draw_mouse 0 -framerate 30 -video_size $1'x'$2 -i $3 -f pulse -i default -c:v libx264 -preset fast -maxrate 2500k -bufsize 2500k -g 60 -c:a aac -b:a 128k -listen 1 -f flv http://0.0.0.0:$4" > /dev/null 2>&1 &


