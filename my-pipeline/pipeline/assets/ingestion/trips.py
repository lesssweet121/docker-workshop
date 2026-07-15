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

import io
import json
import os

import pandas as pd
import requests


def parse_date(value: str) -> pd.Timestamp:
    ts = pd.to_datetime(value)
    if ts.tzinfo is not None:
        ts = ts.tz_convert(None)
    return ts


def load_parquet_from_url(url: str) -> pd.DataFrame:
    response = requests.get(url)
    response.raise_for_status()
    with io.BytesIO(response.content) as buffer:
        return pd.read_parquet(buffer)


def materialize():
    start_date = parse_date(os.environ["BRUIN_START_DATE"])
    end_date = parse_date(os.environ["BRUIN_END_DATE"])
    taxi_types = json.loads(os.environ.get("BRUIN_VARS", "{}") or "{}")
    taxi_types = taxi_types.get("taxi_types", ["yellow"])

    months = pd.period_range(start_date.to_period("M"), end_date.to_period("M"), freq="M")
    frames = []

    for taxi_type in taxi_types:
        for month in months:
            url = (
                "https://d37ci6vzurychx.cloudfront.net/trip-data/"
                f"{taxi_type}_tripdata_{month.year}-{month.month:02d}.parquet"
            )

            df = load_parquet_from_url(url)
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
            else:
                raise ValueError(f"Unsupported taxi type: {taxi_type}")

            selected_columns = [
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

            df = df.loc[:, selected_columns]
            df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])
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

