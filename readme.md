**Prelaunch Previews for Google Calendar**
-
Prelaunch Previes for Google Calendar is an app to add the contents of:
[PreLaunch-Previews](https://everydayastronaut.com/prelaunch-previews/) to your google calendar.<br>
****
**Setup**
1. Go to [Calendar API quickstart](https://developers.google.com/calendar/quickstart/python) and click 'Enable the Google Calendar API'<br>
2. Click 'DOWNLOAD CLIENT CONFIGURATION'
3. Add to the same directory as this project
4. Run start.py; this will open your browser and ask you to log into your google account
5. The app isn't verified so show Advanced and click Go to start(unsafe)... Don't worry, its safe. I don't even know
how to write a virus
6. Click allow to grant permission for this application to modify your calendar (will never delete anything)<br>
[subject to change since a feature to remove the events may be added in]
7. Click allow again to confirm changes. This will open a page that should say "The authentication flow has completed. 
You may close this window." This is to generate the token.pickle file (used for authentication)
****
**MongoDB**<br>
Create a free [MongoDatabase](https://docs.atlas.mongodb.com/getting-started/)<br>
You do not need to insert your own data. Once you are finished creating your database click back on clusters on the left
navigation menu and click 'CONNECT' on the cluster you want to use for this program. Click 'Connect your Application'
select your driver version (this program was written with python 3.7.5). Then copy the connection string. Go to
database_manager.py and replace 'REPLACE_CONNECTION_STRING' with the one you just copied. Make sure you replace
<password> with the admin password of the data base (not the password that you use to log into MongoDB). After that you
should be good to go.

If you do not want to deal with MongoDB the only thing affected will be deleting the events that were put in by the
calendar. In this case:
1. delete delete.py
2. delete database_manager.py
3. delete `from database_manager import post_launch_event` from start.py
4. delete `post_launch_event(mission.mission_name, mission.location, mission.lsp, mission.rocket_name, mission.date, mission.start_time, mission.end_time)`
from start.py
****
**Running the program**<br>
In start.py, assuming you didn't delete anything, on line 68 you must put in your own time zone. Use
[this](http://www.timezoneconverter.com/cgi-bin/zonehelp.tzc?cc=US&ccdesc=United%20States) for reference. After that's
done, run start.py and your Google calendar should populate with all the current rocket launch announcements.<br>
****
**Bugs**
1. No in-program fix for events that are updated. My "fix" is just how I'm running the program. I have a raspberryPi that
runs delete.py and start.py once a day. So first delete.py runs to clear all the old events, then runs start.py after 
delete.py finishes. This refreshes with all the new information.
2. If it looks like some events are not being deleted you are apparently a very busy person. You have to go into both
start.py and delete.py and replace the part that says ` maxResults=50` to any number that is above 50. This is the number
of events that the program will read into the program and your calendar went above that number.