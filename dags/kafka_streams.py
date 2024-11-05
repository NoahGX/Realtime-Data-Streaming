import requests
from datetime import datetime

def stream_data():
    res = requests.get("https://randomuser.me/api/")
    res = res.json()
    res = res['results'][0]
    print(res)

stream_data()