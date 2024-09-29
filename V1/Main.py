from flask import Flask, jsonify, request
import subprocess
import EntityBehave

app = Flask(__name__)

subprocess.run('pwd')