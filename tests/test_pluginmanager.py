import os
import shutil
import testtools
from spoonybard.core.managers import PluginManager


class PluginManagerTestCase(testtools.TestCase):
    def _create_test_plugin(self, return_value):
        shutil.rmtree('test_plugin', ignore_errors=True)
        os.mkdir('test_plugin')
        fp = open('test_plugin/__init__py', 'w')
        fp.close()
        fp = open('test_plugin/things.py', 'w')
        fp.write('def funfunfun(): return "%s"' % return_value)
        fp.close()

    def setUp(self):
        super(PluginManagerTestCase, self).setUp()
        self._create_test_plugin('Default')
        self.pluginmanager = PluginManager()

    def tearDown(self):
        super(PluginManagerTestCase, self).tearDown()
        shutil.rmtree('test_plugin', ignore_errors=True)

    def test_plugin_imported(self):
        plugin = self.pluginmanager.get('test_plugin.things.funfunfun')
        self.assertEqual(
            'Default',
            plugin())

    def test_reload_plugin(self):
        plugin = self.pluginmanager.get('test_plugin.things.funfunfun')
        self._create_test_plugin('New Code')
        self.assertEqual(
            'Default',
            plugin())
        self.pluginmanager.reload()
        plugin = self.pluginmanager.get('test_plugin.things.funfunfun')
        self.assertEqual(
            'New Code',
            plugin())

    def test_register_job_handler(self):
        self.pluginmanager.register_job_handler(
            'thing', 'test_plugin.things.funfunfun')
        plugin = self.pluginmanager.get_job_handler('thing')
        self.assertEqual(
            'Default',
            plugin())
