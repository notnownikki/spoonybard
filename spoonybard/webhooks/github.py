import json
import spoonybard
from flask import request

app = spoonybard.flaskapp

@app.route('/github/', methods=['POST'])
def githubpr():
    payload = json.loads(request.form['payload'])
    return "Hello, Github!"
