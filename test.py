import requests

BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE + "game/1", {"likes": 10, "name": "Seongjong", "views": 100})
print(response.json())
input()
response = requests.get(BASE + "game/1", {"likes": 10})
print(response.json())