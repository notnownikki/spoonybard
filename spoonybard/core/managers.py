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
        self.reset()

    def reset(self):
        self.plugins = set()
        self.job_handlers = {}
        self.command_handlers = {}

    def load(self, name, force_reload_if_unmanaged=False):
        if name in sys.modules and name not in self.plugins:
            # we're getting an already loaded module, which we has not been
            # loaded through PluginManager, return it from sys.modules and
            # add it to our list
            module = sys.modules[name]
            if force_reload_if_unmanaged:
                importlib.reload(module)
        else:
            module = importlib.import_module(name)
        self.plugins.add(name)
        return module

    def reload(self):
        self.job_handlers = {}
        for name in self.plugins:
            module = importlib.import_module(name)
            importlib.reload(module)

    def register_job_handler(self, handler_name, handler):
        self.job_handlers[handler_name] = handler

    def get_job_handler(self, name):
        return self.job_handlers.get(name)

    def register_command_handler(self, handler_name, handler):
        self.command_handlers[handler_name] = handler

    def get_command_handler(self, name):
        klass = self.command_handlers.get(name)
        if klass is None:
            return
        return klass(name)
