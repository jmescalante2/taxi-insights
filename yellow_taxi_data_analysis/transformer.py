import pandas as pd
import pyarrow.parquet as pq

from yellow_taxi_data_analysis.paths import YELLOW_TAXI_DATA_PATH

BATCH_SIZE = 50000


def main():
    parquet_file = pq.ParquetFile(YELLOW_TAXI_DATA_PATH)

    for batch in parquet_file.iter_batches(batch_size=BATCH_SIZE):
        df_chunk = batch.to_pandas()
        df_clean = df_chunk[df_chunk["passenger_count"] > 0]
        print(f"cleaned {len(df_clean)} rows")


if __name__ == "__main__":
    main()
