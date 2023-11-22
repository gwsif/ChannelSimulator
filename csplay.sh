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

# $1 = Expected Runtime
# $2 = Expected Filepath
# $3 = Expected Mediaplayer

# Opens a video ($2) in borderless fullscreen for a specified time period ($1) using the specified mediaplayer ($3)
timeout $1 "$3" --fullscreen --audio-filter normvol --qt-minimal-view --no-qt-name-in-title --no-video-deco --no-embedded-video --no-osd "$2"