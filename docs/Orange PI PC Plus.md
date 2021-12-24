Using this board as testbench cause you have HDMI and can install a regular desktop

Armbian bullsey is under other downloads and does not include desktop

run through initial config
as soon as you get a terminal, don't do anything else, reboot
cause there was an issue with no default terminal or something

shutdown -r now
sudo apt update
sudo apt upgrade
sudo armbian config

replace "System > Install > Boot from eMMC - system on eMMC" with "System > Default" to install desktop

> actually it does have eMMC also if you want

then exit and `sudo dpkg --configure -a`
cause it didn't finish all that for some reason and desktop would not work

then go back to `sudo armbian config`
You will have option for System > Desktop
Enable Auto Login = No

should drop you to desktop
reboot to make sure everything is good, audio for example needed it

rest is just preferences
default applications, theme, notifications, desktop, purge some stuff

<!--
I tried like five browsers and firefox-esr was least laggy
-->

# Git

See github cheetsheet TODO: add link

# Geany

Just to remember what I did, obviously setup to your liking.

`sudo apt install geany geany-plugins`

<!--
make it dark theme:

`~/.config/gtk-3.0/settings.ini`

```
[Settings]
gtk-application-prefer-dark-theme=true
```
-->

> Himbeere theme from https://www.geany.org/download/themes/

download the configuration file and put it into `~/.config/geany/colorschemes/`

then View > Change Color Theme


## plugins

  * Addons
    * Preferences = (unselect) show available tasks, (select) mark by double click, deselect single click
  * Tree Browser
  <!-- * Git Change Bar
  * Overview -->

## Preferences

unselect

Interface > Interface

Show symbols
Show documents

Interface > Toolbar

Show toolbar

Editor

(select these)
Features > Newline strips trailing spaces
Indentation > Spaces
Completions > disable all
Display > Indentation Guides, and White space

Files

(select)
strip trailing
replace tabs

Various

intergace.msgwin_compiler_visible
intergace.msgwin_messages_visible
intergace.msgwin_scribble_visible
intergace.msgwin_status_visible

