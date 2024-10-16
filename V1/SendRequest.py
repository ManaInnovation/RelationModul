import requests

# URL for the Flask app's endpoint
flask_app_url = "http://13.38.16.203:5000/run-program"

# The actual API server URL that will be used by the EntityBehave program
api_base_url = "http://asset23d.ir.com"

# Data payload to send with the POST request
data = {
    "url": api_base_url
}

# Send a POST request to the Flask app
response = requests.post(flask_app_url, json=data)

# Print the response from the server
print(response.json())
