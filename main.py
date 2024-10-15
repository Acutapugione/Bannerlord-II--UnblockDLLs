import os
import subprocess

# Define paths based on Steam and GOG installation locations (adjust these if needed)
steam_install_path = (
    r"C:\Program Files (x86)\Steam\steamapps\common\Mount & Blade II Bannerlord"
)
gog_install_path = r"C:\GOG Games\Mount & Blade II Bannerlord"

# Error message variable
error_message = ""

# Check administrator privileges
if not os.getuid() == 0:
    print("This script requires administrator privileges. Please run it with sudo.")
    exit(1)

# Find game installation directory
game_found = False
if os.path.isdir(steam_install_path):
    game_path = steam_install_path
    game_found = True
elif os.path.isdir(gog_install_path):
    game_path = gog_install_path
    game_found = True
else:
    # Prompt user to select directory if not found automatically
    # print()
    game_path = input(
        "Game directory not found. Please select the Mount & Blade II Bannerlord directory:\n"
    )  # "/home/acuta/Games/bannerlord-2/drive_c/GOG Games/Mount & Blade II Bannerlord/"  #
    print(f"{os.path.isdir(game_path)=}")
    if os.path.isdir(game_path):
        game_found = True
if game_found:
    print("Checking files. Please wait...")

    # Find all subdirectories within the Modules folder
    all_folders = [
        os.path.join(game_path, "Modules", root)
        for root, _, _ in os.walk(os.path.join(game_path, "Modules"))
    ]

    # Find blocked DLL files
    blocked_files = []
    for folder in all_folders:
        try:
            for filename in os.listdir(folder):
                if filename.endswith(".dll") and os.access(
                    os.path.join(folder, filename), os.R_OK and not os.W_OK
                ):
                    blocked_files.append(os.path.join(folder, filename))
        except OSError as e:
            error_message += f"\nError accessing directory: {e}"

    if blocked_files:
        # Unblock DLL files (uppercase names only)
        for file in blocked_files:
            if any(char.isupper() for char in file):
                try:
                    os.chmod(file, os.stat(file).st_mode | os.W_OK)
                except Exception as e:
                    error_message += f"\nError unblocking file {file}: {e}"

        print("Successfully unblocked the following files:")
        for file in blocked_files:
            print(file)

    else:
        print("No locked files found. Everything is okay.")

else:
    print("Game directory not found or incorrect. Please verify the installation.")

if error_message:
    print("\nErrors encountered:")
    print(error_message)

print("Exiting...")
