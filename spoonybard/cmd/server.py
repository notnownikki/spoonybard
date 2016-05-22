import ConfigParser
import argparse
import importlib
import spoonybard

from flask import Flask

setattr(spoonybard, 'flaskapp', Flask('spoonybard'))


def _run_flask(plugin_list, host, port):
    app = spoonybard.flaskapp
    print app.__hash__
    for plugin in plugin_list:
        importlib.import_module(plugin)
    app.run(host=host, port=port)

def main():
    parser = argparse.ArgumentParser(description='Run the spoonybard server.')
    parser.add_argument('-c', help='Configuration file path')
    args = parser.parse_args()
    config = ConfigParser.ConfigParser()
    config.readfp(open(args.c, 'r'))
    plugin_list = config.get('server', 'plugins').split(',')
    host = config.get('server', 'host')
    port = config.get('server', 'port')
    _run_flask(plugin_list, host, port)
