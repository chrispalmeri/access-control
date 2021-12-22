Using this board as testbench cause you have HDMI and can install a regular desktop

# Browser

`apt-get purge chromium` and then install "firefox-esr".
I tried like five browsers and it was the best on a low power device.

# Git

Configure it, don't remember exactly what was required

# Geany

Just to remember what I did, obviously setup to your liking.

`apt-get install geany-plugins`

make it dark theme:

`~/.config/gtk-3.0/settings.ini`

```
[Settings]
gtk-application-prefer-dark-theme=true
```

> Himbeere theme from https://www.geany.org/download/themes/

download the configuration file and put it into `~/.config/geany/colorschemes/`

then View > Change Color Theme


## plugins

Addons -> mark by double click, deselect single click

  * Tree Browser
  * Git Change Bar
  * Overview

```
msgwin_status_visible=false
msgwin_compiler_visible=false
msgwin_messages_visible=false
msgwin_scribble_visible=false
```
