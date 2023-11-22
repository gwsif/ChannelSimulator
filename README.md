![Logo](https://github.com/gwsif/ChannelSimulator/blob/testing/channelsim_zerofour_crop.png?raw=true)


# ChannelSimulator

ChannelSimulator is a project that takes local media files in directories that are defined by a configuration file and plays them in an order similar to that of a television broadcast.

ChannelSimulator was developed as a means to provide a method of recreating old television broadcasts of yesteryear simply by using video files and simple, easy to understand text files which you can then broadcast to a smart-tv or other screen via VLC's network stream functionality (or similar equivalent). 

The end goal is to be provide a simple, yet flexible enough solution for simulating a convincing broadcast of your choosing so long as you have access to the original media (ie: episodes/movies/commercials). Eventually ChannelSimulator should be capable of generating its own internal graphics like LDL's (Lower Display Line's), dynamic channel watermark/branding, and dynamic, scrolling tv guide.



## Features

**Current v0.4 feature-set:**
- Marathon mode
- Headless playback
- Local playback
- Local file support

Marathon Mode:
Plays episodes of a single series in a single, local directory interspersed with a random number of commercials.

Broadcast Mode:
Plays episodes from multiple series in multiple, local directories intersperesed with a random number of commercials.

-*-*-*-*-*-*-*-*-

**Upcoming Features:**
- Broadcast mode
- YouTube support
- Commercial breaks on continuous files ("split-files")
- Community-driven, "split-file" support to eliminate double work.
- LDL (Lower Display Line) generation
- Channel corner watermarking/branding
- Advanced block programming.
- Smart shuffle/random to prevent repeats
- Customizable resolution to be kind to your CPU/GPU
- Full ARM support for RPi goodness
- Cloud storage support
- Advanced, automated playback of general web-content
- EAS integration for live and period accurate (Customizable) emergency alerts





## Support

Currently ChannelSimulator only supports Linux based operating systems for running the simulation. For viewing the headless stream, you may use any player capable of playing back a TCP network stream (e.g.: VLC)

Running the simulation under WSL may be possible but is untested and not-recommended. 

## Installation

When I have installation instructions

```bash
  iwill place
  them here
```

## FAQ

#### Will I have to 'split' my videos into different files for commercials to play?

No. This is the primary purpose of ChannelSimulator. The 'split' is handled by timecodes inside of a text file that is named identically to the episode being played. For example if the episode were titled 'season1 - episode1.mp4' then the accompanying 'split' file would be named 'season1 - episode1.csv'. This text file will hold information about the video file and will unfortunately need to be manually populated. 

This means that, while you won't need to actually split your video files up, you will need to watch through them and find the timecodes where a commercial break should be and record that into the file. These files are designed to be distributable as they contain merely timecode information meaning the work theoretically only has to be performed once provided the original file remains consistent.

#### Does this handle 'bumpers' like [adult swim]'s?
Yes - but not as of current. Bumper support is planned however! Simulation of cartoon cartoon fridays, mid-00s adult swim, Y2K new years celebrations, whatever. As long as you have legal access to the material you are using, it is supported. 

#### Can I run this on my TV?
Yes, provided you have a smart-tv or android/google-tv capable of either installing VLC or playback of a tcp network stream. The program will generate an ip and port combination for you to conveniently connect to.

#### Can I run this on my PC/Mac?
No - unless you run Linux, in which case, Yes (see addendum below). Regrettably this solution relies on technology that is inherent to the Linux OS. 

It *might* be possible to run it under WSL, however I have not tested this. Mac is a similar story and remains untested.

#### Can I run this on my favorite SBC?
Yes. ChannelSimulator aims to be compatible with Raspberry Pi and the ARM architecture. Currently ARM support is untested though and is/will remain unstable and unguarantee'd until the eventual Version 1.0 release.



## Roadmap
Currently ChannelSimulator is on Version 0.4 alpha. Version 1.0 is considered the long-term target.

**v0.4**
- Python rebase
- Marathon mode
- Headless playback
- Local playback
- Local file support targeted 

**v0.5**
- Basic "split-file" support targeted
- Broadcast mode
- Basic YouTube support targeted

**v0.6**
- ARM testing
- LDL (Lower Display Line) support targeted 
- Channel watermark/branding support targeted

**v0.7**
- Smart shuffle/random to prevent repeats

-*-*-*-*-*-*-*-*

....

-*-*-*-*-*-*-*-*

**v1.0**
- Tagging
- Support for commercial block by time vs number
- Advanced support for headless playback of web-content
- ARM support
- Full YouTube support
- Cloud storage support
- Community-driven, "split-file" support to eliminate double work.

The following is a future wishlist of features/suggestions that are targeted for eventual inclusion.

**v1.1**
- Multi-Channel support
- Dynamic TV guide Channel
## Acknowledgements

 - [Awesome Readme Templates](https://awesomeopensource.com/project/elangosundar/awesome-README-templates)
 - [Awesome README](https://github.com/matiassingers/awesome-readme)
 - [dots-nordic](https://github.com/SkyyySi/dots-nordic/tree/master)



## License
ChannelSimulator is licensed under the Gnu GPL Version 3.0 License. A copy of the license is distributed with this project and is also made available in full at the link below.

* [https://www.gnu.org/licenses/gpl-3.0.en.html](https://www.gnu.org/licenses/gpl-3.0.en.html)