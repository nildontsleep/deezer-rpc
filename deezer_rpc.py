import pygetwindow as gw
import time
import re
import logging
import ctypes
import requests
from pypresence import Presence

# Configuration & Constants
DISCORD_CLIENT_ID = "1219930243205173298"
VERSION = "v2"
DEEZER_API_SEARCH_URL = "https://api.deezer.com/search?q="

# Configure logging
logging.basicConfig(
    filename="deezer_rpc.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialization Functions
def print_app_initialization():
    """Logs and prints app initialization message."""
    logging.info("Initializing app...")
    print(" ┃ 🪧 Initializing app...")

# Set console title
ctypes.windll.kernel32.SetConsoleTitleW(f"Deezer RPC | {VERSION}")
time.sleep(1)

# Window Detection Functions
def get_valid_deezer_windows():
    """Finds and filters valid Deezer application windows."""
    logging.info("Searching for Deezer windows...")
    all_windows = gw.getWindowsWithTitle("")
    
    # Improved detection (matches variations of Deezer window titles)
    valid_deezer_windows = [w for w in all_windows if "deezer" in w.title.lower() and " - " in w.title]

    logging.info(f"Found {len(valid_deezer_windows)} valid Deezer window(s)")
    return valid_deezer_windows

def prompt_user_for_window(windows):
    """Prompts the user to choose a Deezer window if multiple are detected."""
    print("\n ┃ 🔍 Multiple valid Deezer windows detected. Please select one:")
    for idx, window in enumerate(windows):
        print(f" ┃ [{idx + 1}] {window.title}")

    while True:
        try:
            choice = int(input(" ┃ ➡  Enter the number of your choice: ")) - 1
            if 0 <= choice < len(windows):
                return windows[choice]
            print(" ┃ ⚠️ Invalid choice. Please enter a valid number.")
        except ValueError:
            print(" ┃ ⚠️ Invalid input. Please enter a number.")

def format_deezer_title(raw_title: str) -> tuple:
    """Extracts song title and artist from the window title."""
    title_parts = raw_title.split(" - ")
    
    if len(title_parts) >= 2:
        song_title = title_parts[0].strip()
        artist_name = title_parts[1].strip()
    else:
        song_title, artist_name = raw_title, "Unknown"

    return song_title, artist_name

# Deezer API Fetch Function
def get_song_info(song_title: str, artist_name: str):
    """Fetches song details (cover, artist image, and song link) from Deezer API."""
    query = f"{artist_name} {song_title}"
    
    try:
        response = requests.get(DEEZER_API_SEARCH_URL + query)
        response.raise_for_status()
        data = response.json()

        if data["data"]:
            song = data["data"][0]
            return {
                "album_cover": song["album"]["cover_medium"],  # 250x250 px cover
                "artist_image": song["artist"]["picture_small"],  # Small artist image
                "song_link": song["link"]  # Direct song URL
            }
    except requests.RequestException as e:
        logging.error(f"Failed to fetch song info: {e}")

    return None  # Fallback to default values if API fails

# Discord Presence Function
def update_discord_presence(deezer_window):
    """Updates Discord Rich Presence with current Deezer track and album cover."""
    try:
        rpc = Presence(DISCORD_CLIENT_ID)
        rpc.connect()
        logging.info("Connected to Discord Rich Presence API.")
        print(" ┃ 🌟 Updating Discord Rich Presence...")
    except Exception as error:
        logging.error(f"Failed to connect to Discord: {error}")
        print(" ┃ ❌ Error: Unable to connect to Discord.")
        return

    last_title = None

    while True:
        try:
            window_title = deezer_window.title
            song_title, artist_name = format_deezer_title(window_title)

            if song_title and song_title != last_title:
                song_info = get_song_info(song_title, artist_name)

                if song_info:
                    cover_url = song_info["album_cover"]
                    artist_url = song_info["artist_image"]
                    song_link = song_info["song_link"]
                    rpc.update(
                        details=f"🎧 Listening to {song_title}",
                        state=f"🎤 {artist_name}",
                        large_image=cover_url,
                        large_text="Deezer",
                        small_image=artist_url,
                        small_text=artist_name,
                        buttons=[
                            {"label": "🎵 Listen on Deezer", "url": song_link}  # Deezer track link
                        ]
                    )

                    logging.info(f"Updated Discord: {song_title} by {artist_name}")
                    print(f" ┃ 🎧 Updated Discord: {song_title} by {artist_name}")

                last_title = song_title

            time.sleep(1)
        except Exception as error:
            logging.error(f"Error updating Discord presence: {error}")
            print(f" ┃ ❌ Error updating Discord presence: {error}")
            break

# Main Execution Function
def main():
    """Main function to initialize window detection and update Discord presence."""
    ctypes.windll.kernel32.SetConsoleTitleW(f"Deezer RPC | {VERSION}")
    print(" ┃ 🔍 Searching for Deezer windows...")
    
    deezer_windows = get_valid_deezer_windows()
    if not deezer_windows:
        logging.warning("No Deezer window detected.")
        print(" ┃ ⚠️ Deezer window not detected. Please open Deezer and start playing a track.")
        return
    
    # Mode selection
    while True:
        mode_choice = input(" ┃ 🔄 Select mode: [A]uto-detect / [M]anual selection: ").strip().lower()
        if mode_choice in ['a', 'm']:
            break
        print(" ┃ ⚠️ Invalid choice. Please enter 'A' or 'M'.")

    if mode_choice == 'a':
        print(" ┃ 🚀 Auto-detect mode selected. Using first detected Deezer window.")
        selected_window = deezer_windows[0]
    else:
        selected_window = prompt_user_for_window(deezer_windows)

    print(f" ┃ 🎶 Using window: {selected_window.title}")
    logging.info(f"Using Deezer window: {selected_window.title}")

    update_discord_presence(selected_window)

# Program Entry Point
if __name__ == "__main__":
    print_app_initialization()
    main()
