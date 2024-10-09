from flask import Flask, jsonify, request
import subprocess
import EntityBehave
import os


app = Flask(__name__)


program_status = "stopped"
process = None  

@app.route('/run-command', methods=['POST'])
def run_command():
    global program_status, process
    command = request.json.get('command')
    CurentURL = request.json.get('URL')

    if command == 'run-program':
        if program_status == "running":
            return jsonify({"message": "Program is already running", "status": "running"})
        else:
            try:
                
                EntityBehave.run_entity_behave(CurentURL)
                #process = subprocess.Popen(["python3", "./EntityBehave.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                program_status = "running"
                return jsonify({"message": "Program started successfully", "status": "running"})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            
    elif command == 'check-status':
        if program_status == "running":
            return jsonify({"message": "Program is running", "status": "running"})
        else:
            return jsonify({"message": "Program is not running", "status": "stopped"})

    elif command == 'stop-program':
        if program_status == "stopped":
            return jsonify({"message": "Program is not running", "status": "stopped"})
        else:
            program_status = "stopped"
            return jsonify({"message": "Program stopped successfully", "status": "stopped"})

    elif command == 'git-update':
        try:
            result = subprocess.run(['git', 'pull'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return jsonify({"message": "Git update performed", "output": result.stdout, "error": result.stderr})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif command == 'git-clone':
        
        repo_url = 'https://github.com/your/repository.git'
        try:
            result = subprocess.run(['git', 'clone', repo_url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return jsonify({"message": "Repository cloned", "output": result.stdout, "error": result.stderr})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        error = result.stderr
        print(f"Command output: {output}")  
        return jsonify({
            "command": command,
            "output": output,
            "error": error
        })

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {str(e)}")  
        return jsonify({
            "command": command,
            "error": str(e),
            "output": e.output
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)
