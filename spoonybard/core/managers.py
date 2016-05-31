import importlib
import yaml


class ConfigManager(object):
    def __init__(self):
        self.config = {}
        self.filename = None

    def get(self):
        return self.config

    def load(self, filename):
        self.filename = filename
        with open(filename, 'r') as stream:
            self.config = yaml.load(stream)

    def reload(self):
        self.load(self.filename)


class PluginManager(object):
    def __init__(self):
        self.plugins = {}

    def get(self, name):
        if name not in self.plugins:
            self.plugins[name] = importlib.import_module(name)
        return self.plugins[name]

    def reload(self):
        for name in self.plugins:
            plugin = self.plugins[name]
            importlib.reload(plugin)
            self.plugins[name] = plugin
