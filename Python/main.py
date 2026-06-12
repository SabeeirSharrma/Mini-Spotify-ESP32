import time
import socket
import unicodedata
import serial
import spotipy

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from requests.exceptions import ConnectionError, Timeout
from spotipy.exceptions import SpotifyException
import os

# Config

# SERIAL_PORT = "COM3"      # Windows

SERIAL_PORT = "/dev/ttyUSB0"   # Linux
# SERIAL_PORT = "/dev/ttyACM0"   # Linux alternative

BAUDRATE = 115200

POLL_INTERVAL = 2          # seconds between Spotify polls
RECONNECT_INTERVAL = 5     # seconds between connectivity checks

load_dotenv()


# Helpers

def create_spotify_client():
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
            scope="user-read-currently-playing user-read-playback-state",
        )
    )


def has_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.close()
        return True
    except OSError:
        return False


def wait_for_internet():
    print("Waiting for internet connection...")

    while True:
        if has_internet():
            print("Internet connection restored.")
            return
        time.sleep(RECONNECT_INTERVAL)


def sanitize_for_lcd(text):
    # NFKD decomposition splits e.g. 'é' into 'e' + combining acute accent
    decomposed = unicodedata.normalize("NFKD", text)

    # Keep only ASCII characters (the combining marks are non-ASCII and get dropped)
    return decomposed.encode("ascii", errors="ignore").decode("ascii")


# Spotify Auth

sp = create_spotify_client()


# Serial

print(f"Connecting to {SERIAL_PORT}...")

ser = serial.Serial(
    SERIAL_PORT,
    BAUDRATE,
    timeout=1
)

time.sleep(2)

print("Connected.")
print("Waiting for Spotify playback...")


# State

last_track_id = None


# Main Loop

while True:
    try:
        playback = sp.current_playback()

        if playback is None:
            time.sleep(POLL_INTERVAL)
            continue

        item = playback.get("item")

        if item is None:
            time.sleep(POLL_INTERVAL)
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

            lcd_artist = sanitize_for_lcd(artist_text)
            lcd_song = sanitize_for_lcd(song)

            ser.write(f"1:{lcd_artist}\n".encode("utf-8"))
            time.sleep(0.05)

            ser.write(f"2:{lcd_song}\n".encode("utf-8"))
            time.sleep(0.05)

            last_track_id = track_id

        time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\nExiting...")
        break

    except (ConnectionError, Timeout, OSError) as e:
        print(f"\nLost connection to Spotify API: {e}")
        wait_for_internet()
        print("Reconnecting to Spotify...")
        sp = create_spotify_client()
        print("Reconnected. Resuming playback polling...")

    except SpotifyException as e:
        print(f"\nSpotify API error: {e}")

        if e.http_status in (502, 503, 504):
            # Server-side issue — wait for connectivity and retry
            wait_for_internet()
            print("Reconnecting to Spotify...")
            sp = create_spotify_client()
            print("Reconnected. Resuming playback polling...")
        else:
            # Other API errors (rate limit, auth, etc.) — brief pause and retry
            print(f"Retrying in {RECONNECT_INTERVAL}s...")
            time.sleep(RECONNECT_INTERVAL)

ser.close()