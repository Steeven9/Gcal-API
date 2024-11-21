# Gcal-API

Simple API to fetch events from a Google Calendar using their API
and OAuth authentication.

Requires `google-auth` `google-auth-oauthlib` `google-api-python-client` `fastapi[standard]`

Needs a Google Calendar API key as env variable `GCAL_API_KEY`.

## Installation

```bash
python -m venv .venv
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
