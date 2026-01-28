docker exec kafka-broker /opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka-broker:9092 --create --if-not-exists --topic nyc311.raw --partitions 5 --replication-factor 1

echo "Created Kafka topics:"
docker exec kafka-broker /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list