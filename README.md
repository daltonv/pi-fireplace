# Pi Fireplace 🔥

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

## python server

A learning project: a Raspberry Pi fireplace video player controlled through a local HTTP API.

This repository is intentionally a **skeleton**, not a finished application. The API is up and running, but the actual MPV interaction is yours to build.

## Quick start

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run uvicorn pi_fireplace.main:app --reload --host 127.0.0.1 --port 8000
```

Open:

- API docs: <http://127.0.0.1:8000/docs>
- Health check: <http://127.0.0.1:8000/api/v1/health>

Run tests and linting:

```bash
uv run pytest
uv run ruff check .
```

When you add/remove dependencies, use `uv add` and `uv remove`. Commit the `uv.lock` that `uv sync` produces.

## Structure

```text
pi-fireplace/
├── pyproject.toml                  # uv project + dependencies
├── src/pi_fireplace/
│   ├── main.py                     # app composition, API routers
│   ├── api/routes/
│   │   ├── health.py               # working example endpoint
│   │   └── playback.py             # your future player endpoints
│   └── services/
│       └── mpv.py                  # your future MPV IPC integration
├── tests/
│   └── test_health.py              # one reference API test
└── web/
    └── README.md                   # reserved for future frontend
```

## Suggested next steps (you implement these)

1. Define the interface your player service should offer: status, play, pause, volume, load file.
2. Learn MPV's [JSON IPC](https://mpv.io/manual/stable/#json-ipc) and implement one command in `services/mpv.py`.
3. Expose that command in `api/routes/playback.py` using FastAPI.
4. Add tests for your endpoint, using a fake service rather than running a video in the test suite.
5. Decide how to launch/monitor MPV independently of FastAPI (e.g., systemd); keep the web server independent of the video process.
6. Later, build a web UI in `web/` that sends HTTP requests to `/api/v1/...`.

A possible API design, **not implemented**:

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/playback/state` | Current media, pause state, volume |
| POST | `/api/v1/playback/play` | Resume playback |
| POST | `/api/v1/playback/pause` | Pause playback |
| PUT | `/api/v1/playback/volume` | Set volume |
| PUT | `/api/v1/playback/media` | Change active video |

Don't treat these routes as mandatory. Decide your own contracts as you learn.

## Developing over SSH

Keep the API bound to localhost initially (`127.0.0.1`). From your Mac, you can tunnel to the Pi:

```bash
ssh -L 8000:127.0.0.1:8000 <pi-user>@fireplace.local
```

Then open <http://127.0.0.1:8000/docs> on your Mac. This lets you develop without exposing an unauthenticated video-control API to the whole network. When you add a real frontend, decide how it will be served and secured before exposing the API on your LAN.
