import requests
import argparse
import json

def run_command(command):
    url = 'http://13.38.16.203:6000/run-command'
    data = {'command': command}
    response = requests.post(url, json=data)

    # Print the status code and response text
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    # If the response is successful, decode the JSON
    if response.ok:
        print(response.json())
    else:
        return {'error': f'Failed to execute command: {response.status_code}', 'output': ''}
def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Run a command on the server and return the output in JSON format.')
    parser.add_argument('command', type=str, help='The command to execute on the server.')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run the command and get the output
    result = run_command(args.command)
    
    # Print the result as a JSON string
    print(json.dumps(result, indent=4))

if __name__ == '__main__':
    main()