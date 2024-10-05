from flask import Flask, jsonify, request
import subprocess
import os
import psutil  # To check if the process is running

app = Flask(__name__)

# Variable to track the program status (whether it's running or not)
program_status = "stopped"
process = None  # To store the process handle of the running program

@app.route('/run-command', methods=['POST'])
def run_command():
    global program_status, process  # Access the global variable for program status
    command = request.json.get('command')
    print(f"Received command: {command}")  # Print the received command
    
    if not command:
        return jsonify({"error": "No command provided"}), 400

    # Handle special commands
    if command == 'run-program':
        if program_status == "running":
            return jsonify({"message": "Program is already running", "status": "running"})
        else:
            try:
                # Start the EntityBehave program as a subprocess
                process = subprocess.Popen(["python3", "EntityBehave.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                program_status = "running"
                return jsonify({"message": "Program started successfully", "status": "running"})
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    elif command == 'check-status':
        if program_status == "running":
            if process.poll() is None:  # Process is still running
                return jsonify({"message": "Program is running", "status": "running"})
            else:  # Process has terminated
                program_status = "stopped"
                process = None
                return jsonify({"message": "Program is not running anymore", "status": "stopped"})
        else:
            return jsonify({"message": "Program is not running", "status": "stopped"})

    elif command == 'stop-program':
        if program_status == "stopped":
            return jsonify({"message": "Program is not running", "status": "stopped"})
        else:
            try:
                if process is not None:
                    process.terminate()  # Terminate the process
                    process.wait()  # Wait for the process to finish
                    process = None
                    program_status = "stopped"
                return jsonify({"message": "Program stopped successfully", "status": "stopped"})
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    elif command == 'git-update':
        try:
            result = subprocess.run(['git', 'pull'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return jsonify({"message": "Git update performed", "output": result.stdout, "error": result.stderr})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif command == 'git-clone':
        # Example: Cloning a repository (change the URL as needed)
        repo_url = 'https://github.com/your/repository.git'
        try:
            result = subprocess.run(['git', 'clone', repo_url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return jsonify({"message": "Repository cloned", "output": result.stdout, "error": result.stderr})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # If command does not match any specific case, run it as a generic shell command
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        error = result.stderr
        print(f"Command output: {output}")  # Print the command output
        return jsonify({
            "command": command,
            "output": output,
            "error": error
        })

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {str(e)}")  # Print the error message
        return jsonify({
            "command": command,
            "error": str(e),
            "output": e.output
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)
