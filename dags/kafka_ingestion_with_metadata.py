from datetime import datetime

from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook

CREATE_METADATA_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS ingestion_metadata (
  run_id VARCHAR(100) PRIMARY KEY,
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  records_ingested INT,
  status VARCHAR(20),
  created_at TIMESTAMP DEFAULT NOW()
);
"""

@dag(
    dag_id="kafka_ingestion_with_metadata",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
)
def kafka_ingestion_with_metadata():

    @task
    def create_metadata_table():
        PostgresHook(postgres_conn_id="postgres_default").run(CREATE_METADATA_TABLE_SQL)


kafka_ingestion_with_metadata()