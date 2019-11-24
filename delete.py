from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from database_manager import get_data_frame, delete_launch_event

"""
    ONLY RUN THIS FILE IF YOU WANT TO DELETE ALL OF THE LAUNCH ENTRIES IN YOUR MONGO DB FROM YOUR CALENDAR
"""


SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """
    Deletes Google Calendar events for upcoming rocket events

    will also delete MongoDB documents of the events that are deleted
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

    launch_events_on_calendar = get_data_frame()
    for event in events:
        remove_event = False
        query = {'mission_name': ''}
        for index, row in launch_events_on_calendar.iterrows():
            if event['summary'] == row['mission_name']:
                remove_event = True
                query = {'mission_name': row['mission_name']}

        if remove_event:
            # to delete events:
            delete_launch_event(query)
            service.events().delete(calendarId='primary', eventId=event['id']).execute()


if __name__ == '__main__':
    main()
