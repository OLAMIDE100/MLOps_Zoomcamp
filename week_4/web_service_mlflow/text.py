import requests

rides = {
'PULocationID': 10,
'DOLocationID': 50,
'trip_distance': 40

}

url = "http://localhost:9696/predict"

response = requests.post(url,json=rides)

print(response.json())

