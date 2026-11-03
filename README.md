# pi-fireplace

Raspberry PI based fireplace

## Installation

On your raspberry pi run

```console
sudo apt update
sudo apt install -y mpv ffmpeg socat
mkdir -p ~/Videos
```

Download a fireplace video in the `~/Vidoes` folder

Add the following to `~/.config/systemd/user/fireplace.service`:

```ini
[Unit]
Description=Digital Fireplace Player

[Service]
Type=simple
ExecStart=/usr/bin/mpv --fs --loop-file=inf --no-osc --osd-level=0 --cursor-autohide=always --hwdec=auto --input-ipc-server=%t/fireplace-mpv.sock %h/Videos/fireplace.mp4
Restart=always
RestartSec=3
```

Add the following to `~/.config/labwc/autostart`:

```bash
systemctl --user import-environment WAYLAND_DISPLAY DISPLAY XDG_SESSION_TYPE XDG_CURRENT_DESKTOP
systemctl --user start fireplace.service &
```
