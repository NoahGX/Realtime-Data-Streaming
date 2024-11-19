import uuid
import json
import logging
import requests
from airflow import DAG
from kafka import KafkaProducer
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

# Default arguments for the DAG
default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2024, 11, 18, 12, 00),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Fetch data from the randomuser.me API.
def get_data():
    try:
        response = requests.get("https://randomuser.me/api/")
        response.raise_for_status()
        data = response.json()['results'][0]
        return data
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        raise

# Format the API response into the desired structure.
def format_data(res):
    location = res['location']
    data = {
        'id': str(uuid.uuid4()),
        'first_name': res['name']['first'],
        'last_name': res['name']['last'],
        'gender': res['gender'],
        'address': f"{location['street']['number']} {location['street']['name']}, "
                   f"{location['city']}, {location['state']}, {location['country']}",
        'post_code': location['postcode'],
        'email': res['email'],
        'username': res['login']['username'],
        'dob': res['dob']['date'],
        'registered_date': res['registered']['date'],
        'phone': res['phone'],
        'picture': res['picture']['medium'],
    }
    return data

# Fetch, format, and send data to the Kafka topic.
def stream_data():
    producer = None
    try:
        producer = KafkaProducer(bootstrap_servers=['broker:29092'])
        res = get_data()
        formatted_data = format_data(res)
        producer.send('users_created', json.dumps(formatted_data).encode('utf-8'))
        producer.flush()
        logging.info("Data successfully sent to Kafka.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise
    finally:
        if producer:
            producer.close()

# Define the DAG
with DAG(
    'user_automation',
    default_args=default_args,
    schedule_interval='*/1 * * * *',    # Every minute
    catchup=False,
) as dag:

    streaming_task = PythonOperator(
        task_id='stream_data_from_api',
        python_callable=stream_data,
    )
