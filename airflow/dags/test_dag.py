
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.standard.operators.python import PythonOperator


def safe_main_callable():
    print("example task")

default_args = {
    'description': 'A DAG to test',
    'start_date' : datetime(2025,4,10),
    'catchup' : False,
}

dag = DAG(
    dag_id='test-dag',
    default_args =  default_args,
    schedule = timedelta(minutes=10)
)

with dag:
    task1 = PythonOperator(
        task_id = 'example_rtask',
        python_callable = safe_main_callable
    )