from flask import Flask, jsonify, request
import pandas as pd
import os, sys, io

traffic_df = None

app = Flask(__name__)

def load_traffic_data():
    global traffic_df
    print("Loading Austin Traffic Data")

    traffic_df = pd.read_csv("atxtraffic.csv")
    print(f"Loaded {len(traffic_df)} rows into memory")

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

    if not pd.api.types.is_datetime64_any_dtype(traffic_df["Published Date"]):
        traffic_df["Year"] = pd.to_datetime(traffic_df["Published Date"]).apply(lambda x: x.year)

    filter_df = traffic_df[
            (traffic_df[column] == value) &
            traffic_df["Year"].dt.year == year)
    ]

    return jsonify(filter_df.to_dict(orient="records"))


if __name__ == "__main__":
    load_traffic_data()
    app.run(debug=True, host='0.0.0.0', port=8042)
