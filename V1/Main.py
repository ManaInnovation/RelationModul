from flask import Flask, jsonify,request
import subprocess
import os
import logging
import EntityBehave


app = Flask(__name__)

@app.route('/run-program', methods=['POST'])
def run_program():
    try:
        # Retrieve the URL from the request body (use default if not provided)
        curentURL = request.json.get('url')
        
        # Run the program
        EntityBehave.run_entity_behave(curentURL)

        return jsonify({"message": "Program started successfully with URL: {}".format(curentURL), "status": "running"})
    
    except Exception as e:
        logging.error(f"An error occurred while starting the program: {e}")
        return jsonify({"error": "Failed to run the program", "details": str(e)}), 500


@app.route('/list-files/relationmatrix.json', methods=['GET'])
def list_files():
    try:
        # Directory path where files are saved
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'relationmatrix.json')
        # Get a list of files in the directory
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404
        
        # Read the content of the file
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Return the content of the file in JSON format
        return jsonify({"content": content})
    except Exception as e:
        logging.error(f"Error while reading file: {e}")
        return jsonify({"error": "Failed to read file", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

