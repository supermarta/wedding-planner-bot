from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json'

def check_availability(date_str):
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=credentials)

    time_min = datetime.fromisoformat(date_str)
    time_max = time_min + timedelta(hours=2)

    events = service.events().list(
        calendarId='primary',
        timeMin=time_min.isoformat() + 'Z',
        timeMax=time_max.isoformat() + 'Z',
        singleEvents=True
    ).execute()

    return len(events.get('items', [])) == 0
