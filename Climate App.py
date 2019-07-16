from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import pandas as pd
import seaborn as sns
import datetime as dt
from dateutil.relativedelta import relativedelta 
from flask import Flask, jsonify
import os

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.inspection import inspect
from sqlalchemy import desc

# Create Engine for Hawaii Data 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
inspector = inspect(engine)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# # Exploratory Climate Analysis

# Parse dates
data_last_str = "2017-08-23"
data_last_date = dt.datetime.strptime(data_last_str, '%Y-%m-%d')
print(type(data_last_date), data_last_date)

# Calculate the date 1 year ago from the last data point in the database
prev_year = data_last_date - relativedelta(years=1)
print(type(prev_year), prev_year)

# Climate App
app = Flask(__name__)

# List all routes that are available
@app.route("/")
def home():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )  

# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
# Use last date in database and Query all passengers
    print(data_last_date, prev_year)
    results =session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
    
    #  Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    all_prcp = []

    for date_ob in results:
        all_prcp_dict = {}
        all_prcp_dict["Date"] = date_ob.date
        all_prcp_dict["Precipitation"] = date_ob.prcp

        all_prcp.append(all_prcp_dict)
    print(all_prcp)

# Return the JSON representation of your dictionary.
    return jsonify(all_prcp)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stationName():
    # Query all station names
    stationName_results = session.query(Station.station).all()
    print(stationName_results)
    # Convert list of tuples into normal list
    stationName_list = list(np.ravel(stationName_results))
    print(stationName_list)
    # Jsonify all_tobs
    return jsonify(stationName_list)

# Return a JSON list of Temperature Observations (tobs) for the previous year

@app.route("/api/v1.0/tobs")
def tobs():
    print(data_last_date, prev_year)
    #Query Temperature Tobs
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= prev_year).all()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(results))
    # print(tobs_list)

    # Jsonify all_tobs
    return jsonify(tobs_list)


# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<startdate>")
def summarystats(startdate):
    # print(startdate)
    # Calculate summary stats
    summary_stats = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.round(func.avg(Measurement.tobs))).\
        filter(Measurement.date >= startdate).all()

    summary = list(np.ravel(summary_stats))
    # print(summary)
    # Jsonify summary
    return jsonify(summary)

# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
@app.route("/api/v1.0/<startdate>/<enddate>")
def daterange(startdate,enddate):
    # Calculate summary stats
    summary_stats = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.round(func.avg(Measurement.tobs))).\
        filter(Measurement.date.between(startdate,enddate)).all()
    
    summary = list(np.ravel(summary_stats))

    # Jsonify summary
    return jsonify(summary)

if __name__ == '__main__':
    app.run(debug=True)
