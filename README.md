# NYC 311 

## Prerequisites
- Docker & Docker compose
- Python 3.9+
- Git

## Quick Start - How to Run the Project
### 1. Clone the repository
```shell
https://github.com/seanhuvaya/nyc-311-requests.git
cd nyc-311-requests
```

### 2. Install Python dependencies
```shell

```

### 3. Start Kafka
```shell
docker run --name kafka -d -p 9092:9092 apache/kafka:latest
```

### 4. Access Kafka shell inside Docker
```shell
docker exec --workdir /opt/kafka/ -it kafka sh
```

### 5. Create the `nyc-311-raw` topic
```shell
bin/kafka-topics.sh --create --topic nyc-311-raw --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### 6. Download NYC 311 dataset
Go to: https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9/about_data
- Filter to a few months (e.g. last 3 months)
- Export as CSV which is ~1.6 GB
- Save as `data/311_service_request.csv` in project directory or update `producer.py`
**Note:** For quick testing use a very small sample (5000 - 20000 rows)

