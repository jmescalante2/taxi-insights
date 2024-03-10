import pandas as pd


def standardize_column_names(taxi_trips_df):
    return taxi_trips_df.rename(
        columns={
            "VendorID": "vendor_id",
            "RatecodeID": "rate_code_id",
            "PULocationID": "pickup_location_id",
            "DOLocationID": "dropoff_location_id",
            "Airport_fee": "airport_fee",
        }
    )


def without_zero_passengers(taxi_trips_df):
    return taxi_trips_df[taxi_trips_df["passenger_count"] > 0]


def derive_location_details(
    taxi_trips_df, taxi_zones_df, left_on, right_on, drop, rename
):
    merged_df = (
        pd.merge(
            taxi_trips_df,
            taxi_zones_df,
            how="left",
            left_on=left_on,
            right_on=right_on,
            validate="many_to_one",
        )
        .drop(columns=drop)
        .rename(columns=rename)
    )

    return merged_df


def build_date_dimension(df, datetime_column, rename):
    df["week_name"] = df[datetime_column].dt.day_name()
    df["calendar_day"] = df[datetime_column].dt.day
    df = df.rename(columns=rename)

    return df


def build_time_dimension(df, datetime_column, rename):
    df["hour"] = df[datetime_column].dt.hour
    df["time_of_day"] = df["hour"].apply(get_time_of_day)
    df = df.rename(columns=rename)

    return df


# Derive time of day: morning, afternoon, evening
def get_time_of_day(hour):
    if 0 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Afternoon"
    else:
        return "Evening"


def transform(batch_df, taxi_zones_df):
    taxi_trips_chunk_df = standardize_column_names(batch_df)
    taxi_trips_chunk_df = without_zero_passengers(taxi_trips_chunk_df)

    taxi_trips_chunk_df = derive_location_details(
        taxi_trips_chunk_df,
        taxi_zones_df,
        left_on=["pickup_location_id"],
        right_on=["location_id"],
        drop=["location_id"],
        rename={"borough": "pickup_borough", "zone": "pickup_zone"},
    )

    taxi_trips_chunk_df = derive_location_details(
        taxi_trips_chunk_df,
        taxi_zones_df,
        left_on=["dropoff_location_id"],
        right_on=["location_id"],
        drop=["location_id"],
        rename={"borough": "dropoff_borough", "zone": "dropoff_zone"},
    )

    taxi_trips_chunk_df = build_time_dimension(
        taxi_trips_chunk_df,
        "tpep_pickup_datetime",
        rename={"hour": "pickup_hour", "time_of_day": "pickup_timeofday"},
    )

    taxi_trips_chunk_df = build_time_dimension(
        taxi_trips_chunk_df,
        "tpep_dropoff_datetime",
        rename={"hour": "dropoff_hour", "time_of_day": "dropoff_timeofday"},
    )

    taxi_trips_chunk_df = build_date_dimension(
        taxi_trips_chunk_df,
        "tpep_pickup_datetime",
        rename={
            "week_name": "pickup_week_name",
            "calendar_day": "pickup_calendar_day",
        },
    )

    taxi_trips_chunk_df = build_date_dimension(
        taxi_trips_chunk_df,
        "tpep_dropoff_datetime",
        rename={
            "week_name": "dropoff_week_name",
            "calendar_day": "dropff_calendar_day",
        },
    )

    print(f"cleaned {len(batch_df)}=>{len(taxi_trips_chunk_df)} rows")

    return taxi_trips_chunk_df
