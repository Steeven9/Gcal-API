# Gcal-API

Simple API to fetch events from a Google Calendar using their API
and OAuth authentication.

Requires the packages `google-auth` `google-auth-oauthlib` `google-api-python-client` `fastapi[standard]`

Needs a Google Calendar API key as env variable `GCAL_API_KEY`.
Create it from <https://console.cloud.google.com/apis/api/calendar-json.googleapis.com/credentials>

## Installation

Note: on Debian/Ubuntu, you might need to run `sudo apt install python3-venv` first

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run in dev mode

```bash
fastapi dev main.py
```

## Run in prod mode

```bash
fastapi run
```
