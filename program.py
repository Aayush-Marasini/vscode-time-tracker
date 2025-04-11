import logging
import os
import pickle
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up logging
logging.basicConfig(filename='tracker.log', level=logging.INFO)

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Set the credentials file path
CREDENTIALS_FILE = 'time-tracker-401501-39012fa9fee5.json'


# Function to authenticate with Google
def authenticate():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens.
    # It is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds


# Function to create a calendar event
def create_event(service, event_title, event_duration):
    # Calculate event end time based on duration
    start_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    end_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(time.time() + event_duration * 60))

    event = {
        'summary': event_title,
        'start': {
            'dateTime': start_time,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'UTC',
        },
    }

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        logging.info(f"Event created: {event.get('htmlLink')}")
        print(f"Event created: {event.get('htmlLink')}")
    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        print(f"An error occurred: {error}")


# Main tracking logic
def track_time():
    creds = authenticate()
    try:
        service = build('calendar', 'v3', credentials=creds)
    except HttpError as error:
        logging.error(f"An error occurred while creating the service: {error}")
        print(f"An error occurred: {error}")
        return

    # Example: Track for 1 hour of coding time (this can be dynamically set)
    event_title = "VS Code Work Session"
    event_duration = 60  # in minutes

    create_event(service, event_title, event_duration)


if __name__ == '__main__':
    track_time()

