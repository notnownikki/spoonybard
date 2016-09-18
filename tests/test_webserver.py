import os
import shutil
import spoonybard
import testtools
from spoonybard.core.webserver import WebServer
from spoonybard.core.managers import ConfigManager, PluginManager


WEBSERVER_CONFIG = """
webserver:
  host: 127.0.0.42
  port: 9404
  plugins:
    - tests.plugin_a
"""

EXTRA_PLUGIN_WEBSERVER_CONFIG = """
webserver:
  host: 127.0.0.42
  port: 9404
  plugins:
    - tests.plugin_a
    - tests.plugin_b
"""


WEB_PLUGIN_SRC = """
from spoonybard import engine

app = engine.webserver.flask_app


def hello_world():
    return '%s'

app.add_url_rule('%s', '%s', hello_world)
"""


class WebserverTestCase(testtools.TestCase):
    """
    Because spoonybard sets up the engine with a webserver,
    we have to interact with it, otherwise we'll have two
    webservers going on and that could be bad. So this is
    halfway between a unit test and an integration test.
    Sorry.
    """
    def setUp(self):
        super().setUp()
        self.generated_plugins = []
        self.cfg_filename = '_test_webserver_cfg.yml'

    def init_webserver(self, cfg_yaml=WEBSERVER_CONFIG):
        fp = open(self.cfg_filename, 'w')
        fp.write(cfg_yaml)
        fp.close()
        config = ConfigManager()
        config.load(self.cfg_filename)
        self.webserver = spoonybard.engine.webserver
        self.webserver.load(config)

    def tearDown(self):
        super().tearDown()
        os.remove(self.cfg_filename)
        path = os.path.dirname(__file__)
        for generated in self.generated_plugins:
            shutil.rmtree(os.path.join(path, generated))

    def generate_plugin(
            self, plugin_name, url_path='/', view_name='hello_world',
            output_text='Hello, World!'):
        path = os.path.dirname(__file__)
        if os.path.exists(os.path.join(path, plugin_name)):
            shutil.rmtree(os.path.join(path, plugin_name))
        os.mkdir(
            os.path.join(path, plugin_name))
        plugin_src = WEB_PLUGIN_SRC % (output_text, url_path, view_name)
        fp = open(os.path.join(path, plugin_name, '__init__.py'), 'w')
        fp.write(plugin_src)
        fp.close()
        if plugin_name not in self.generated_plugins:
            self.generated_plugins.append(plugin_name)

    def test_webserver_loads_plugins(self):
        self.generate_plugin('plugin_a')
        self.init_webserver(WEBSERVER_CONFIG)
        flask_app = self.webserver.flask_app
        response_from_plugin = flask_app.test_client().get('/')
        self.assertEqual(
            b'Hello, World!',
            response_from_plugin.get_data())

    def test_webserver_reloads(self):
        self.generate_plugin('plugin_a')
        self.init_webserver(WEBSERVER_CONFIG)
        flask_app = self.webserver.flask_app
        response_from_plugin = flask_app.test_client().get('/')
        self.assertEqual(
            b'Hello, World!',
            response_from_plugin.get_data())
        response_from_plugin = flask_app.test_client().get('/hello/')
        self.assertEqual(
            404,
            response_from_plugin.status_code)

        self.generate_plugin('plugin_a', '/', 'index', 'New index.')
        self.generate_plugin('plugin_b', '/hello/', 'hello', 'Hello there!')
        self.init_webserver(EXTRA_PLUGIN_WEBSERVER_CONFIG)
        flask_app = self.webserver.flask_app
        response_from_plugin = flask_app.test_client().get('/')
        self.assertEqual(
            b'New index.',
            response_from_plugin.get_data())
        response_from_plugin = flask_app.test_client().get('/hello/')
        self.assertEqual(
            b'Hello there!',
            response_from_plugin.get_data())
