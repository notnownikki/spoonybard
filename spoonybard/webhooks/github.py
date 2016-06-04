import json
import spoonybard
from flask import request

"""
Work in progress testing code. Not tested. Will probably disappear.
"""

app = spoonybard.flaskapp


@app.route('/github/', methods=['POST'])
def githubpr():
    payload = json.loads(request.form['payload'])
    return payload
