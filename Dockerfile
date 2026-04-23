FROM apache/airflow:3.2.1

WORKDIR /opt/airflow

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt