from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    Integer,
    MetaData,
    String,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateTable, DropTable

Base = declarative_base()


class YellowTaxiTrip(Base):
    __tablename__ = "yellow_taxi_trips"

    trip_id = Column(Integer, primary_key=True, autoincrement=True)
    vendor_id = Column(Integer)
    tpep_pickup_datetime = Column(DateTime)
    tpep_dropoff_datetime = Column(DateTime)
    passenger_count = Column(Integer)
    trip_distance = Column(Float)
    rate_code_id = Column(Integer)
    store_and_fwd_flag = Column(String)
    pickup_location_id = Column(Integer)
    dropoff_location_id = Column(Integer)
    payment_type = Column(Integer)
    fare_amount = Column(Float)
    extra = Column(Float)
    mta_tax = Column(Float)
    tip_amount = Column(Float)
    tolls_amount = Column(Float)
    improvement_surcharge = Column(Float)
    total_amount = Column(Float)
    congestion_surcharge = Column(Float)
    airport_fee = Column(Float)
    pickup_borough = Column(String)
    pickup_zone = Column(String)
    dropoff_borough = Column(String)
    dropoff_zone = Column(String)
    pickup_hour = Column(Integer)
    pickup_timeofday = Column(String)
    dropoff_hour = Column(Integer)
    dropoff_timeofday = Column(String)
    pickup_week_name = Column(String)
    pickup_calendar_day = Column(Integer)
    pickup_calendar_date = Column(Date)
    dropoff_week_name = Column(String)
    dropoff_calendar_day = Column(Integer)
    dropoff_calendar_date = Column(Date)


def create_database(engine):
    # Create database and table
    Base.metadata.drop_all(engine)  # Drops table if exists
    Base.metadata.create_all(engine)  # Creates new table
