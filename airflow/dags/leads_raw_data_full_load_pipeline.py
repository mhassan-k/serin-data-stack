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
import db_util

def load_parquet_to_postgres():
    db_util.load_parquet_to_table( 'leads.parquet','leads_sft')


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1)
}

dag = DAG('leads_raw_data_full_load_pipeline', default_args=default_args, schedule_interval='@daily')

start = DummyOperator(task_id='start_etl',
                      dag=dag)

end = DummyOperator(task_id='end_etl',
                    dag=dag)

load_parquet = PythonOperator(
    task_id='parquet_to_postgres',
    python_callable=load_parquet_to_postgres,
    dag=dag
            )

start >> load_parquet >> end