from kafka import KafkaConsumer

consumer = KafkaConsumer('nyc-311-raw', bootstrap_servers=['localhost:9092'],)

for message in consumer:
    print(message)

consumer.close()