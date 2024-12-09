# Realtime Data Streaming

## Overview
In this self-project, we set up an end-to-end data streaming pipeline in realtime using Docker Compose. To accomplish this taks, we will integrate different components such as Apache Airflow, Apache Kafka, Apache Spark, Confluent Control Center, Confluent Schema Registry, PostgreSQL, and Cassandra. 

The pipeline works as follows:
- Airflow runs a DAG (`kafka_stream.py`) that retrieves user data from the Random User API in intervals and sends it to a Kafka topic (`users_created`).
- Spark, configured with Kafka and Cassandra connectors, consumes the user data events from Kafka and stores them into a Cassandra database.

## Features
- **Real-Time Streaming with Kafka:** User events are published to and consumed from a Kafka topic.
- **Automated Data Ingestion:** Airflow DAG fetches data every minute from the Random User API.
- **Schema Registry & Control Center:** Confluent platform images included for optional schema management and monitoring.
- **Data Storage:** Final data is stored in a Cassandra keyspace and table for scalable and robust persistence.
- **Orchestration & Scheduling:** Airflow handles job scheduling and pipeline management.
- **Scalable & Modular:** The pipeline is modular, allowing you to replace sources, sinks, or add transformations without re-architecting.

## Usage
1. **Clone the Repository:**
2. **Set Up Airflow Directories & Files:**
    - Place`requirements.txt` is in the project root.
    - Place the `entrypoint.sh` script in the `scripts` directory.
    - Place any and all DAGs in the `dags` directory.

3. **Start the Environment:**
   ```
   docker-compose up -d
   ```

4. **Access Services:**
    - Airflow UI: [http://localhost:8080](http://localhost:8080) (username: `admin`, password: `admin`)
    - Kafka Broker: exposed on localhost:9092
    - Confluent Control Center: [http://localhost:9021](http://localhost:9021)
    - Spark Master UI: [http://localhost:9090](http://localhost:9090)
    - PostgreSQL and Cassandra ports are also exposed for direct connections if needed.

## Prerequisites
- **Docker & Docker Compose:** Ensure Docker and Docker Compose are installed.
- **Sufficient System Resources:** Running multiple services simultaneously may require sufficient CPU, RAM, and disk space.
- **Network Ports:** Make sure the ports used by the services (e.g., 8080, 9092, 9021, 9090, etc.) are not being used by other applications.

## Input
- **Source API:** The input data comes from [Random User API](https://randomuser.me/). Airflow’s DAG invokes the API every minute.
- **Kafka Topic `users_created`:** Fetched and processed user data is streamed into this Kafka topic.

## Output
- **Airflow UI Logs:** Real-time logs and status of DAGs.
- **Cassandra Table:** Processed user data is written by Spark into the `spark_streams.created_users` table.
- **Spark Streaming Logs:** Check the Spark driver and executor logs for details about streaming operations.

## Notes
- **Customization:** You can modify the Airflow DAG (`kafka_stream.py`) to fetch data from a different API or perform additional transformations.
- **Security & Authentication:** This setup is for demonstration and development. Consider adding security features (authentication, SSL, RBAC) for production environments.
- **Monitoring & Observability:** Leverage Control Center and Spark UI for monitoring. Integrate with Prometheus/Grafana or other APM tools for enhanced observability.
- **Scaling Out:** Additional Spark workers or Kafka brokers can be added to the `docker-compose.yml` as needed.