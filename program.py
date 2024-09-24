import psutil
import time
import datetime
import win32gui
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Define the process name of VS Code
vscode_process_name = "Code.exe"

# Initialize a variable to track if VS Code is currently open
vscode_open = False

# Load Google Calendar API credentials
credentials = service_account.Credentials.from_service_account_file(r"time-tracker-401501-39012fa9fee5.json", scopes=['https://www.googleapis.com/auth/calendar'])




# Create a Calendar service
service = build('calendar', 'v3', credentials=credentials)

while True:
    # Get a list of running processes
    running_processes = psutil.process_iter(attrs=['pid', 'name'])

    for process in running_processes:
        if process.info['name'] == vscode_process_name:
            # Check if VS Code is not already open
            if not vscode_open:
                # VS Code has been opened, record the timestamp
                vs_code_start_time = datetime.datetime.now()
                print(f"VS Code opened at {vs_code_start_time}")
                vscode_open = True
            break
    else:
        # If no VS Code process is found, reset the open flag
        if vscode_open:
            # VS Code was closed, calculate usage time
            vs_code_end_time = datetime.datetime.now()
            vs_code_usage_time = vs_code_end_time - vs_code_start_time

            # Create a Google Calendar event for VS Code usage
            event = {
                'summary': 'VS Code Usage',
                'description': 'Time spent on VS Code',
                'start': {
                    'dateTime': vs_code_start_time.isoformat(),
                    'timeZone': 'Asia/Kathmandu',
                },
                'end': {
                    'dateTime': vs_code_end_time.isoformat(),
                    'timeZone': 'Asia/Kathmandu',
                },
            }

            # Upload the event to Google Calendar
            #Enter your email here in calendarId
            service.events().insert(calendarId='', body=event).execute()
            print(f"VS Code closed at {vs_code_end_time}, Time spent: {vs_code_usage_time}")
            vscode_open = False

    # Check if VS Code is currently focused
    hwnd = win32gui.GetForegroundWindow()
    window_title = win32gui.GetWindowText(hwnd)
    if "Visual Studio Code" in window_title:
        vscode_open = True
    else:
        vscode_open = False

    time.sleep(1)  # Sleep for 1 second before checking again
