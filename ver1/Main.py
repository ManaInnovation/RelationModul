from flask import Flask, jsonify,request
import subprocess
import os
import logging
import EntityBehave


app = Flask(__name__)
#logging.basicConfig(level=logging.DEBUG)
# @app.route('/')
# def hello_world():
#     return 'Hello from Flask!'

@app.route('/run-program', methods=['GET'])
# @app.route('/run-program', methods=['POST'])
def run_program():
   

     try:
          relation_matrix = EntityBehave.V2RelationMatrix()
          relation_matrix.StartProcess()

          myjson = relation_matrix.Array3d
          return jsonify(myjson)
          
     except Exception as e:
          return jsonify({"result": "error occurred", "message": str(e)})

          
@app.route('/run-command', methods=['POST'])
def run_command():
    
          command = request.json.get('command')
          if not command:
               return jsonify({"error": "No command provided"}), 400
     
          try:
               result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
               output = result.stdout
               error = result.stderr
               return jsonify({
               "command": command,
               "output": output,
               "error": error
          })

          except subprocess.CalledProcessError as e:
          # Return any error that occurs during execution
               return jsonify({
                    "command": command,
                    "error": str(e),
                    "output": e.output
               }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)
