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

### Wiring (For DEVKITV1)

Check for equivalents if not the same type of ESP32 (for eg. D is sometimes replaced by GPIO)

| LCD | ESP32   |
| --- | ------- |
| VCC | VIN     |
| GND | GND     |
| SDA | D21     |
| SCL | D22     |

Default I2C address:

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
git clone https://github.com/SabeeirSharrma/Mini-Spotify-ESP32.git
cd Mini-Spotify-ESP32
```

### Python Dependencies

Using uv:

```bash
cd Python
uv sync
```

Or with pip:

```bash
cd Python
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
5. Under APIs used, enable: Web API and Web Playback SDK

Create a `.env` file:

```env
SPOTIFY_CLIENT_ID=YOUR_CLIENT_ID
SPOTIFY_CLIENT_SECRET=YOUR_CLIENT_SECRET
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

---

## Flashing the ESP32

1. In VSCode, install the PlatformIO extension and create a new project
2. In the new project you will see `platformio.ini` and in the `src` folder, `main.cpp` (create one if you don't see it)
3. Copy the `platformio.ini` and `main.cpp` from the `ESP32` folder

---

## Running

Linux:

```bash
cd Python
python main.py
```

Windows:

```bash
cd Python
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
* [ ] Scrolling text for long titles
* [ ] Auto-start on login

### v1.1

* [ ] Automatic ESP32 detection
* [ ] Improved serial protocol

### v2.0

* [ ] One-command setup
* [ ] Automatic firmware flashing

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
