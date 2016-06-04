import importlib
from spoonybard.core.managers import PluginManager, ConfigManager

plugins = PluginManager()
config = ConfigManager()

# import core plugins
importlib.import_module('spoonybard.core.handlers')
