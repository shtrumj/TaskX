import requests
BASE = "http://127.0.0.1:8765/"

response = requests.get(BASE + "ser/37")
print(response.json())