import argparse
import importlib
import spoonybard
from flask import Flask

setattr(spoonybard, 'flaskapp', Flask('spoonybard'))


def _run_flask(plugin_list, host, port):
    app = spoonybard.flaskapp
    plugin_list += ['spoonybard.server.core']
    for plugin in plugin_list:
        importlib.import_module(plugin)
    app.run(host=host, port=port)

def main():
    parser = argparse.ArgumentParser(description='Run the spoonybard server.')
    parser.add_argument('-c', help='Configuration file path')
    args = parser.parse_args()
    spoonybard.load_config(args.c)
    plugin_list = spoonybard.config.get('server', 'plugins').split(',')
    host = spoonybard.config.get('server', 'host')
    port = spoonybard.config.get('server', 'port')
    _run_flask(plugin_list, host, port)
