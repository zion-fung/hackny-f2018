from datetime import datetime, timezone
import math
import pytz
from google.transit import gtfs_realtime_pb2
import requests
import time # imports module for Epoch/GMT time conversion
import os # imports package for dotenv
from dotenv import load_dotenv, find_dotenv # imports module for dotenv
load_dotenv(find_dotenv()) # loads .env from root directory
import json

# The root directory requires a .env file with API_KEY assigned/defined within
# and dotenv installed from pypi. Get API key from http://datamine.mta.info/user
api_key = "15e022850d4f853819c83dc0fe9bb4b5"

# Requests subway status data feed from City of New York MTA API
from protobuf_to_dict import protobuf_to_dict
def get_train_data(feed_id):
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get('http://datamine.mta.info/mta_esi.php?key={}&feed_id={}'.format(api_key, feed_id))
    feed.ParseFromString(response.content)
    subway_feed = protobuf_to_dict(feed) # subway_feed is a dictionary
    # it has both entity and header keys
    try:
        realtime_data = subway_feed['entity'] # train_data is a list
    except KeyError:
        realtime_data = subway_feed # if entity does not exist then it's just a list
    return realtime_data

# This function takes a converted MTA data feed and a specific station ID and
# loops through various nested dictionaries and lists to (1) filter out active
# trains, (2) search for the given station ID, and (3) append the arrival time
# of any instance of the station ID to the collected_times list
def station_time_lookup(train_data, station):
    collected_times = []
    ids = []
    for trains in train_data: # trains are dictionaries
        if trains.get('trip_update', False) != False:
            unique_train_schedule = trains['trip_update'] # train_schedule is a dictionary with trip and stop_time_update
            unique_arrival_times = unique_train_schedule['stop_time_update'] # arrival_times is a list of arrivals
            for scheduled_arrivals in unique_arrival_times: #arrivals are dictionaries with time data and stop_ids
                if scheduled_arrivals.get('stop_id', False) == station: 
                    time_data = scheduled_arrivals['arrival']
                    unique_time = time_data['time']
                    if unique_time != None:
                        collected_times.append(unique_time)
                        ids.append(trains["id"])
    return collected_times, ids

# collected_times = station_time_lookup(realtime_data, "701S")

# Sort the collected times list in chronological order (the times from the data
# feed are in Epoch time format)
# collected_times.sort()
def print_times(times):
    for time in times:
        tz = pytz.timezone('America/New_York')
        print(datetime.fromtimestamp(time, tz).strftime('%Y-%m-%d %H:%M:%S'))
# print_times(collected_times)
# valid feeds are 1, 26, 16, 21, 2, 11, 31, 36, 51
# more_data = get_train_data("21")
# print(get_train_data("36"))
def get_schedule(day, stop_id):
    f = json.loads(open("stop_times.json").read())
    schedule = f[stop_id][day]
    schedule.sort()
    return schedule

def get_late_times(schedule, real_time):
    # Subtracts two time strings in format HH:MM:SS
    def time_subtraction(time1, time2):
        times1 = time1.split(":")
        times2 = time2.split(":")
        seconds1 = int(times1[0]) * 3600 + int(times1[1]) * 60 + int(times1[2])
        seconds2 = int(times2[0]) * 3600 + int(times2[1]) * 60 + int(times2[2])
        difference_seconds = seconds2 - seconds1
        result = time.strftime('%H:%M:%S', time.gmtime(abs(difference_seconds)))
        if difference_seconds > 0:
            return "- " + result
        return result
    late_times = []
    start = 0
    schedule_times = len(schedule)
    scheduled_times = []
    for real in real_time:
        print("Getting late time for:", real)
        index = start
        while index < schedule_times and schedule[index] < real:
            index += 1
        # Get the time before
        index -= 1
        # If you end up comparing to the same scheduled time as the last one, move to the next
        print("Scheduled:", schedule[index])
        if len(scheduled_times) > 0:
            print("Previous Scheduled:", scheduled_times[-1])
            if str(schedule[index]) == str(scheduled_times[-1]):
                print("Incremented!")
                index += 1
        start = index
        difference = time_subtraction(real, schedule[index])
        scheduled_times.append(schedule[index])
        print("Difference:", difference)
        print("------------")
        late_times.append(difference)
    return late_times, scheduled_times