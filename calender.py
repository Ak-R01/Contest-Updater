import os.path
from pathlib import Path
from datetime import datetime , timezone , timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from contests_getter import get_data
from contests_getter import notify_mako

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

CONFIG_DIR = Path(os.environ.get("XDF_CONFIG_HOME",Path.home() / ".config")) / "contest-updater"
DATA_DIR = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")) / "contest-updater"

CREDENTIALS_FILE = CONFIG_DIR / "credentials.json"
TOKEN_FILE = DATA_DIR / "token.json"

CONFIG_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

def add_or_update_contest(service, contest , calendar_id="primary"):
  event_id =f"cfcontest{contest['id']}"
  start = datetime.fromtimestamp(contest["startTimeSeconds"],tz = timezone.utc)
  end = start + timedelta(seconds=contest["durationSeconds"])
  body = {
    "id": event_id,
    "summary": contest["name"],
    "description": f"https://codeforces.com/contests/{contest['id']}",
    "start": {"dateTime": start.isoformat()},
    "end": {"dateTime": end.isoformat()},
  }
  # print(contest,"\n")
  # print(body)
  # print("**************************************")
  try:
    service.events().insert(calendarId=calendar_id,body = body).execute()
    notify_mako("Contest Added to Calendar",contest["name"],timeout="10000")
  except HttpError as e:
    if e.resp.status == 409:
      body.pop("id")
      service.events().patch(eventId=event_id,calendarId=calendar_id,body=body).execute()
      print(f"Updated {contest['name']}")
    else:
      raise


def main():
  creds = None
  if os.path.exists(TOKEN_FILE):
    creds = Credentials.from_authorized_user_file(TOKEN_FILE,SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      print("Access token expired. Refreshing token using Google")
      creds.refresh(Request())
    else:
      print("No valid token found, Opening browser for one-time token generation")
      flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE,SCOPES)
      creds = flow.run_local_server(port=0)
    with open(TOKEN_FILE,'w') as token:
      token.write(creds.to_json())
  try:
    service = build('calendar','v3',credentials=creds)
    print("Fetching Contest Data")
    contests = get_data()
    for contest in contests:
      try:
        add_or_update_contest(service=service,contest=contest)
      except HttpError as e:
        notify_mako(f"Failed on {contest['name']}",str(e),urgency="critical")

    # event = service().events().insert(calendarId='primary',body=event_body).execute()
  except HttpError as error:
      notify_mako("Error Connecting to Calendar",str(error),"10000","critical")

if __name__ == '__main__':
  main()
