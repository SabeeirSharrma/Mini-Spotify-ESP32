import time
import serial
import spotipy

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import os

# -------------------------
# CONFIG
# -------------------------

SERIAL_PORT = "COM3"      # Windows

# SERIAL_PORT = "/dev/ttyUSB0"   # Linux
# SERIAL_PORT = "/dev/ttyACM0"   # Linux alternative

BAUDRATE = 115200

# -------------------------
# LOAD ENV
# -------------------------

load_dotenv()

# -------------------------
# SPOTIFY AUTH
# -------------------------

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope="user-read-currently-playing user-read-playback-state",
    )
)

# -------------------------
# SERIAL
# -------------------------

print(f"Connecting to {SERIAL_PORT}...")

ser = serial.Serial(
    SERIAL_PORT,
    BAUDRATE,
    timeout=1
)

time.sleep(2)

print("Connected.")
print("Waiting for Spotify playback...")

# -------------------------
# STATE
# -------------------------

last_track_id = None

# -------------------------
# MAIN LOOP
# -------------------------

while True:
    try:
        playback = sp.current_playback()

        if playback is None:
            time.sleep(2)
            continue

        item = playback.get("item")

        if item is None:
            time.sleep(2)
            continue

        track_id = item["id"]

        if track_id != last_track_id:
            song = item["name"]

            artists = [
                artist["name"]
                for artist in item["artists"]
            ]

            artist_text = ", ".join(artists)

            print()
            print("Now Playing")
            print("Artist:", artist_text)
            print("Song  :", song)

            ser.write(f"1:{artist_text}\n".encode("utf-8"))
            time.sleep(0.05)

            ser.write(f"2:{song}\n".encode("utf-8"))
            time.sleep(0.05)

            last_track_id = track_id

        time.sleep(2)

    except KeyboardInterrupt:
        print("\nExiting...")
        break

    except Exception as e:
        print("Error:", e)
        time.sleep(5)

ser.close()