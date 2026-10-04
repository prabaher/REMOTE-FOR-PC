# Laptop Remote

A lightweight web-based remote control for a Windows laptop. The Flask server
serves a browser interface that can control media playback, volume, keyboard
arrows, the mouse, and a few Windows window actions through PyAutoGUI.

## Features

- Media controls: play/pause, volume up/down, previous, and next
- Keyboard arrow controls
- Mouse touchpad and click controls
- Minimize all windows, restore windows, and switch applications
- Connection status and hostname display
- Windows launcher that prints the laptop's LAN address and opens the local UI

## Requirements

- Windows
- Python 3.9 or newer
- A phone or another device connected to the same local network

## Setup

1. Clone or download this repository.
2. Open PowerShell or Command Prompt in the project directory.
3. Create and activate a virtual environment (recommended):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install the dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

If PowerShell blocks script activation, use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

## Run

### Recommended Windows launcher

Double-click `start_remote.bat`, or run it from a terminal:

```bat
start_remote.bat
```

The launcher displays the laptop's local IP address and opens the remote
interface at `http://127.0.0.1:5000`.

### Run manually

```powershell
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

To control the laptop from another device on the same network, open
`http://<LAPTOP-IP>:5000` on that device. Replace `<LAPTOP-IP>` with the
address printed by `start_remote.bat`.

Keep the terminal running while the remote is in use.

## Supported controls

The web interface sends control commands to the Flask `/control` endpoint.
The current commands include:

| Category | Actions |
| --- | --- |
| Mouse | Move up, down, left, or right; left click; right click |
| Media | Play/pause; volume up/down; forward; backward |
| Keyboard | Up, down, left, and right arrow keys |
| Windows | Minimize, restore, and Alt+Tab |

## Security notes

This app is intended for use on a trusted local network. It does not include
authentication or encryption, and the server listens on all network
interfaces (`0.0.0.0`). Anyone who can reach port `5000` on the laptop may be
able to control the mouse, keyboard, and media playback.

- Do not expose port `5000` directly to the internet.
- Use the app only on a trusted network.
- Stop the server when it is no longer needed.
- If Windows Firewall prompts for access, allow private networks only.

The app currently runs Flask with debug mode enabled for local development.
Disable debug mode before using it in any less-trusted environment.

## Project structure

```text
.
├── app.py                 # Flask server and PyAutoGUI command handling
├── requirements.txt       # Python dependencies
├── start_remote.bat       # Windows launcher
├── templates/
│   └── remote.html        # Remote-control page
└── static/
    ├── app.js             # Browser controls and connection status
    └── style.css          # Interface styling
```

