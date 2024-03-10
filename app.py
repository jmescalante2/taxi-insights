import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine

from yellow_taxi_data_analysis import transformer
from yellow_taxi_data_analysis.paths import TAXI_ZONE_DATA_PATH, YELLOW_TAXI_DATA_PATH

BATCH_SIZE = 50000


def main():
    taxi_trips_df = pq.ParquetFile(YELLOW_TAXI_DATA_PATH)
    taxi_zones_df = pd.read_csv(TAXI_ZONE_DATA_PATH)

    for batch in taxi_trips_df.iter_batches(batch_size=BATCH_SIZE):
        transformed_df = transformer.transform(batch.to_pandas(), taxi_zones_df)
