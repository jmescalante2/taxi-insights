from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    inspect,
    text,
)
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.schema import CreateTable

# Constants for the database connection and configuration
DB_URI = "postgresql://admin:admin@localhost:5432"
DB_NAME = "taxi_data"
TABLE_NAME = "yellow_taxi_trips"


def create_database(engine, db_name):
    with engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        try:
            conn.execute(text(f"CREATE DATABASE {db_name}"))
            print(f"Database {db_name} created successfully.")
        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")


def define_table_schema(engine):
    metadata = MetaData()
    yellow_taxi_trips = Table(
        TABLE_NAME,
        metadata,
        Column("trip_id", Integer, primary_key=True, autoincrement=True),
        Column("VendorID", Integer),
        Column("tpep_pickup_datetime", DateTime),
        Column("tpep_dropoff_datetime", DateTime),
        Column("passenger_count", Float),
        Column("trip_distance", Float),
        Column("RatecodeID", Integer),
        Column("store_and_fwd_flag", String(1)),
        Column("PULocationID", Integer),
        Column("DOLocationID", Integer),
        Column("payment_type", Integer),
        Column("fare_amount", Float),
        Column("extra", Float),
        Column("mta_tax", Float),
        Column("tip_amount", Float),
        Column("tolls_amount", Float),
        Column("improvement_surcharge", Float),
        Column("total_amount", Float),
        Column("congestion_surcharge", Float),
        Column("Airport_fee", Float),
    )
    metadata.create_all(engine)

    print(CreateTable(yellow_taxi_trips).compile(engine).string)
    return yellow_taxi_trips


def truncate_table(engine, table_name):
    if inspect(engine).has_table(table_name):
        with engine.begin() as conn:
            conn.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE")


def load_data_in_chunks(engine, parquet_file, batch_size=50000):
    import pandas as pd
    import pyarrow.parquet as pq

    # Open the Parquet file
    parquet_file = pq.ParquetFile(parquet_file)

    # Truncate the table before loading new data
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE yellow_taxi_trips RESTART IDENTITY"))

    # Iterate over batches
    for batch in parquet_file.iter_batches(batch_size=batch_size):
        # Convert the batch to a pandas DataFrame
        df_chunk = batch.to_pandas()

        # Clean data for each chunk (example: remove records with passenger_count <= 0)
        df_clean = df_chunk[df_chunk["passenger_count"] > 0]

        # Load chunk into SQL database
        df_clean.to_sql(
            "yellow_taxi_trips",
            engine,
            if_exists="append",
            index=False,
            schema="public",
        )

        print("Loaded a chunk of size", len(df_clean))


def main():
    engine = create_engine(DB_URI)
    create_database(engine, DB_NAME)
    with_db_engine = create_engine(f"{DB_URI}/{DB_NAME}")
    yellow_taxi_trips = define_table_schema(with_db_engine)
    load_data_in_chunks(with_db_engine, "yellow_tripdata_2023-12.parquet")


if __name__ == "__main__":
    main()
