import os
import shutil
import testtools
from types import ModuleType
import spoonybard
from spoonybard.core.managers import PluginManager


PLUGIN_SRC = """
from spoonybard import engine

def funfunfun():
    return "%s"

engine.plugins.register_job_handler('testjh', funfunfun)
"""

class PluginManagerTestCase(testtools.TestCase):
    def _create_test_plugin(self, return_value):
        shutil.rmtree('test_plugin', ignore_errors=True)
        os.mkdir('test_plugin')
        fp = open('test_plugin/__init__.py', 'w')
        fp.write(PLUGIN_SRC % return_value)
        fp.close()

    def setUp(self):
        super(PluginManagerTestCase, self).setUp()
        self._create_test_plugin('Default')
        spoonybard.engine.plugins.reload()

    def tearDown(self):
        super(PluginManagerTestCase, self).tearDown()
        shutil.rmtree('test_plugin', ignore_errors=True)

    def test_plugin_imported(self):
        plugin = spoonybard.engine.plugins.load('test_plugin')
        self.assertEqual(
            'Default',
            plugin.funfunfun())

    def test_reload_plugin(self):
        plugin = spoonybard.engine.plugins.load('test_plugin')
        self._create_test_plugin('New Code')
        self.assertEqual(
            'Default',
            plugin.funfunfun())
        spoonybard.engine.plugins.reload()
        plugin = spoonybard.engine.plugins.load('test_plugin')
        self.assertEqual(
            'New Code',
            plugin.funfunfun())

    def test_register_job_handler(self):
        plugin = spoonybard.engine.plugins.load('test_plugin')
        handler = spoonybard.engine.plugins.get_job_handler('testjh')
        self.assertEqual(
            'Default',
            handler())

    def test_job_handler_is_reloaded(self):
        plugin = spoonybard.engine.plugins.load('test_plugin')
        spoonybard.engine.plugins.register_job_handler('test', plugin.funfunfun)
        self._create_test_plugin('Reloaded handler')
        spoonybard.engine.plugins.reload()
        handler = spoonybard.engine.plugins.get_job_handler('testjh')
        self.assertEqual(
            'Reloaded handler',
            handler())
