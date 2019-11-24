from pymongo import MongoClient
import pandas as pd

connect = 'REPLACE_CONNECTION_STRING'
client = MongoClient(connect)
db = client.launch_previews
launch_events = db.launch_previews


def post_launch_event(mission_name, location, lsp, rocket_name, date, start_time, end_time):
    """
    Posts a new launch event to the connected Mongo Database
    :param mission_name: the name of the mission
    :param location: where the rocket will launch
    :param lsp: the launch service provider
    :param rocket_name: the name of the rocket
    :param date: the date of the launch
    :param start_time: the start time of the launch
    :param end_time: the end time of the launch
    """
    event = {
        'mission_name': mission_name,
        'location': location,
        'lsp': lsp,
        'rocket_name': rocket_name,
        'date': date,
        'start_time': start_time,
        'end_time': end_time
    }

    launch_events.insert_one(event)


def delete_launch_event(query):
    """
    Deletes the document matching the query
    :param query: the document to be deleted
    """
    launch_events.delete_one(query)


def get_data_frame():
    """
    Creates a DataFrame of the launch_events
    :return: the DataFrame
    """
    return pd.DataFrame(launch_events.find())
