import uuid
import requests
    import json
    import time
    import logging
from airflow import DAG
from datetime import datetime
    from kafka import KafkaProducer
from airflow.operators.python import PythonOperator

def get_data():
    res = requests.get("https://randomuser.me/api/")
    res = res.json()
    res = res['results'][0]
    return res

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 3, 12, 00)
}