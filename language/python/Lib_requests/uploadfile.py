import requests

files = {'file':open('Python.png','rb')}

response = requests.post('http://127.0.0.1:5000/upload',files=files)