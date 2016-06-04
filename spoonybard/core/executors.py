import tempfile
import os
import subprocess


class Executor(object):
    def __init__(self, config={}):
        self.config = config
        self.log = []

    def run(self, script):
        self.setup_stream(script)
        line = self.stream.readline()
        while line:
            self.log.append(line)
            line = self.stream.readline()
        return self.get_exit_code()

    def get_log(self):
        return self.log

    def get_exit_code(self):
        return None


class SSHExecutor(Executor):
    pass


class LocalExecutor(Executor):
    def setup_stream(self, script):
        fd, tmp_script_filename = tempfile.mkstemp()
        os.close(fd)
        f = open(tmp_script_filename, 'w')
        f.write(script)
        f.close()
        os.chmod(tmp_script_filename, 0o744)
        p = subprocess.Popen(
            tmp_script_filename, shell=True, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
        self.process = p
        self.stream = p.stdout

    def get_exit_code(self):
        self.process.wait()
        return self.process.returncode
