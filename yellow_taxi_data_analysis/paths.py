from pathlib import Path

PROJECT_DIRECTORY = Path(__file__).parent.parent.resolve()
DATA_DIRECTORY = Path.joinpath(PROJECT_DIRECTORY, "data")
YELLOW_TAXI_DATA_PATH = Path.joinpath(DATA_DIRECTORY, "yellow_tripdata_2023-12.parquet")
TAXI_ZONE_DATA_PATH = Path.joinpath(DATA_DIRECTORY, "taxi_zones.csv")
