import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import and_, or_, not_

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)


@app.route("/api/v1.0/precipitation")
def precip():

    results = session.query(Measurement).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_records = []
    for record in results:
        precip_dict = {}
        precip_dict[record.date] = record.prcp
        all_records.append(precip_dict)

    return jsonify(all_records)

@app.route("/api/v1.0/stations")
def stations():

    results = session.query(Station.name).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = []
    for record in results:
        station_dict = {}
        station_dict["Station"] = record.name
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    last_date = session.query(Measurement.date, Measurement.tobs).order_by(Measurement.date.desc()).first()
    dateSplit = last_date[0].split("-")
    query_date = dt.date(int(dateSplit[0]), int(dateSplit[1]), int(dateSplit[2])) - dt.timedelta(days = 365)
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= query_date)

    # Create a dictionary from the row data and append to a list of all_passengers
    all_temps = []
    for record in results:
        temp_dict = {}
        temp_dict[record.date] = record.tobs
        all_temps.append(temp_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/<start>")
def temp(start):
    # date is of the format MM-DD-YYYY")
    dateSplit = start.split("-")
    query_date = dt.date(int(dateSplit[2]), int(dateSplit[0]), int(dateSplit[1]))
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= query_date).first()
    # Create a dictionary from the row data and append to a list of all_passengers
    all_agg = []
    agg_dict = {}
    agg_dict = ({"MinTemp": results[0]}, {"AvgTemp": results[1]},{"MaxTemp":results[2]})
    return jsonify(agg_dict)

@app.route("/api/v1.0/<start>/<end>")
def temp2(start, end):
    # date is of the format MM-DD-YYYY")
    startSplit = start.split("-")
    endSplit = end.split("-")
    startDate = dt.date(int(startSplit[2]), int(startSplit[0]), int(startSplit[1]))
    endDate = dt.date(int(endSplit[2]), int(endSplit[0]), int(endSplit[1]))
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(and_(startDate <= Measurement.date, Measurement.date <= endDate )).first()
    # Create a dictionary from the row data and append to a list of all_passengers
    all_agg = []
    agg_dict = {}
    agg_dict = ({"MinTemp": results[0]}, {"AvgTemp": results[1]},{"MaxTemp":results[2]})
    return jsonify(agg_dict)

if __name__ == '__main__':
    app.run(debug=False)
