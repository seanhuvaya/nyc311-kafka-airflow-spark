import time
import pandas as pd

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

df = pd.read_csv('data/311_service_request.csv')

for _, row in df.iterrows():
    producer.send(topic='nyc-311-raw', value=row.to_json(orient='records', lines=True).encode("utf-8"))
    producer.flush()
    time.sleep(1)

print('Done!')
producer.close()