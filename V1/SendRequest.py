import requests
url = 'http://13.38.16.203:5000/run-command'
data = {'command': 'ls -l'}
response = requests.post(url, json=data)
print(response.json())





