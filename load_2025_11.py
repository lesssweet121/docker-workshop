import duckdb

parquet_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet"
pg = "postgresql://root:root@localhost:5432/ny_taxi"

con = duckdb.connect()
con.execute("INSTALL postgres; LOAD postgres;")
con.execute(f"ATTACH '{pg}' AS pg (TYPE postgres);")

con.execute("DROP TABLE IF EXISTS pg.public.yellow_taxi_trips_2025_11;")
con.execute(f"""
CREATE TABLE pg.public.yellow_taxi_trips_2025_11 AS
SELECT * FROM read_parquet('{parquet_url}');
""")

print("Done: created pg.public.yellow_taxi_trips_2025_11")
