import sys
import pandas as pd
from sqlalchemy import text
import json
from sqlalchemy import create_engine
import numpy as np

engine = create_engine('postgresql+psycopg2://airflow:airflow@host.docker.internal:8585/postgres')

LEADS_SCHEMA = "leads_schema.sql"
SPTP_SCHEMA = "sftp_schema.sql"


def create_table():
    try:
        with engine.connect() as conn:
            for name in [LEADS_SCHEMA,SPTP_SCHEMA]:
                
                with open(f'/opt/sql/{name}', "r") as file:
                    query = text(file.read())
                    conn.execute(query)
        print("Successfull")
    except Exception as e:
        print("Error creating table",e)
        sys.exit(e)


# create_table()

def insert_to_table(json_stream :str, table_name: str,from_file=False):
    try:
        if not from_file:
            df = pd.read_json(json_stream)

        else:
            # df = pd.read_json(f'../temp/{json_stream}')
            with open(f'/opt/data/temp_files/{json_stream}','r') as file:
                data=file.readlines()
            dt=data[0]

            df=pd.DataFrame.from_dict(json.loads(dt))
            df.columns=df.columns.str.replace(' ','')

            # TODO: This(the following line) shall be fixed when using cloud services
            # due to local memory (resource) shortage, I minimized the df to be loaded 
            # df=df.loc[:np.floor(df.shape[0]/10),:] 
            df.dropna(inplace=True)
        with engine.connect() as conn:
            df.to_sql(name=table_name, con=conn, if_exists='append', index=False)

    except Exception as e:
        print(f"error while inserting to table: {e}")  
        sys.exit(e)


def load_parquet_to_table(file_path :str ,table_name :str ):
    try:
        # Load Parquet file into a DataFrame
        df = pd.read_parquet(f'../data/parquet/{file_path}')

        # Write the DataFrame to the PostgreSQL database table
        with engine.connect() as conn:
            df.to_sql(table_name, con=conn, if_exists='replace', index=False)

        print("Parquet file loaded into PostgreSQL successfully.")
    except Exception as e:
        print(f"Error loading Parquet file into PostgreSQL: {str(e)}")

