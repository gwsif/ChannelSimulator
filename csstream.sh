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

# Launches ffmpeg stream piped into nc through local port of choice.
nohup sh -c "ffmpeg -f x11grab -nostdin -draw_mouse 0 -framerate 30 -video_size $1'x'$2 -i $3 -f pulse -i default -c:v libx264 -preset fast -maxrate 2500k -bufsize 2500k -g 60 -c:a aac -b:a 128k -f avi - | nc -lp $4" > /dev/null 2>&1 &