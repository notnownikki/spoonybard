import flask


class WebServer(object):
    def __init__(self, plugins):
        self.flask_app = flask.Flask('spoonybard')
        self.plugins = plugins

    def load(self, config):
        self.flask_app = flask.Flask('spoonybard')
        plugins = config.get()['webserver']['plugins']
        self.plugins.reset()
        for plugin_name in plugins:
            self.plugins.load(
                plugin_name, force_reload_if_unmanaged=True)
