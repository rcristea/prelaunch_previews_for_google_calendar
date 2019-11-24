from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import launch_event as le
from database_manager import post_launch_event

SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """
    Creates Google Calendar events for upcoming rocket events

    will also create MongoDB documents to enable deletion of events (if desired by the user)
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=50, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    launch_events = le.LaunchEvents()
    missions = launch_events.missions
    for mission in missions:
        summary = mission.mission_name
        location = mission.location
        description = mission.to_string()
        start_date_time = mission.date + 'T' + mission.start_time
        end_date_time = mission.date + 'T' + mission.end_time
        time_zone = 'Europe/London'

        if start_date_time[11:13] == "23" and end_date_time[11:13] == "00":
            end_date_time = mission.date + 'T' + '23:59:59'

        if mission.start_time != '00:00:00':
            launch_event = {
                'summary': summary,
                'location': location,
                'description': description,
                'start': {
                    'dateTime': start_date_time,
                    'timeZone': time_zone,
                },
                'end': {
                    'dateTime': end_date_time,
                    'timeZone': 'America/New_York',
                },
                'recurrence': [
                ],
                'attendees': [
                ],
                'reminders': {
                },
            }

            add_event = True

            for event in events:
                if event['summary'] == launch_event['summary']:
                    add_event = False

            if add_event:
                post_launch_event(mission.mission_name, mission.location, mission.lsp, mission.rocket_name,
                                  mission.date, mission.start_time, mission.end_time)
                # to play around with the code: comment out this line. This is what adds to your calendar
                launch_event = service.events().insert(calendarId='primary', body=launch_event).execute()


if __name__ == '__main__':
    main()
