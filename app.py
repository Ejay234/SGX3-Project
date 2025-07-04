from flask import Flask, jsonify, request
import pandas as pd
import os, sys, io

traffic_df = None

app = Flask(__name__)

def load_traffic_data():
    global traffic_df
    print("Loading Austin Traffic Data")

    traffic_df = pd.read_csv("atxtraffic.csv")

    traffic_df["Published Date"] = pd.to_datetime(traffic_df["Published Date"], errors="coerce")

    traffic_df["Year"] = traffic_df["Published Date"].dt.year
    traffic_df["Hour"] = traffic_df["Published Date"].dt.hour

    print(f"Loaded and cleaned {len(traffic_df)} rows")

@app.route("/")
def index():
    global traffic_df
    sample = traffic_df.head(10).to_dict(orient="records")
    return jsonify(sample)

@app.route("/head")
def top():
    global traffic_df
    num = int(request.args.get("count"))
    sample = traffic_df.head(num).to_dict(orient="records")
    return jsonify(sample)

@app.route("/shape")
def shape():
    global traffic_df
    # shape() returns a tuple
    rows = traffic_df.shape[0]
    columns = traffic_df.shape[1]
    return jsonify({"rows": rows, "columns": columns})

@app.route("/columns")
def columns():
    global traffic_df
    columns = traffic_df.columns.tolist()
    return jsonify(columns)

@app.route("/info")
def info():
    global traffic_df
    buffer = io.StringIO()
    traffic_df.info(buf=buffer)
    buffer.seek(0)
    return jsonify({"info": buffer.read()})

@app.route("/describe")
def describe():
    global traffic_df
    # for column descriptions
    describe = traffic_df.describe().to_dict(orient="index")
    return jsonify(describe)

@app.route("/unique")
def unique():
    global traffic_df
    column = request.args.get("column")
    if column not in traffic_df.columns:
        return jsonify({"error": f"Column '{column}' not found"}), 400
    values = traffic_df[column].dropna().unique().tolist()
    return jsonify({column: values})

@app.route("/incidents")
def incidents():
    global traffic_df
    column = request.args.get("column")
    value = request.args.get("value")
    year = request.args.get("year")

    # Check if all inquirys exists
    if not column or not value or not year:
        return jsonify({"Error": "Missing parameters"}), 400

    # Check if column exists
    if column not in traffic_df.columns:
        return jsonify({"Error": f"Column '{column}' not found."}), 400

    # Check if year is an integer
    try:
        year = int(year)
    except ValueError:
        return jsonify({"Error": "Year must be an integer"}), 400
    
    # Ensure there is a datetime column
    if "Published Date" not in traffic_df.columns:
        return jsonify({"error": "No date column established in the dataframe"}), 400

    # Ensures the date is in a datetime frame
    if not pd.api.types.is_datetime64_any_dtype(traffic_df["Published Date"]):
        traffic_df["Year"] = pd.to_datetime(traffic_df["Published Date"]).apply(lambda x: x.year)

    # Create the givendataframe to showcase in the route
    filter_df = traffic_df[
            (traffic_df[column] == value) &
            (traffic_df["Year"] == year)
    ]

    return jsonify(filter_df.to_dict(orient="records"))

@app.route("/hour")
def hour():
    global traffic_df

    # Get hour parameters
    start = request.args.get("start")
    end = request.args.get("end")

    # Validate the parameters
    if start is None or end is None:
        return jsonify({"error": "Missing parameters"})

    try:
        start = int(start)
        end = int(end)
        if not (0 <= start <= 23) and ( 0 < = end <= 23):
            raise ValueError
    except:
        return jsonify({"error": "Hours must be between 0 and 23"})

    # Ensure there is a datetime column
    if "Published Date" not in traffic_df.columns:
        return jsonify({"error": "No date column established in the dataframe"}), 400

    # Ensures the date is in a datetime frame
    if not pd.api.types.is_datetime64_any_dtype(traffic_df["Published Date"]):
        traffic_df["Hour"] = pd.to_datetime(traffic_df["Published Date"]).apply(lambda x: x.hour)

    # Create the givendataframe to showcase in the route
    filter_df = traffic_df["Hour"].between(start, end)

    return jsonify(filter_df.to_dict(orient="records"))

@app.route("/nearby")
def nearby():
    global traffic_df

    # Get latitude and longitude
    try:
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lon"))
    except (TypeError, ValueError):
        return jsonify({"error": "Missing or invalid"})

    if "Latitude" not in traffic_df.columns or "Longitude" not in traffic_df.columns:
        return jsonify({"Error": "Dataframe does not have columns"})

    # Function to compute distance in kilometers
    def compute(lat1, lon1, lat2, lon2):
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * \
            math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    km = traffic_df.apply(lambda row: haversine(lat, long, row["Latitude"], row["Longitude"]), axis=1)

    filter_df = traffic_df[km <= 1]

    return jsonify(filter_df = traffic_df.to_dict(orient="records"))
    

if __name__ == "__main__":
    load_traffic_data()
    app.run(debug=True, host='0.0.0.0', port=8042)
