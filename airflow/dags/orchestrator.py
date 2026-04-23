
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.standard.operators.python import PythonOperator


def safe_main_callable():
    import sys
    sys.path.append('/opt/airflow/request_api')
    from insert_records import main
    return main()

default_args = {
    'description': 'A DAG to orchestrate data',
    'start_date' : datetime(2025,4,10),
    'catchup' : False,
}

dag = DAG(
    dag_id='air-quality-orchestrator',
    default_args =  default_args,
    schedule = timedelta(minutes=5)
)

with dag:
    task1 = PythonOperator(
        task_id = 'ingest_data',
        python_callable = safe_main_callable
    )