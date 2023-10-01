## CHANNEL SIMULATOR                                                                                               
ChannelSimulator is a project that takes local media files in directories that are defined by a configuration file and plays them
in an order similar to that of a television broadcast. 

### **This branch is UNSTABLE and MIGHT, MAY, OR WILL BREAK STUFF! BE WARNED!**

## REQUIREMENTS
ChannelSimulator requires that the following packages be installed on your linux system (Other OS not currently supported at this time!):
- VLC
- ffmpeg
- mediainfo
- xorg-x11-server-xvfb
- xdpyinfo

## SUPPORT
Support for ChannelSimulator is limited in scope at present.
| Operating System | Supported? | Planned? |
| ---------------- | ---------- | -------- |
| Ubuntu Linux     | Yes        | Yes      |
| Fedora Linux     | Yes        | Yes      |
| Raspbian Linux   | No         | Yes      |
| Windows 11       | No         | Maybe    |
| Windows 10       | No         | Maybe    |
| Android          | No         | No       |
| MacOS            | No         | Yes      |
| iOS              | No         | No       |



## INSTRUCTIONS
1. Clone this repository
   - use the command `git pull https://github.com/gwsif/ChannelSimulator-BASH`
   - or by choosing Code > "Download Zip" from the main repository and unzipping it.
2. Make sure all of the files are executable.
   - Open a terminal from inside the ChannelSimulator folder or navigate to it from a terminal and copy and paste the following command:
   ```
   sudo chmod +x chansim.sh display_video.sh play_show.sh play_commercials.sh scan_config.sh simulate_marathon.sh display_menu.sh channel_simulator.cfg
   ```
3. Run chansim
   ```
   ./chansim
   ```
4. If you are playing back locally (IE: on your own machine) then press `3` to begin the simulation.
5. If you are playing back headless (IE: over LAN) then press `1` to start the virtual broadcast and then press `3` to begin the simulation

Please note that, by default, ChannelSimulator uses an `Xvfb display` value of `100` (aka id) and `nc` with `port 5000`. If you are currently using any software that conflicts with these defaults, you may change them in the configuration file. Please also note that when restarting the headless stream, a kill command is run on the process `nc` as well as `vlc` so if you are running other instances of these then ChannelSimulator **WILL** interfere with them!


## FUTURE
There will be more additions/expansions to this system as I move forward! It is currently planned to allow for custom time splitting on video files that have commercial break openings, but are continuous (as in one file) rather than non-continuous (as in multiple files). Commercial segments based on time vs number of commercials is also planned. Down the line I would like to add more advanced stuff such as overlays, video and audio effects, support for tagging and automated broadcasts based on those tags, and more. Support for YouTube links as well as other media URLs that are natively handled by VLC is also coming. **You absoluely will be able to mix and match local files & remote media URL's for playback!**

ChannelSimulator will eventually be capable of generating its own unique graphics set to add to broadcasts in addition to traditional media as well, however this is only and end goal at present!
