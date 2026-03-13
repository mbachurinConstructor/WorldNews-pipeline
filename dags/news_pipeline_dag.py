from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys


sys.path.insert(0, '/opt/airflow')

from scripts.extract import run_extract
from scripts.transform import run_transform
from scripts.load import load_to_db

default_args : dict = {
    'owner': "airflow",
    "retries" : 1,
    "retry_delay" : timedelta(minutes=5),
}

with DAG(
    dag_id="news_pipeline",
    default_args=default_args,
    description="Fetch news, transform, load to PostgreSQL",
    schedule_interval="@hourly",
    start_date=datetime(2026, 3, 12),
    catchup=False,
) as dag:
    extract : PythonOperator = PythonOperator(
        task_id="extract",
        python_callable=run_extract,
    )

    transform : PythonOperator = PythonOperator(
        task_id="transform",
        python_callable=run_transform,
    )

    load : PythonOperator = PythonOperator(
        task_id="load_to_db",
        python_callable=load_to_db,
    )

    extract >> transform >> load