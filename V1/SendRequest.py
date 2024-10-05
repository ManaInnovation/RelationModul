import requests


url = 'http://13.38.16.203:6000/run-command'
data = {'command': 'ls -l'}
response = requests.post(url, json=data)
print(response.json())




# Print the status code and response text
print("Status Code:", response.status_code)
print("Response Text:", response.text)

# If the response is successful, decode the JSON
if response.ok:
    print(response.json())
else:
    print("Failed to get a valid JSON response.")