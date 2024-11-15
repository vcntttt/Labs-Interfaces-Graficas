import time
import os
import requests

def sendIMG(img):
    print(f"Enviando imagen {img}")
    url = "http://127.0.0.1:5000/img/upload"
    files = {'file': open(img, 'rb')}
    response = requests.post(url, files=files)
    print(response.text)

imgPath = "ejercicio1/IMG"
files = os.listdir(imgPath)
for file in files:
    sendIMG(f"{imgPath}/{file}")
    time.sleep(3)