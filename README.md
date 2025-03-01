# Realtime Data Streaming Pipeline

## Overview
In this self-project, we set up an end-to-end data streaming pipeline in realtime using Docker Compose. To accomplish this taks, we will integrate different components such as Apache Airflow, Apache Kafka, Apache Spark, Confluent Control Center, Confluent Schema Registry, PostgreSQL, and Cassandra. 
The pipeline works as follows:
- Using Airflow, we run a DAG (`kafka_stream.py`) that retrieves user data from the Random User API, in intervals, and sends it to a Kafka topic (`users_created`).
- Spark is configured with connectors to Kafka and Cassandra, it consumes the user data events from Kafka and then stores them into a Cassandra database.

## Features
- **Real-Time Streaming with Kafka:** User events are published to and consumed from a Kafka topic.
- **Automated Data Ingestion:** Airflow DAG fetches data every minute from the Random User API.
- **Data Storage:** Data is stored in a Cassandra keyspace and table for robust persistence.
- **Orchestration & Scheduling:** Airflow handles job scheduling and pipeline management.
- **Schema Registry & Control Center:** Confluent platform images for schema management and monitoring.
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
    1. Web Interfaces
        - Airflow UI: `http://localhost:8080`
            - username: `admin`
            - password: `admin`
        - Spark Master UI: `http://localhost:9090`
        - Confluent Control Center: `http://localhost:9021`
    2. Clien Connections
        - Zookeeper: exposed on `localhost:2181`
        - Kafka Broker: exposed on `localhost:9092`
        - Cassandra: exposed on  `localhost:9042`
    3. REST APIs
        - Schema Registry: exposed on `http://localhost:8081`
    4. Database Connections
        - PostgreSQL (**Note**: Exposing database ports can have security implications.)
    5. To submit jobs from host machine:
        - `spark-submit --master spark://localhost:7077 your_spark_app.py`

## Prerequisites
- **Docker & Docker Compose:** Ensure Docker and Docker Compose are installed.
- **Sufficient System Resources:** Running multiple services simultaneously may require sufficient CPU, RAM, and disk space.
- **Network Ports:** Make sure the ports used by the services (e.g., 8080, 9092, 9021, 9090, etc.) are not being used by other applications.

## Input
- **Source API:** The input data comes from `Random User API` (https://randomuser.me/). The DAG we created for Airflow invokes the API every minute.
- **Kafka Topic `users_created`:** Fetched and processed user data is streamed into our Kafka topic.

## Output
- **Airflow UI Logs:** Real-time logs and status of DAGs.
- **Cassandra Table:** Processed user data is written by Spark into the `spark_streams.created_users` table.
- **Spark Streaming Logs:** The Spark driver and executor logs contain details about streaming operations.

## Notes
- **Customization:** We can modify the Airflow DAG (`kafka_stream.py`) to fetch data from a different API or perform additional transformations.
- **Security & Authentication:** This project is mainly for demonstration and development. For production environments, the best practice would be to add more security features (authentication, SSL, RBAC).
- **Monitoring & Observability:** We can leverage Control Center and Spark UI for monitoring.
- **Scaling Out:** We can add Spark workers or Kafka brokers can be added to the `docker-compose.yml` as needed.
