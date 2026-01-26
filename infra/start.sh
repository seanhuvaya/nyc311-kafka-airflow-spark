#!/bin/bash
echo "Starting services..."
docker compose up -d --remove-orphans

echo "Waiting for Airflow to start..."
until docker compose logs airflow 2>&1 | grep -q "Password for user 'admin'"; do
  sleep 2
done

echo "Creating Airflow connections..."
source .env

# Create Postgres connection
docker exec airflow airflow connections delete postgres_default 2>/dev/null || true
docker exec airflow airflow connections add postgres_default \
    --conn-type postgres \
    --conn-host postgres-db \
    --conn-login "${PG_USER}" \
    --conn-password "${PG_PASSWORD}" \
    --conn-schema "${PG_DB}" \
    --conn-port 5432

# Create Kafka connection
docker exec airflow airflow connections delete kafka_default 2>/dev/null || true
docker exec airflow airflow connections add kafka_default \
    --conn-type kafka \
    --conn-host kafka-broker \
    --conn-port 9092 \
    --conn-extra '{"bootstrap.servers": "kafka-broker:9092"}'

echo ""
echo "✅ Setup complete!"
echo ""
echo "Airflow connections:"
docker exec airflow airflow connections list

docker exec kafka-broker /opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka-broker:9092 --create --if-not-exists --topic nyc311.raw --partitions 3 --replication-factor 1
docker exec kafka-broker /opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka-broker:9092 --create --if-not-exists --topic nyc311.enriched --partitions 5 --replication-factor 1

echo "Kafka topics:"
docker exec kafka-broker /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list

ADMIN_PASSWORD=$(docker compose logs airflow 2>&1 | grep "Password for user 'admin'" | tail -n 1 | awk -F": " '{print $2}')

echo "Airflow username: admin"
echo "Airflow password: $ADMIN_PASSWORD"


