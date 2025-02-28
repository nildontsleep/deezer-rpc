import pygetwindow as gw
import time
import re
import logging
import ctypes
from pypresence import Presence

# Configuration & Constants
DISCORD_CLIENT_ID = "1219930243205173298"
VERSION = "v1"

# Configure logging to store logs in a file
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
    valid_deezer_windows = []

    for window in all_windows:
        title = window.title.lower()
        if "deezer" in title and not any(
            x in title for x in ["explorer", "visual studio", "opera", "chrome", "firefox", "code", VERSION]
        ):
            valid_deezer_windows.append(window)
    
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

# Title Formatting Function

def format_deezer_title(raw_title: str) -> str:
    """Cleans and formats the track title from the Deezer window."""
    title_parts = raw_title.split(" - ")
    formatted_title = (" - ".join(title_parts[:-1]) if len(title_parts) > 1 else raw_title)
    formatted_title = re.sub(r"\{.*?\}", "", formatted_title).strip()
    return formatted_title

# Discord Presence Function

def update_discord_presence(deezer_window):
    """Updates Discord Rich Presence with current Deezer track information."""
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
            clean_title = format_deezer_title(window_title)
            
            if clean_title and clean_title != last_title:
                rpc.update(details="🎧 Listening to Deezer", state=f"🎶 {clean_title}")
                logging.info(f"Updated Discord presence: {clean_title}")
                print(f" ┃ 🎧 Updated Discord presence: {clean_title}")
                last_title = clean_title
            
            time.sleep(1)  # Prevent excessive calls
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
