#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm


prefix = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow"

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

# # to convert df schema into postgres table schema
# print(pd.io.sql.get_schema(df, name="yellow_taxi_data", con=engine))

def ingest_data(
        url:str,
        table_name:str,
        chunk_size:int,
        engine
):
    
    # TODO: Read data in chunks
    df_iter = pd.read_csv(
        url,
        dtype = dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunk_size
    )
    #TODO: Load data in chunks to table
    first = True
    for data_chunk in tqdm(df_iter):
        if first:
            data_chunk.head(0).to_sql(name=table_name, con=engine, if_exists="replace")
            print(f'Table: {table_name} created !!')
            data_chunk.to_sql(name=table_name, con=engine, if_exists="append")
            print(f'Inserted first chunk: {len(data_chunk)}')
            first = False
        else:
            data_chunk.to_sql(name=table_name, con=engine, if_exists="append")
            print(f'Inserted chunk: {len(data_chunk)}')

def main(
        year:int,
        month:int,
        pg_user:str,
        pg_password:str,
        pg_host:str,
        pg_port:int,
        pg_db:str,
        chunk_size:int,
        target_table: str
):

    url = f"{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz"
    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')
    ingest_data(url, table_name=target_table, chunk_size=chunk_size, engine=engine)

if __name__ == '__main__':
    main(
        year=2021,
        month=1,
        pg_user = "root",
        pg_password = "root",
        pg_host = "localhost",
        pg_port = 5433,
        pg_db = "ny_taxi",
        chunk_size=100000,
        target_table="yellow_taxi_data"
    )




