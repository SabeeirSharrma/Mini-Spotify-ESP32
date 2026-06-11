# Spotify Display for ESP32

A plug-and-play Spotify display powered by an ESP32 and a 16x2 I²C LCD.

This project displays the currently playing Spotify track on a small external display connected to your computer. The desktop application communicates with Spotify using the official Spotify Web API and sends track information to the ESP32 over USB serial.

## Features

* 🎵 Displays currently playing Spotify track
* 🎤 Shows artist and song title
* 🔌 USB serial communication
* 📟 Supports 16x2 I²C LCD displays
* 🖥️ Cross-platform desktop application

  * Linux
  * Windows
  * macOS (planned)
* ⚡ Automatic ESP32 detection (planned)
* 🚀 One-command setup (planned)
* 🔄 Starts automatically on login (planned)

---

## Hardware Requirements

### Required Components

* ESP32 development board
* 16x2 I2C LCD display
* USB cable
* Computer running Spotify

### Wiring

| LCD | ESP32   |
| --- | ------- |
| VCC | 5V      |
| GND | GND     |
| SDA | GPIO 21 |
| SCL | GPIO 22 |

Default I²C address:

```text
0x27
```

---

## How It Works

```text
Spotify
   │
   ▼
Desktop Application
   │ USB Serial
   ▼
ESP32
   │ I²C
   ▼
LCD Display
```

The desktop application polls the Spotify Web API for playback information and sends updates to the ESP32 whenever the currently playing track changes.

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/USERNAME/spotify-display.git
cd spotify-display
```

### Python Dependencies

Using uv:

```bash
uv sync
```

Or with pip:

```bash
pip install -r requirements.txt
```

---

## Spotify API Setup

1. Visit the Spotify Developer Dashboard.
2. Create a new application.
3. Copy your:

   * Client ID
   * Client Secret
4. Add a Redirect URI:

```text
http://127.0.0.1:8888/callback
```

Create a `.env` file:

```env
SPOTIFY_CLIENT_ID=YOUR_CLIENT_ID
SPOTIFY_CLIENT_SECRET=YOUR_CLIENT_SECRET
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

---

## Flashing the ESP32

Open the firmware directory:

```bash
cd firmware
```

Upload using PlatformIO:

```bash
pio run --target upload
```

---

## Running

Linux:

```bash
python main.py
```

Windows:

```bash
python main.py
```

The first launch will open a browser window and request Spotify authorization.

After authentication, the application will automatically display the currently playing track on the LCD.

---

## Example Display

```text
The Weeknd
Blinding Lights
```

---

## Roadmap

### v1.0

* [x] ESP32 LCD support
* [x] Spotify Web API integration
* [x] USB serial communication
* [ ] CLI application + background service

### v1.1

* [ ] Automatic ESP32 detection
* [ ] Scrolling text for long titles
* [ ] Improved serial protocol

### v2.0

* [ ] CLI application
* [ ] One-command setup
* [ ] Automatic firmware flashing
* [ ] Service installation
* [ ] Auto-start on login

### Future Ideas

* Album artwork support
* OLED displays
* TFT displays
* Playback progress bar
* Volume display
* Spotify Connect device selection
* Multiple display themes

---

## License

MIT License

---

## Contributing

Contributions, bug reports, and feature requests are welcome.

Feel free to open an issue or submit a pull request.

---

## Disclaimer

This project is not affiliated with Spotify.

Spotify is a trademark of Spotify AB.
