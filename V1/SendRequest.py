import requests

#to just send data
flask_app_url = "http://13.38.16.203:5000/run-program"
api_base_url = "http://asset23d.ir.com"
data = {
    "url": api_base_url
}
response = requests.post(flask_app_url, json=data)
# Print the response from the server
print(response.json())




#to check saved files
flask_app_url = "http://13.38.16.203:5000/list-files/relationmatrix.json"  # Change to your server's IP and filename
response = requests.get(flask_app_url)
try:
    print(response.json())
except ValueError:
    print("Error: Could not decode JSON response.")