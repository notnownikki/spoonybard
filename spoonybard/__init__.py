from spoonybard.core.engines import BardCore
from spoonybard.core.managers import PluginManager, ConfigManager
from spoonybard.core.webserver import WebServer


engine = BardCore()
engine.plugins = PluginManager()
engine.config = ConfigManager()
engine.webserver = WebServer(PluginManager())


# import core plugins
engine.plugins.load('spoonybard.core.handlers')
