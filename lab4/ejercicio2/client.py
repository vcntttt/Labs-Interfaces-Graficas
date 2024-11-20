import time
import requests
import random


def sendData(data):
    url = "http://127.0.0.1:5000/contaminacion/upload"
    response = requests.post(url, json=data)
    print(response.text)

def Generate():
    dMP_Data = {
        'N1': [{
            'd01': random.randint(0, 10),
            'd25': random.randint(0, 10),
            'd10': random.randint(0, 10),
        }],
        'N2': [{
            'd01': random.randint(0, 10),
            'd25': random.randint(0, 10),
            'd10': random.randint(0, 10),
        }],
        'N3': [{
            'd01': random.randint(0, 10),
            'd25': random.randint(0, 10),
            'd10': random.randint(0, 10),
        }]
    }

    return dMP_Data


for _ in range(100):
    sendData(Generate())
    time.sleep(1)