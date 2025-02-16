import pygetwindow as gw
import time
import re
from pypresence import Presence
import ctypes

# constants
discord_client_id = "1219930243205173298"

# app initialization print
def print_app_initialization():
    print(" ┃ 🪧 initializing app...")

time.sleep(1)

def get_valid_deezer_windows():
    """
    filters windows to ensure only actual deezer app windows are selected.

    returns:
        list: a list of verified deezer windows.
    """
    all_windows = gw.getWindowsWithTitle("")  # get all windows
    valid_deezer_windows = []

    for window in all_windows:
        title = window.title.lower()

        # ensure it contains "deezer" but isn't a file explorer, vs code, or web browser
        if "deezer" in title and not any(
            x in title for x in ["explorer", "visual studio", "opera", "chrome", "firefox", "code"]
        ):
            valid_deezer_windows.append(window)

    return valid_deezer_windows

def prompt_user_for_window(windows):
    """
    prompts the user to choose a deezer window if multiple are detected.

    args:
        windows (list): a list of matching window objects.
    
    returns:
        window: the selected deezer window.
    """
    print("\n ┃ 🔍 multiple valid deezer windows detected. please select one:")
    for idx, window in enumerate(windows):
        print(f" ┃ [{idx + 1}] {window.title}")

    while True:
        try:
            choice = int(input(" ┃ ➡ enter the number of your choice: ")) - 1
            if 0 <= choice < len(windows):
                return windows[choice]
            else:
                print(" ┃ ⚠️ invalid choice. please enter a valid number.")
        except ValueError:
            print(" ┃ ⚠️ invalid input. please enter a number.")

def format_deezer_title(raw_title: str) -> str:
    """
    cleans and formats the title of the current track from deezer.
    removes extraneous parts such as track length and any curly brackets.

    args:
        raw_title (str): the title string from the deezer window.
        
    returns:
        str: the cleaned and formatted track title.
    """
    title_parts = raw_title.split(" - ")

    # remove the track duration if present
    formatted_title = (" - ".join(title_parts[:-1]) if len(title_parts) > 1 else raw_title)

    # remove any curly-bracketed text (e.g., album or artist information)
    formatted_title = re.sub(r"\{.*?\}", "", formatted_title).strip()

    return formatted_title

def update_discord_presence(deezer_window):
    """
    connects to discord and updates the user's rich presence status based on the deezer window.

    args:
        deezer_window (window): the deezer window object to extract track information.
    """
    rpc = Presence(discord_client_id)
    rpc.connect()

    print(" ┃ 🌟 updating discord rich presence...")

    last_title = None  # store last known song title

    while True:
        try:
            window_title = deezer_window.title
            clean_title = format_deezer_title(window_title)

            # only update if the title has changed
            if clean_title and clean_title != last_title:
                rpc.update(details="🎧 Listening to deezer", state=f"🎶 {clean_title}")
                print(f" ┃ 🎧 updated discord presence: {clean_title}")
                last_title = clean_title  # update last known title

            time.sleep(1)  # check title every second without flooding console

        except Exception as error:
            print(f" ┃ ❌ error updating discord presence: {error} ❌")
            break

def main():
    """
    main function to initialize deezer window detection and start discord presence update.
    """

    
    ctypes.windll.kernel32.SetConsoleTitleW("Deezer RPC | v0.0.1")
    print(" ┃ 🔍 searching for deezer windows...")
    deezer_windows = get_valid_deezer_windows()

    if not deezer_windows:
        print(" ┃ ⚠️ deezer window not detected. please open deezer and start playing a track.")
        return

    # ask user for auto or manual mode
    while True:
        mode_choice = input(" ┃ 🔄 select mode: [a]uto-detect / [m]anual selection: ").strip().lower()
        if mode_choice in ['a', 'm']:
            break
        print(" ┃ ⚠️ invalid choice. please enter 'a' or 'm'.")

    if mode_choice == 'a':
        print(" ┃ 🚀 auto-detect mode selected. using first detected deezer window.")
        selected_window = deezer_windows[0]
    else:
        selected_window = prompt_user_for_window(deezer_windows)

    print(f" ┃ 🎶 using window: {selected_window.title}")
    update_discord_presence(selected_window)

if __name__ == "__main__":

    print_app_initialization()
    main()
    
