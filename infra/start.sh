#!/bin/bash
docker compose up -d

echo "Waiting for Airflow to start..."

until docker compose logs airflow 2>&1 | grep -q "Password for user 'admin'"; do
  sleep 2
done

ADMIN_PASSWORD=$(docker compose logs airflow 2>&1 | grep "Password for user 'admin'" | tail -n 1 | awk -F": " '{print $2}')

echo "Airflow username: admin"
echo "Airflow password: $ADMIN_PASSWORD"


