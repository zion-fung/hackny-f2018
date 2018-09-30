import openpyxl
if __name__ == "__main__":
    wb = openpyxl.load_workbook("stop_times.xlsx", read_only=True)
    sheet = wb["stop_times"]
    stop_times = {}
    index = 0
    for row in sheet.rows:
        stop_id = row[3].value
        trip_id = row[0].value
        time = str(row[1].value)[-8:]
        if stop_id not in stop_times:
            stop_times[stop_id] = {}
            stop_times[stop_id]["Sunday"] = []
            stop_times[stop_id]["Saturday"] = []
            stop_times[stop_id]["Weekday"] = []
        if "Sunday" in trip_id:
            stop_times[stop_id]["Sunday"].append(time)
        elif "Saturday" in trip_id:
            stop_times[stop_id]["Saturday"].append(time)
        elif "Weekday" in trip_id:
                stop_times[stop_id]["Weekday"].append(time)
        index += 1
        if index % 100 == 0:
            print("Wrote", index, "lines!")
    print("Wrote", index, "lines!")
    f = open("stop_times.json", "w")
    f.write(str(stop_times))
    f.close()
    # format is { stop_id: {"Sunday": [], "Weekday": [], "Saturday": [] } }