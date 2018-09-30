from flask import Flask, request, jsonify, render_template
from datetime import datetime, timezone
from math import cos, asin, sqrt
import pytz
import pandas
import mta

app = Flask(__name__)

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


# User will give a line feed and a station id
@app.route("/station-line-info", methods=["POST"])
def post_test():
    # valid feeds are 1, 26, 16, 21, 2, 11, 31, 36, 51
    params = request.get_json(force=True)
    train_data = mta.get_train_data(params["feed_id"])
    station_times = mta.station_time_lookup(train_data, params["station_id"])
    response = {
        "station_times": [],
        "schedule_times": mta.get_schedule("Saturday", params["station_id"]),
        "late_times": []
    }
    for time in station_times:
        # Convert from epoch to human time
        response["station_times"].append(epoch_to_time(time))
    response["station_times"].sort()
    response["late_times"] = mta.get_late_times(response["schedule_times"], response["station_times"])
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


if __name__ == "__main__":
    app.run(debug=True)

# valid feeds are 1, 26, 16, 21, 2, 11, 31, 36, 51
