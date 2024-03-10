import pandas as pd
import pyarrow.parquet as pq

from yellow_taxi_data_analysis import database, load, transformer
from yellow_taxi_data_analysis.database import get_engine
from yellow_taxi_data_analysis.paths import TAXI_ZONE_DATA_PATH, YELLOW_TAXI_DATA_PATH

BATCH_SIZE = 50000
DB_PROTOCOL = "postgresql"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USERNAME = "admin"
DB_PASSWORD = "admin"
DB_NAME = "taxi_data"
TABLE_NAME = "yellow_taxi_trips"


ENGINE = get_engine(
    protocol=DB_PROTOCOL,
    username=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)


def set_up():
    print("Setting up the database and the table...")
    database.create_database(ENGINE, DB_NAME)
    print("Database and table created successfully.")


def main():
    set_up()

    taxi_trips_df = pq.ParquetFile(YELLOW_TAXI_DATA_PATH)
    taxi_zones_df = pd.read_csv(TAXI_ZONE_DATA_PATH)

    for batch in taxi_trips_df.iter_batches(batch_size=BATCH_SIZE):
        transformed_df = transformer.transform(batch.to_pandas(), taxi_zones_df)
        load.load(TABLE_NAME, transformed_df, ENGINE, verbose=True)
