#!/usr/bin/env bash
set -euo pipefail

AIRFLOW_HOME="/opt/airflow"
REQUIREMENTS_FILE="$AIRFLOW_HOME/requirements.txt"
DB_FILE="$AIRFLOW_HOME/airflow.db"

# Install requirements if 'requirements.txt' exists
if [[ -f "$REQUIREMENTS_FILE" ]]; then
  python -m pip install --upgrade pip
  python -m pip install --user -r "$REQUIREMENTS_FILE"
fi

# Initialize an Airflow database
# Create an admin user if the database does not exist
if [[ ! -f "$DB_FILE" ]]; then
  airflow db init
  airflow users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --password admin \
    --email admin@example.com \
    --role Admin
fi

# Upgrade the Airflow database
airflow db upgrade

# Start the Airflow webserver
exec airflow webserver