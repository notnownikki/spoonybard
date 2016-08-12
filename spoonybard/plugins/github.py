import json
import spoonybard
from flask import request
from spoonybard.core.triggers import ChangeTrigger

"""
Work in progress testing code. Not tested. Will probably disappear.
"""


class GithubChange(ChangeTrigger):
    def __init__(self, payload):
        self.payload = payload

    def match(self, job):
        pass

    def update(self, results):
        pass


@spoonybard.webserver.flask_app.route('/github-pr/', methods=['POST'])
def githubpr():
    payload = json.loads(request.form['payload'])
    spoonybard.engine.queue_change(GithubChange(payload))
    return payload
