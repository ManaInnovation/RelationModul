from flask import Flask, jsonify, request
import subprocess
import EntityBehave

app = Flask(__name__)

@app.route('/run-command', methods=['POST'])
def run_command():
    command = request.json.get('command')
    print(f"Received command: {command}")  
    if not command:
        return jsonify({"error": "No command provided"}), 400

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
