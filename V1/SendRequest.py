import requests

# Step 1: Send the URL to start the program
flask_app_url = "http://13.38.16.203:5000/run-program"
api_base_url = "http://asset23d.ir"  # External API

data = {
    "url": api_base_url
}

response = requests.post(flask_app_url, json=data)
print("Response from running the program:")
print(response.json())

# Step 2: Check if the file was saved successfully
flask_app_url = "http://13.38.16.203:5000/list-files/relationmatrix.json"  # Flask URL to get the saved file
response = requests.get(flask_app_url)

print("Response from getting file content:")
try:
    print(response.json())
except ValueError:
    print("Error: Could not decode JSON response.")
