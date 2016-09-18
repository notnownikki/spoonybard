import testtools
import paramiko
from mock import patch, MagicMock
from spoonybard.core.ssh import SSHHandler


class TestableHandler(SSHHandler):
	def __init__(self):
		# The SSHHandler is a stream request handler, that expects all
		# kinds of request related things. Instead of mocking it, this
		# class allows us to supply things in a more readable way.
		# Don't judge me.
		pass


class SSHHandlerTestCase(testtools.TestCase):
	def setUp(self):
		super().setUp()
		self.sshhandler = TestableHandler()

	def test_hostkey_added_from_configuration(self):
		pass

	def test_getting_command_times_out(self):
		pass

	def test_channel_failure_closes_transport(self):
		pass

	def test_command_got_from_channel(self):
		pass

	def test_command_executed(self):
		pass
