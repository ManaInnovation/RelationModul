from flask import Flask, jsonify
import subprocess
import os
import logging
import EntityBehave


app = Flask(__name__)

#logging.basicConfig(level=logging.DEBUG)

# @app.route('/')
# def hello_world():

#     return 'Hello from Flask!'

@app.route('/run-program')
# @app.route('/run-program', methods=['POST'])
def run_program():
   

   
     try:
          relation_matrix = EntityBehave.V2RelationMatrix()
          relation_matrix.StartProcess()

          myjson = relation_matrix.Array3d
          return myjson
          
     except:
          return '{"result":"error occured"}'
          
     

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
