from flask import Flask, jsonify
import subprocess
import os
import logging

app = Flask(__name__)

#logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/run-program', methods=['POST'])
def run_program():
    #program_env_python = 'C:/Users/win11/miniconda3/envs/myprogramenv/python.exe'
    program_env_python = 'C:/Users/win11/AppData/Local/Microsoft/WindowsApps/python3.exe'
    #program_env_python = "/home/ubuntu/miniconda3/envs/myprogramenv/bin/python"

   
    program_script_path = 'D:/projects/Git_projects/RelationModul/mini_flask_project/ver3/EntityBehave.py'
    
    result = subprocess.run([program_env_python, program_script_path], capture_output=True, text=True)
    
    return jsonify({'stdout': result.stdout, 'stderr': result.stderr})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
