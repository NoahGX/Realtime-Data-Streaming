#!/bin/zsh
set -e

if [ -e "/opt/airflow/requirements.txt" ]; then
  python -m pip install --upgrade pip
  python -m pip install --user -r /opt/airflow/requirements.txt
fi

if [ ! -f "/opt/airflow/airflow.db" ]; then
  airflow db init
  airflow users create \
    --username admin \
    --password admin \
    --email admin@example.com \
    --firstname admin \
    --lastname admin \
    --role Admin
fi

airflow db upgrade

exec airflow webserver
