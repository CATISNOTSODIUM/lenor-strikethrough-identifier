import requests
import json
url = 'http://localhost:8080/upload'
fp = 'input.jpeg' # to fix

text_path = 'input.txt'

with open(text_path, 'r') as file:
    file_content = file.read()

def send():
    files = {'image': open(fp, 'rb')}
    payload = {'coordinates': file_content}

    response = requests.post(url, files=files, data=payload, verify=False)
    print(response.json()["message"])

send()