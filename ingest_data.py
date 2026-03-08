#!/usr/bin/env python
# coding: utf-8

# In[56]:

pg_user = 'root'
pg_pass = 'root'
pg_host = 'localhost'
pg_port = 5432
pg_db = 'ny_taxi'


year = 2021
month = 1


engine = create_engine(
    "postgresql+psycopg://root:root@ny_taxi_pg:5432/ny_taxi"
)


# In[57]:


import pandas as pd


# In[58]:


# Read a sample of the data
prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'


# In[60]:





# In[63]:


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

df = pd.read_csv(
    prefix + 'yellow_tripdata_2021-01.csv.gz',
    nrows=100,
    dtype=dtype,
    parse_dates=parse_dates
)


# In[64]:


df.head()


# In[65]:


df['tpep_pickup_datetime']


# In[66]:


get_ipython().system('uv add sqlalchemy')


# In[67]:


get_ipython().system('uv add psycopg2-binary')


# In[68]:


from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')


# In[69]:


df.head(0)


# In[70]:


df.head(0).to_sql(
    name="yellow_taxi_data",
    con=engine,
    if_exists="replace",
    index=False
)


# In[71]:


get_ipython().system('nc -vz localhost 5432')


# In[72]:


get_ipython().system('nc -vz localhost 5432')


# In[73]:


len(df)


# In[74]:


print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[75]:


df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[77]:


get_ipython().system('uv add tqdm')


# In[78]:


df_iter = pd.read_csv(
    prefix + 'yellow_tripdata_2021-01.csv.gz',
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000
)


# In[79]:


from tqdm.auto import tqdm


# In[80]:


for df_chunk in tqdm(df_iter):
    df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




