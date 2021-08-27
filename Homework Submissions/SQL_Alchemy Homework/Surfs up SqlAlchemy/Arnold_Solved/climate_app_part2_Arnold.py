from flask import Flask, jsonify
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import json

########this is the primary code and one approach attempted.  I was also trying to create SQL files to reference with "def"
######## for a sleeker set of codes, but i ran out of time. SQL_C_factory, sqlhelper_climate, and the SQL files were my attempt
# Flask Setup
app = Flask(__name__)

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# Flask Routes
@app.route("/")
def index():
    return (
        f"Welcome to the Hawaii Weather Station API!<br/>"
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"<a href='/api/v1.0/2016-10-31'>/api/v1.0/START_DATE</a>  ----- (date must be yyyy-mm-dd format)<br/>"
        f"<a href='/api/v1.0/2017-05-22/2017-08-22'>/api/v1.0/START_DATE/END_DATE</a>  ----- (date must be yyyy-mm-dd format)<br/>"

    )

@app.route("/api/v1.0/stations")
def station():

    conn = engine.connect()

  
    query = "SELECT * FROM station;"
    df = pd.read_sql(query, con=conn)
    conn.close()
    
  
    data = df.to_json(orient="records")
    data = json.loads(data) 

    return jsonify({"ok": True, "data": data})

@app.route("/api/v1.0/precipitation")
def precipitation():

    conn = engine.connect()


    query = f"""
                SELECT
                    date,
                    avg(prcp) as avg_prcp
                FROM
                    measurement
                GROUP BY
                    date
                ORDER BY
                    date asc;
            """
    df = pd.read_sql(query, con=conn)
    conn.close()
    
    data = df.to_json(orient="records") 
    data = json.loads(data) 

    return jsonify({"ok": True, "data": data})

@app.route("/api/v1.0/tobs")
def temperature():
    # Measurement TABLE, most popular station  - last year

    conn = engine.connect()
    query = f"""
                SELECT
                    station,
                    date,
                    tobs as temperature
                FROM
                    measurement
                WHERE
                    station = 'USC00519281'
                    and date >= '2016-08-23'
                ORDER BY
                    date asc;
            """
    df = pd.read_sql(query, con=conn)
    conn.close()
    

    data = df.to_json(orient="records") 
    data = json.loads(data) 

    return jsonify({"ok": True, "data": data})

@app.route("/api/v1.0/<start>") 
def startDate(start):

    conn = engine.connect()


    query = f"""
                SELECT
                    date,
                    min(tobs) as min_temp,
                    avg(tobs) as avg_temp,
                    max(tobs) as max_temp
                FROM
                    measurement
                where
                    date = '{start}'
            """
    df = pd.read_sql(query, con=conn)
    conn.close()
    
 
    data = df.to_json(orient="records") 
    data = json.loads(data) 

    return jsonify({"ok": True, "data": data})

@app.route("/api/v1.0/<start>/<end>") 
def dateRange(start, end):
    #  grouped by date, and avg precipitation


    conn = engine.connect()


    query = f"""
                SELECT
                    min(date) as start_date,
                    max(date) as end_date,
                    min(tobs) as min_temp,
                    avg(tobs) as avg_temp,
                    max(tobs) as max_temp
                FROM
                    measurement
                where
                    date >= '{start}'
                    and date <= '{end}'
            """
    df = pd.read_sql(query, con=conn)
    conn.close()
    
    
    data = df.to_json(orient="records") 
    data = json.loads(data) 

    return jsonify({"ok": True, "data": data})


if __name__ == "__main__":
    app.run(debug=True)
