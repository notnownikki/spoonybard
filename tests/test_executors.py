import testtools
import os
from io import StringIO
from mock import patch, Mock
from spoonybard.core.executors import Executor, LocalExecutor, SSHExecutor


BASH_SCRIPT = """#!/bin/bash -e

echo HELLO
"""


class ExecutorTestCase(testtools.TestCase):
    def test_executor_logs_stream_output(self):
        script = 'first line\nsecond line\nthird line'
        executor = DummyExecutor()
        executor.run(script)
        log = executor.get_log()
        self.assertEqual(
            ['first line\n', 'second line\n', 'third line'],
            log)


class LocalExecutorTestCase(testtools.TestCase):
    def test_executor_runs_script_locally(self):
        executor = LocalExecutor()
        executor.run(BASH_SCRIPT)
        log = executor.get_log()
        self.assertEqual(
            [b'HELLO\n'],
            log)
    def test_executor_records_exit_code(self):
        executor = LocalExecutor()
        exit_code = executor.run(BASH_SCRIPT)
        self.assertEqual(
            0,
            exit_code)
    def test_executor_deletes_tmp_script(self):
        executor = LocalExecutor()
        executor.run(BASH_SCRIPT)
        self.assertFalse(
            os.path.exists(executor.tmp_script_filename))


# ==============================================
# Dummy executors for testing core functionality

class DummyExecutor(Executor):
    """just echoes back the script passed to run"""
    def run_script(self, script):
        self.stream = StringIO(script)

    def get_exit_code(self):
        return 0
