from datetime import date
from os import getenv

from fastapi import FastAPI
from googleapiclient.discovery import build

app = FastAPI()

API_KEY = getenv("GCAL_API_KEY")
NUM_EVENTS = 10


@app.get("/")
def read_root():
    return "Hello World"


@app.get("/events/{calendar_id}")
def read_item(calendar_id: str):
    events = get_calendar_events(calendar_id)
    print(f"Found {len(events)} events")
    return events


def get_calendar_events(calendar_id: str):
    service = build('calendar', 'v3', developerKey=API_KEY)

    try:
        events_result = service.events().list(
            calendarId=f"{calendar_id}@group.calendar.google.com",
            maxResults=NUM_EVENTS,
            singleEvents=True,
            timeMin=f"{date.today()}T00:00:00Z",
            orderBy='startTime').execute()
        events = events_result.get('items', [])
    except Exception as e:
        print(f"Error accessing calendar: {e}")
        return {"error": "Unable to access calendar"}

    if not events:
        print('No upcoming events found.')
        return []

    event_list = []
    for event in events:
        if "compleanno" not in event['summary'].lower():
            start = event['start'].get('dateTime', event['start'].get('date'))
            event_list.append({"startTime": start, "title": event['summary']})

    return event_list
