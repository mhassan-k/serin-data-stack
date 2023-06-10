import os
import sys
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

cwd=os.getcwd()
sys.path.append(f'../transfer_utils/')
sys.path.append(f'../sql/')
sys.path.append(f'../data/temp_files/')
sys.path.insert(0,os.path.abspath(os.path.dirname(__file__)))
from extractor import DataExtractor
import db_util


data_extractor=DataExtractor()


def create_table():
    db_util.create_table()

def extract_data(ti,file_name,**kwargs):

    loaded_df_name=data_extractor.extract_data(file_name=file_name,return_json=True)
    sftp_file_name=loaded_df_name
   
    ti.xcom_push(key="sftp",value=sftp_file_name)


def populate_sftp_table(ti,file_name,**kwargs):
    sftp_file_name = ti.xcom_pull(key="sftp",task_ids='extract_from_file_'+file_name)

    db_util.insert_to_table(sftp_file_name, 'leads_sftp',from_file=True)


def clear_sftp(ti,file_name,**kwargs):
    os.remove(f'../data/SFTP/{file_name}')

# Specifing the default_args
default_args = {
    'owner': 'Hassan',
    'depends_on_past': False,
    'email': ['Hassan@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

path_of_the_directory =f'../data/SFTP'

with DAG(
    dag_id='sftp_raw_data_inc_load_pipeline',
    default_args=default_args,
    description='this loads our data to the database',
    start_date=datetime(2023,5,31),
    schedule_interval='@daily',
    catchup=False
) as dag:
    start = DummyOperator(task_id='start_etl')
    end = DummyOperator(task_id='end_etl')
    create_tables = PythonOperator(
        task_id='create_table',
        python_callable = create_table
    )
    for file in os.listdir(path_of_the_directory):
        read_data = PythonOperator(
        task_id='extract_from_file_'+file,
        python_callable = extract_data,
        op_kwargs={"file_name":file}
        ) 
    
        populate_sftp = PythonOperator(
            task_id='load_sftp_data_'+file,
            python_callable = populate_sftp_table,
            op_kwargs = {"file_name": file}
        )
    

        clean_daily_sftp_data = PythonOperator(
            task_id='clean_sftp_files_'+file,
            python_callable = clear_sftp,
            op_kwargs={"file_name": file}
        )

        start>>create_tables>>read_data>>populate_sftp>>clean_daily_sftp_data>>end
