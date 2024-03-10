import pandas as pd
from sqlalchemy import create_engine

# SQLite database connection
engine = create_engine("sqlite:///taxi_data_db.sqlite")


# Load and clean data from Parquet
df = pd.read_parquet("yellow_tripdata_2023-12.parquet")
df_clean = df[df["passenger_count"] > 0]

# Load into SQL database
df_clean.to_sql("yellow_taxi_trips", engine, if_exists="replace", index=False)
