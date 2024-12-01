import logging
import textwrap
from pyspark.sql import SparkSession
from cassandra.cluster import Cluster
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

def create_keyspace(session):
    try:
        query = textwrap.dedent("""
            CREATE KEYSPACE IF NOT EXISTS spark_streams
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
        """)
        session.execute(query)
        logging.info("Keyspace 'spark_streams' created successfully!")
    except Exception as e:
        logging.error(f"Could not create keyspace 'spark_streams' due to: {e}")

def create_table(session):
    try:
        query = textwrap.dedent("""
            CREATE TABLE IF NOT EXISTS spark_streams.created_users (
                id UUID PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                gender TEXT,
                address TEXT,
                post_code TEXT,
                email TEXT,
                username TEXT,
                registered_date TEXT,
                phone TEXT,
                picture TEXT
            );
        """)
        session.execute(query)
        logging.info("Table 'created_users' created successfully in keyspace 'spark_streams'!")
    except Exception as e:
        logging.error(f"Could not create table 'created_users' due to: {e}")

def insert_data(session, **kwargs):
    logging.info("Inserting data...")
    try:
        query = """
            INSERT INTO spark_streams.created_users (
                id, first_name, last_name, gender, address, 
                post_code, email, username, dob, registered_date, phone, picture
            ) VALUES (
                %(id)s, %(first_name)s, %(last_name)s, %(gender)s, %(address)s, 
                %(post_code)s, %(email)s, %(username)s, %(dob)s, %(registered_date)s, %(phone)s, %(picture)s
            )
        """
        session.execute(query, kwargs)
        logging.info(f"Data inserted for {kwargs.get('first_name')} {kwargs.get('last_name')}")
    except Exception as e:
        logging.error(f"Could not insert data due to: {e}")

def create_spark_connection():
    try:
        packages = [
            "com.datastax.spark:spark-cassandra-connector_2.13:3.4.1",
            "org.apache.spark:spark-sql-kafka-0-10_2.13:3.4.1"
        ]
        spark_session = (
            SparkSession.builder
            .appName('SparkDataStreaming')
            .config('spark.jars.packages', ",".join(packages))
            .config('spark.cassandra.connection.host', 'localhost')
            .getOrCreate()
        )
        spark_session.sparkContext.setLogLevel("ERROR")
        logging.info("Spark connection created successfully!")
        return spark_session
    except Exception as e:
        logging.error(f"Couldn't create the Spark session due to exception: {e}")
        return None

def connect_to_kafka(spark_session):
    try:
        kafka_df = (
            spark_session.readStream
            .format('kafka')
            .option('kafka.bootstrap.servers', 'localhost:9092')
            .option('subscribe', 'users_created')
            .option('startingOffsets', 'earliest')
            .load()
        )
        logging.info("Kafka DataFrame created successfully.")
        return kafka_df
    except Exception as e:
        logging.warning(f"Kafka DataFrame could not be created because: {e}")
        return None

def create_cassandra_connection(contact_points=['localhost']):
    try:
        cluster = Cluster(contact_points)
        session = cluster.connect()
        logging.info("Cassandra connection established successfully.")
        return session
    except Exception as e:
        logging.error(f"Could not create Cassandra connection due to: {e}")
        return None

def create_selection_df_from_kafka(spark_df):
    schema = StructType([
        StructField("id", StringType(), nullable=False),
        StructField("first_name", StringType(), nullable=False),
        StructField("last_name", StringType(), nullable=False),
        StructField("gender", StringType(), nullable=False),
        StructField("address", StringType(), nullable=False),
        StructField("post_code", StringType(), nullable=False),
        StructField("email", StringType(), nullable=False),
        StructField("username", StringType(), nullable=False),
        StructField("registered_date", StringType(), nullable=False),
        StructField("phone", StringType(), nullable=False),
        StructField("picture", StringType(), nullable=False)
    ])
    selection_df = (
        spark_df.selectExpr("CAST(value AS STRING)")
        .select(from_json(col('value'), schema).alias('data'))
        .select("data.*")
    )
    logging.info("Selection DataFrame created successfully.")
    return selection_df

def main():
    # Create Spark connection
    spark_conn = create_spark_connection()
    if not spark_conn:
        logging.error("Spark connection could not be established. Exiting application.")
        return

    # Connect to Kafka with Spark connection
    spark_df = connect_to_kafka(spark_conn)
    if spark_df is None:
        logging.error("Failed to create Kafka DataFrame. Exiting application.")
        return

    # Create selection DataFrame from Kafka DataFrame
    selection_df = create_selection_df_from_kafka(spark_df)

    # Create Cassandra connection
    cassandra_session = create_cassandra_connection()
    if not cassandra_session:
        logging.error("Cassandra session could not be established. Exiting application.")
        return

    # Set up Cassandra keyspace and table
    create_keyspace(cassandra_session)
    create_table(cassandra_session)

    # Start streaming
    try:
        logging.info("Starting the streaming process...")
        streaming_query = (
            selection_df.writeStream
            .format("org.apache.spark.sql.cassandra")
            .option("checkpointLocation", "/tmp/checkpoint")
            .option("keyspace", "spark_streams")
            .option("table", "created_users")
            .start()
        )
        streaming_query.awaitTermination()
    except Exception as e:
        logging.error(f"An error occurred during streaming: {e}")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )
    main()