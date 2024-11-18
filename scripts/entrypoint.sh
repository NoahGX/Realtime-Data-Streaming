#!/bin/bash
set -e

# Install Python packages if requirements.txt exists
if [ -f "/opt/airflow/requirements.txt" ]; then
  # Upgrade pip using the Python interpreter
  python -m pip install --upgrade pip
  # Install requirements from the specified file
  pip install --user -r /opt/airflow/requirements.txt
fi

# Initialize the Airflow database if it doesn't exist
if [ ! -f "/opt/airflow/airflow.db" ]; then
  airflow db init
  airflow users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@example.com \
    --password admin
fi

# Upgrade the Airflow database to the latest version
airflow db upgrade

# Start the Airflow webserver
exec airflow webserver
