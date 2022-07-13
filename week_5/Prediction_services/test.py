import requests

url = 

ride = {}

response = requests.post(url,json=ride).json()

print(response)