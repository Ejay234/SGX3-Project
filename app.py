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

if __name__ == "__main__":
    load_traffic_data()
    app.run(debug=True, host='0.0.0.0', port=8042)
