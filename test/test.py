import requests
import json
url = 'http://localhost:8080/upload'
fp = 'input.jpeg'

text_path = 'input.txt'

with open(text_path, 'r') as file:
    file_content = file.read()
    
files = {'image': open(fp, 'rb')}
payload = {'coordinates': file_content}

response = requests.post(url, files=files, data=payload, verify=False)
print(response.text)