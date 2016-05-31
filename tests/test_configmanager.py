import os
import testtools
from spoonybard.core.managers import ConfigManager


class ConfigManagerTestCase(testtools.TestCase):
    def _create_test_config(self, config_value):
        fp = open('_test_config.yml', 'w')
        fp.write('section:\n  key: %s' % config_value)
        fp.close()

    def setUp(self):
        super(ConfigManagerTestCase, self).setUp()
        self._create_test_config('Default')
        self.configmanager = ConfigManager()
        self.configmanager.load('_test_config.yml')

    def tearDown(self):
        super(ConfigManagerTestCase, self).tearDown()
        os.remove('_test_config.yml')

    def test_get_config(self):
        cfg = self.configmanager.get()
        self.assertEqual(
            'Default',
            cfg['section']['key'])

    def test_reload_config(self):
        self._create_test_config('New')
        self.configmanager.reload()
        cfg = self.configmanager.get()
        self.assertEqual(
            'New',
            cfg['section']['key'])
