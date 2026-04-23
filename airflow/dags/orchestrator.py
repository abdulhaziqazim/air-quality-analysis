from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta

def ingest_task():
    import sys
    sys.path.append('/opt/airflow/request_api')

    from insert_records import main
    return main()


def run_sql(file_path):
    import psycopg2

    conn = psycopg2.connect(
        host="db",
        port=5432,
        dbname="postgres_db",
        user="db_user",
        password="db_password"
    )

    cursor = conn.cursor()

    with open(file_path, "r") as f:
        sql = f.read()

    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()


default_args = {
    "start_date": datetime(2025, 4, 10),
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
    "catchup": False
}

with DAG(
    dag_id="air_quality_sql_pipeline",
    default_args=default_args,
    schedule=timedelta(minutes=5),
    tags=["etl"]
) as dag:

    ingest = PythonOperator(
        task_id="ingest_data",
        python_callable=ingest_task
    )

    staging = PythonOperator(
        task_id="staging_transform",
        python_callable=run_sql,
        op_args=["/opt/airflow/sql/staging/stg_air_quality.sql"]
    )

    analytics = PythonOperator(
        task_id="analytics_transform",
        python_callable=run_sql,
        op_args=["/opt/airflow/sql/analytics/air_quality_daily.sql"]
    )

    ingest >> staging >> analytics