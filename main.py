from flask import Flask, request, jsonify, render_template
from datetime import datetime, timezone
from math import cos, asin, sqrt
import pytz
import pandas
import mta
from flask_cors import CORS
from fuzzywuzzy import fuzz

app = Flask(__name__)
CORS(app)
train_data = {}

# @app.route("/")
# def hello_world():
#     return "Hello world"
@app.route("/station-line-stripped", methods=["POST"])
def get_line_feed():
    params = request.get_json(force=True)
    train_data = mta.get_train_data(params["feed_id"])
    return jsonify(mta.get_train_data(params["feed_id"]))

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route('/api/distance')
def distance():
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    stop = closest_station(latitude, longitude)
    print(stop)
    return stop

@app.route("/train-status", methods=["POST", "GET"])
def change_status():
    if request.method == "POST":
        params = request.get_json(force=True)
        train_id = params["train_id"]
        status = params["status"]
        if train_id in train_data:
            if status:
                train_data[train_id] += 1
            else:
                train_data[train_id] -= 1
        else:
            if status:
                train_data[train_id] = 1
            else:
                train_data[train_id] = -1
        return str(train_data[train_id])
    else:
        train_id = int(request.args.get("train_id"))
        print("Searching:", train_id)
        print(train_data)
        print(train_id in train_data)
        return get_train_score(train_id)

def get_train_score(train_id):
    try:
        return str(train_data[train_id])
    except KeyError:
        return "DNE"
# User will give a line feed and a station id
@app.route("/station-line-info", methods=["POST"])
def get_all():
    # valid feeds are 1, 26, 16, 21, 2, 11, 31, 36, 51
    params = request.get_json(force=True)
    train_data = mta.get_train_data(params["feed_id"])
    # Now includes train id
    station_data = mta.station_time_lookup(train_data, params["station_id"])
    # print(station_data)
    station_times = station_data[0]
    ids = station_data[1]
    data = {
        "station_times": [],
        # "schedule_times": mta.get_schedule("Saturday", params["station_id"]),
        "schedule_times": [],
        "late_times": []
    }
    for time in station_times:
        # Convert from epoch to human time
        data["station_times"].append(epoch_to_time(time))
    data["station_times"].sort()
    # returns a tuple with the late times and the scheduled times
    late_times = mta.get_late_times(mta.get_schedule("Sunday", params["station_id"]), data["station_times"])
    # print(late_times)
    data["late_times"] = late_times[0]
    data["schedule_times"] = late_times[1]
    response = []
    for index in range(len(data["station_times"])):
        train_id = ids[index]
        score = get_train_score(int(train_id))
        print(score)
        response.append({"predicted": data["station_times"][index], "scheduled": data["schedule_times"][index], "difference": data["late_times"][index], "id": train_id, "score": score})
    return jsonify(response)


# https://stackoverflow.com/questions/41336756/find-the-closest-latitude-and-longitude
def haversine(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))


def closest_station(latitude, longitude):
    data = pandas.read_csv("Stations.csv")
    min_dist = 1000000000
    stop_id = ""
    for index, row in data.iterrows():
        hav_dist = haversine(latitude, longitude,
                             float(row["GTFS Latitude"]), float(row["GTFS Longitude"]))
        if hav_dist < min_dist:
            min_dist = hav_dist
            stop_id = getattr(row, "GTFS Stop ID")
    return stop_id


def epoch_to_time(time):
    tz = pytz.timezone('America/New_York')
    return datetime.fromtimestamp(time, tz).strftime('%H:%M:%S')

locations = {"start":"", "end":""}
@app.route('/autofill')
def station():
    param = request.args.get("start")
    resp_type = request.args.get("type")
    if resp_type == "start":
        locations["start"] = fuzziest_station(param);
    else:
        locations["end"] = fuzziest_station(param);
    print(param)
    return param

@app.route("/locations")
def get_locations():
    # print(start, end)
    # print(locations)
    # loc = {"start": start, "end": end}
    return jsonify(locations)

def fuzziest_station(street_name):
    print("Street:",street_name)
    data = pandas.read_csv("Stations.csv")
    fuzziest = 0
    stop_id = ""
    for index, row in data.iterrows():
        fuzz_ratio = fuzz.ratio(street_name, row["Stop Name"])
        if fuzz_ratio > fuzziest:
            fuzziest = fuzz_ratio
            stop_id = getattr(row, "GTFS Stop ID")
    return stop_id


if __name__ == "__main__":
    app.run(debug=True)

# valid feeds are 1, 26, 16, 21, 2, 11, 31, 36, 51
line_feeds = {
    "1":1,
    "2":1,
    "3":1,
    "4":1,
    "5":1,
    "6":1,
    "S":1,
    "A":26,
    "C":26,
    "E":26,
    "H":26,
    "S":26,
    "N":16,
    "Q":16,
    "R":16,
    "W":16,
    "B":21,
    "D":21,
    "F":21,
    "M":21,
    "L":2,
    "G":31,
    "J":36,
    "Z":36,
    "7":51
}
def get_line_feed(stop_id):
    return line_feeds[stop_id]

