import flet as ft
from pathlib import Path
from src.ui import UserInterface
from src.core import resource_path
import json
import requests
import uuid
import sys
import webbrowser # Import the webbrowser module
import threading # Import the threading module

# Get the HWID of the current machine
def get_hwid():
    return str(uuid.getnode())

# Check if the HWID is valid and not expired
def check_hwid(hwid):
    # Get the JSON file from GitHub
    url = "https://raw.githubusercontent.com/remohotaf/remo-jest-hot/main/hwid.json"
    response = requests.get(url)
    data = json.loads(response.text)
    # Loop through the users in the JSON file
    for user in data["users"]:
        # If the HWID matches, check the expiration date
        if user["hwid"] == hwid:
            expiration_date = user["expiration_date"]
            # If the expiration date is not empty, compare it with the current date and time
            if expiration_date:
                from datetime import datetime
                current_datetime = datetime.now()
                # Convert the expiration date to a datetime object
                expiration_datetime = datetime.strptime(expiration_date, "%Y-%m-%d %H:%M")
                # If the current datetime is before or equal to the expiration datetime, return True and print the username and when the license will expire
                if current_datetime <= expiration_datetime:
                    print(f"Hello {user['username']}. Your license will expire on {expiration_datetime.strftime('%Y-%m-%d %H:%M')}.")
                    return True
                # Otherwise, return False and print when the license expired
                else:
                    print(f"License expired on {expiration_datetime.strftime('%Y-%m-%d %H:%M')}.")
                    return False
            # If the expiration date is empty, return True and print the username
            else:
                print(f"Hello {user['username']}. Your license has no expiration date.")
                return True
    # If the HWID is not found, return False
    return False

# Define a function that will run in a background thread and check the HWID periodically and exit the program if it is invalid or expired
def check_hwid_thread(hwid):
    # Set an interval in seconds for checking the HWID (e.g. 10 minutes = 600 seconds)
    interval = 600 
    # Create an infinite loop that will run until the program exits
    while True:
     # Check if the HWID is valid and not expired using the check_hwid function
result = check_hwid(hwid)
# Print the result
if result:
    print("HWID is valid and not expired.")
else:
    print("HWID is invalid or expired.")
    # Exit the program if HWID is invalid or expired
    sys.exit()
# Wait for the interval before checking again using the time.sleep function
time.sleep(interval)

def main():
    # Get the current HWID
    hwid = get_hwid()
    # Check if the HWID is valid and not expired
    result = check_hwid(hwid)
    # Print the result
    if result:
        print("HWID is valid and not expired.")
        # Run your original code if HWID is valid and not expired
        if Path(resource_path("accounts.json", True)).exists():
            pass
        else:
            with open(resource_path("accounts.json", True), "w") as f:
                f.write(json.dumps([{"username": "Your Email", "password": "Your Password"}], indent=4))
        # Create a background thread that will run the check_hwid_thread function with hwid as an argument using threading module 
        t = threading.Thread(target=check_hwid_thread, args=(hwid,))
        # Set the thread as daemon so it will terminate when the main thread exits 
        t.setDaemon(True)
        # Start the thread 
        t.start()
        # Run this link every time you launch the program using webbrowser module 
        webbrowser.open("https://www.tiktok.com/@remo_zadymiarz")
        # Run your flet app after creating and starting the background thread 
        ft.app(target=UserInterface, assets_dir=resource_path("assets"))
        else:
    print("HWID is invalid or expired.")
    # Print the HWID and ask if the user wants to close the program if HWID is invalid or expired
    print(f"Your HWID is {hwid}.")
    answer = input("Do you want to close the program? (Y/N): ")
    # If the answer is yes, exit the program
    if answer.lower() == "y":
        sys.exit()
