import argparse
import testtools
import spoonybard
from spoonybard.core.commands import Command, HelpCommand


class ExampleCommand(Command):
    def setup_parser(self):
        self.parser.add_argument('--things', help='Things to do')

spoonybard.engine.plugins.register_command_handler(
    'example', ExampleCommand)


class DummyChannel(object):
    def __init__(self):
        self.output = []
    def send(self, data):
        self.output.append(data)


class TestCommands(testtools.TestCase):
    def setUp(self):
        super().setUp()
        self.command = ExampleCommand('example')
        self.channel = DummyChannel()

    def test_arguments_get_parsed(self):
        self.command.parse_args('--things stuff')
        self.assertEqual(
            'stuff',
            self.command.args.things)

    def test_command_generates_usage_for_help(self):
        self.command.help(self.channel)
        self.assertEqual(
            ['usage: example [--things THINGS]\n'],
            self.channel.output)

    def test_incorrect_args(self):
        self.assertFalse(
            self.command.parse_args('--not-an-option bad-things'))


class TestHelpCommand(testtools.TestCase):
    def setUp(self):
        super(TestHelpCommand, self).setUp()
        self.command = HelpCommand('help')
        self.channel = DummyChannel()

    def test_gets_help_from_nominated_command(self):
        self.command.parse_args('example')
        self.command.execute(self.channel)
        self.assertEqual(
            ['usage: example [--things THINGS]\n'],
            self.channel.output)

    def test_help_for_unknown_command(self):
        self.command.parse_args('things')
        self.command.execute(self.channel)
        self.assertEqual(
            ['Could not find help for command: things\n'],
            self.channel.output)
