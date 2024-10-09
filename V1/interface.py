import requests
import json

def send_command_to_server(command):
    url = 'http://13.38.16.203:6000/run-command'  
    data = {'command': command}

    try:
        response = requests.post(url, json=data)

        if response.status_code == 200:
            print(f"Command '{command}' executed successfully.")
            return response.json()  
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return {'error': f"Failed to execute command: {command}"}

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        return {'error': f"Request failed: {str(e)}"}


if __name__ == '__main__':
    while True:
        command = input("Enter a command (e.g., 'run-program', 'git-update'): ")

        if command == 'exit':
            break
        
   
        result = send_command_to_server(command)
        print(json.dumps(result, indent=4))  
