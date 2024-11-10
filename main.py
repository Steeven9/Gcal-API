import os.path
from datetime import date

from fastapi import FastAPI
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

app = FastAPI()
# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
NUM_EVENTS = 10
CREDENTIALS_PATH = "/var/cal_data"


@app.get("/")
def read_root():
    return "Hello World"


@app.get("/events/{calendar_id}")
def read_item(calendar_id: str):
    events = get_calendar_events(calendar_id)
    print(f"Found {len(events)} events")
    return events


def get_calendar_events(calendar_id: str):
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists(CREDENTIALS_PATH + '/token.json'):
        creds = Credentials.from_authorized_user_file(
            CREDENTIALS_PATH + '/token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH + '/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(CREDENTIALS_PATH + '/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    events_result = service.events().list(
        calendarId=f"{calendar_id}@group.calendar.google.com",
        maxResults=NUM_EVENTS,
        singleEvents=True,
        timeMin=f"{date.today()}T00:00:00Z",
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return []

    event_list = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        event_list.append({"startTime": start, "title": event['summary']})

    return event_list
