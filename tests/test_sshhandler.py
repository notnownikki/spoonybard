import testtools
import paramiko
from mock import patch, MagicMock
from spoonybard.core.ssh import SSHHandler


class TestableHandler(SSHHandler):
	def __init__(self):
		pass


class SSHHandlerTestCase(testtools.TestCase):
	def setUp(self):
		super(SSHHandlerTestCase, self).setUp()
		self.sshhandler = TestableHandler()

	@patch.object(paramiko, 'Transport')
	def test_hostkey_added_from_configuration(self, mock_transport):
		pass

	def test_getting_command_times_out(self):
		pass

	def test_channel_failure_closes_transport(self):
		pass

	def test_command_got_from_channel(self):
		pass

	def test_command_executed(self):
		pass
