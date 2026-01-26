import json
from datetime import datetime

from airflow import DAG
from airflow.providers.apache.kafka.operators.produce import ProduceToTopicOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2026, 1, 1),
}


def producer_function():
    for i in range(100):
        yield (json.dumps({
            "message_id": i,
            "timestamp": datetime.now().isoformat(),
            "data": f"Test message {i}"
        }), json.dumps({  # Optional: message key
            "key": f"key_{i}"
        }))


with DAG(
        "kafka-producer_dag",
        default_args=default_args,
        schedule=None,
        catchup=False,
) as dag:
    produce_topic_operator = ProduceToTopicOperator(
        task_id="produce_to_kafka",
        topic="nyc311.raw",
        producer_function=producer_function,
        kafka_config_id="kafka_default",
    )
