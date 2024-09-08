# Import the dependencies.

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

from datetime import datetime, timedelta


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################


@app.route('/')
def home():
    return (
        "Welcome to the Hawaii Climate API!<br>"
        "Available Routes:<br>"
        "/api/v1.0/precipitation<br>"
        "/api/v1.0/stations<br>"
        "/api/v1.0/tobs<br>"
        "/api/v1.0/<start><br>"
        "/api/v1.0/<start>/<end>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():

    # Find the most recent date in the data set
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    
    # Ensure most_recent_date is in correct datetime format
    most_recent_date = datetime.strptime(most_recent_date, "%Y-%m-%d")


    # Query for the most recent 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= (most_recent_date - timedelta(days=366))).all()
    
    # Convert the results into a dictionary
    precipitation_data = {date: prcp for date, prcp in results}
    
    return jsonify(precipitation_data)

@app.route('/api/v1.0/stations')
def stations():
    # Query all stations
    results = session.query(Station.station, Station.name).all()
    
    # Convert the results into a list of dictionaries
    stations_data = [{'station': station, 'name': name} for station, name in results]
    
    return jsonify(stations_data)

@app.route('/api/v1.0/tobs')
def tobs():
    # Query for temperature observations for the most active station over the last 12 months
    most_active = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()
    
    most_active_id = most_active[0][0]
   
    # Find the most recent date in the data set
    most_recent_date = session.query(func.max(Measurement.date)).scalar()

    # Ensure most_recent_date is in correct datetime format
    most_recent_date = datetime.strptime(most_recent_date, "%Y-%m-%d")

    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_id).\
        filter(Measurement.date >= (most_recent_date - timedelta(days=366)))
    
    # Convert the results into a list of dictionaries
    tobs_data = [{'date': date, 'temperature': tobs} for date, tobs in results]
    
    return jsonify(tobs_data)

@app.route('/api/v1.0/<start>')
def start_date(start):
    # Query temperature statistics from the start date to the most recent date
    results = session.query(
        func.min(Measurement.tobs).label('min_temp'),
        func.avg(Measurement.tobs).label('avg_temp'),
        func.max(Measurement.tobs).label('max_temp')
    ).filter(Measurement.date >= start).all()
    
    # Convert the result to a dictionary
    temp_stats = results[0]._asdict()
    
    return jsonify(temp_stats)

@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    # Query temperature statistics from the start date to the end date
    results = session.query(
        func.min(Measurement.tobs).label('min_temp'),
        func.avg(Measurement.tobs).label('avg_temp'),
        func.max(Measurement.tobs).label('max_temp')
    ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    # Convert the result to a dictionary
    temp_stats = results[0]._asdict()
    
    return jsonify(temp_stats)

if __name__ == '__main__':
    app.run(debug=True)