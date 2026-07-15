"""@bruin
name: ingestion.trips
type: python
image: python:3.11
connection: duckdb-default

materialization:
  type: table
  strategy: append

columns:
  - name: pickup_datetime
    type: timestamp
  - name: dropoff_datetime
    type: timestamp
  - name: pickup_location_id
    type: integer
  - name: dropoff_location_id
    type: integer
  - name: passenger_count
    type: double
  - name: trip_distance
    type: double
  - name: fare_amount
    type: double
  - name: total_amount
    type: double
  - name: payment_type
    type: integer
  - name: taxi_type
    type: string
@bruin"""

import json
import os

import pandas as pd


def parse_datetime(value):
    ts = pd.Timestamp(value)
    if ts.tzinfo is not None:
        ts = ts.tz_convert(None)
    return ts


def materialize():
    start_date = parse_datetime(os.environ["BRUIN_START_DATE"])
    end_date = parse_datetime(os.environ["BRUIN_END_DATE"])
    taxi_types = json.loads(os.environ["BRUIN_VARS"]).get("taxi_types", ["yellow"])

    frames = []
    months = pd.period_range(start_date.to_period("M"), end_date.to_period("M"), freq="M")

    for taxi_type in taxi_types:
        for month in months:
            url = (
                "https://d37ci6vzurychx.cloudfront.net/trip-data/"
                f"{taxi_type}_tripdata_{month.year}-{month.month:02d}.parquet"
            )

            df = pd.read_parquet(url)
            df["taxi_type"] = taxi_type

            if taxi_type == "yellow":
                df = df.rename(columns={
                    "tpep_pickup_datetime": "pickup_datetime",
                    "tpep_dropoff_datetime": "dropoff_datetime",
                    "PULocationID": "pickup_location_id",
                    "DOLocationID": "dropoff_location_id",
                })
            elif taxi_type == "green":
                df = df.rename(columns={
                    "lpep_pickup_datetime": "pickup_datetime",
                    "lpep_dropoff_datetime": "dropoff_datetime",
                    "PULocationID": "pickup_location_id",
                    "DOLocationID": "dropoff_location_id",
                })

            keep_columns = [
                "pickup_datetime",
                "dropoff_datetime",
                "pickup_location_id",
                "dropoff_location_id",
                "passenger_count",
                "trip_distance",
                "fare_amount",
                "total_amount",
                "payment_type",
                "taxi_type",
            ]

            df = df[keep_columns]
            df = df[
                (df["pickup_datetime"] >= start_date)
                & (df["pickup_datetime"] < end_date)
            ]

            frames.append(df)

    if not frames:
        return pd.DataFrame(columns=[
            "pickup_datetime",
            "dropoff_datetime",
            "pickup_location_id",
            "dropoff_location_id",
            "passenger_count",
            "trip_distance",
            "fare_amount",
            "total_amount",
            "payment_type",
            "taxi_type",
        ])

    return pd.concat(frames, ignore_index=True)
