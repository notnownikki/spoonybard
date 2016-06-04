import importlib
import sys
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
        self.job_handlers = {}

    def get(self, name):
        if name not in self.plugins:
            path = name.split('.')
            module_name = '.'.join(path[:-1])
            plugin_name = path[-1]
            self.plugins[name] = getattr(
                importlib.import_module(module_name), plugin_name)
        return self.plugins[name]

    def reload(self):
        for name in self.plugins:
            path = name.split('.')
            plugin_name = path[-1]
            plugin = self.plugins[name]
            reloaded_module = importlib.reload(sys.modules[plugin.__module__])
            self.plugins[name] = getattr(reloaded_module, plugin_name)

    def register_job_handler(self, handler_name, handler_plugin_name):
        self.job_handlers[handler_name] = handler_plugin_name

    def get_job_handler(self, name):
        return self.get(self.job_handlers[name])
