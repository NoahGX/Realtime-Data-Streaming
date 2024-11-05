import requests
from datetime import datetime

def stream_data():
    res = requests.get("https://randomuser.me/api/")
    print(res.json())


stream_data()