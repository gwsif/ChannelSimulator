# CHANNEL SIMULATOR                                                                                               
ChannelSimulator is a project that takes local media files in directories that are defined by a configuration file and plays them
in an order similar to that of a television broadcast.

## INSTRUCTIONS
1. Clone this repository either by using `git pull https://github.com/gwsif/ChannelSimulator-BASH` or by choosing Code > "Download Zip" from the main repository and unzipping it into your home folder.
2. Rename the folder `ChannelSimulator-BASH` to just `ChannelSimulator`.
3. Ensure the contents of the folder contains the scripts/ and config/ directories as well as the main chansim.sh script.
4. Modify `config/channel_simulator.cfg` in a text editor and change the parameters you would like using the comments as instructions and then save it.
7. Open a terminal and type `cd $HOME/ChannelSimulator/; chmod +x chansim.sh; $/HOME/ChannelSimulator/chansim.sh`
8. Press 1 to read in the config file.
9. Press 2 to start the broadcast!
10. Enjoy!

When you are finished, close the terminal running the script first and then close the media player. Then run `sudo killall your-media-player` where `your-media-player` is the same media player you have specified in your config file!

## BONUS!
(This process will be getting automated soon!)
You can pipe the video output to a stream, which you can then connect to via VLC on another PC by doing the following:
1. Open a terminal
2. If you have VLC and ffmpeg installed you can move on to step 3, otherwise install them via your package manager of choice.

   
*Ubuntu (example)*
```
sudo apt update; sudo apt install vlc ffmpeg
```
*Fedora (example)*
```
sudo dnf upgrade; sudo dnf install vlc ffmpeg
```
---
3. Once VLC and ffmpeg are installed, enter the following into the terminal:
```
Xvfb :100 -screen 0 1280x1024x24 &
```
```
DISPLAY=:100 $HOME/ChannelSimulator/chansim.sh
```
4. Open a new tab or terminal and type:
```
ffmpeg -f x11grab -framerate 30 -video_size 1280x1024 -i :100 -f pulse -i default -c:v libx264 -preset fast -maxrate 2500k -bufsize 5000k -g 60 -vf format=yuv420p -c:a aac -b:a 128k -f avi - | nc -lp 5000
```
This last command will open up port 5000 (customize it if you wish), which you can then connect to on another computer by opening VLC, going to Media > Open Network Stream... and then pasting in the following making sure to change xxx.xxx.xxx.xxx to the ip address and yyyy to the port of the machine that is currently running Channel Simulator. Port 5000 is specified in the prior command using the nc -lp 5000 command and can be changed!
```
tcp://xxx.xxx.xxx.xxx:yyyy
```
Hit Play and enjoy an old fashioned television broadcast! Please note that if you stop watching the stream, it will terminate the entire stream at present. You need only re enter that long ffmpeg command to restart the broadcast. The simulation will be unaffected running this way. Please note that there are issues with this process such as the video surface being drawn/cropped improperly during the broadcast. This will be resolved in upcoming releases but you can mitigate them for now by choosing a slightly smaller display surface of 800x600 instead of the recommended 1280x1024 in the launch commands. Again, this process will be mostly automated in the future so this is just a stopgap. 

When you are finished, close the terminal/tab running the script. Then open a new terminal/tab and run `sudo killall your-media-player` where `your-media-player` is the same media player you have specified in your config file. Then close all tabs. The media stream in your other tab will have been broken when you close VLC. This is a bug at present, and something that will be fixed in the future.

## FUTURE
There will be more additions/expansions to this system as I move forward! It is currently planned to allow for custom time splitting on video files that have commercial break openings, but are continuous (as in one file) rather than non-continuous (as in multiple files). Commercial segments based on time vs number of commercials is also planned. Down the line I would like to add more advanced stuff such as overlays, video and audio effects, support for tagging and automated broadcasts based on those tags, and more.

ChannelSimulator will eventually be capable of generating its own unique graphics set to add to broadcasts in addition to traditional media as well, however this is only and end goal at present!

## SUPPORT
| Operating System | Supported? |
| ---------------- | ---------- |
| Ubuntu Linux     | Yes        |
| Fedora Linux     | Yes        |
| Raspbian Linux   | No         |
| Windows 11       | No         |
| Windows 10       | No         |
| Android          | No         |
| MacOS            | No         |
| iOS              | No         |

