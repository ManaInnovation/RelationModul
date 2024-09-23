from flask import Flask, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/run-program')
def run_program():
    
    program_env_python = 'C:/Users/win11/miniconda3/envs/myprogramenv/python.exe'
   
    program_script_path = 'D:/projects/Git_projects/RelationModul/mini_flask_project/ver3/EntityBehave.py'
    
    result = subprocess.run([program_env_python, program_script_path], capture_output=True, text=True)
    
    return jsonify({'stdout': result.stdout, 'stderr': result.stderr})

if __name__ == '__main__':
    app.run(debug=True)
