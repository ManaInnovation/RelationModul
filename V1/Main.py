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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

