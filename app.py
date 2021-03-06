import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


# database engine and columns
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# app
app = Flask(__name__)

# main route to define endpoints
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"Precipitation: /api/precipitation<br/>"
        f"List of Stations: /api/stations<br/>"
        f"Temperature for one year: /api/tobs<br/>"
        f"Temperature stat from the start date(yyyy-mm-dd): /api/yyyy-mm-dd<br/>"
        f"Temperature stat from start to end dates(yyyy-mm-dd): /api/yyyy-mm-dd/yyyy-mm-dd"
    )


# precipitation endpoint
@app.route("/api/precipitation")
def precipitation():
    session = Session(engine)
    sel = [Measurement.date, Measurement.prcp]
    queryresult = session.query(*sel).all()
    session.close()

    precipitation = []
    for date, prcp in queryresult:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)


# stations endpoint
@app.route("/api/stations")
def stations():
    session = Session(engine)
    sel = [
        Station.station,
        Station.name,
        Station.latitude,
        Station.longitude,
        Station.elevation,
    ]
    queryresult = session.query(*sel).all()
    session.close()

    stations = []
    for station, name, lat, lon, el in queryresult:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lon"] = lon
        station_dict["Elevation"] = el
        stations.append(station_dict)

    return jsonify(stations)


# tobs endpoints
@app.route("/api/tobs/<start>")
def get_tobs_start(start):
    session = Session(engine)
    queryresult = (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .all()
    )
    session.close()

    tobsall = []
    for min, avg, max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)

    return jsonify(tobsall)


@app.route("/api/tobs/<start>/<stop>")
def get_tobs_start_stop(start, stop):
    session = Session(engine)
    queryresult = (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .filter(Measurement.date <= stop)
        .all()
    )
    session.close()

    tobsall = []
    for min, avg, max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)

    return jsonify(tobsall)


@app.route("/api/tobs")
def tobs():
    session = Session(engine)
    lateststr = (
        session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    )
    latestdate = dt.datetime.strptime(lateststr, "%Y-%m-%d")
    querydate = dt.date(latestdate.year - 1, latestdate.month, latestdate.day)
    sel = [Measurement.date, Measurement.tobs]
    queryresult = session.query(*sel).filter(Measurement.date >= querydate).all()
    session.close()

    tobsall = []
    for date, tobs in queryresult:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobsall.append(tobs_dict)

    return jsonify(tobsall)


if __name__ == "__main__":
    app.run(debug=True)
