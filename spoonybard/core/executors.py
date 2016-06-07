import io
import tempfile
import os
import paramiko
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
    def setup_stream(self, script):
        # connect using the key from the configuration
        key_str = io.StringIO(self.config['key'])
        pkey = paramiko.RSAKey.from_private_key(key_str)
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())
        self.client.connect(
            self.config['hostname'], username=self.config['username'],
            pkey=pkey, timeout=60, banner_timeout=60)

        # upload the script
        script_filename = subprocess.check_output('mktemp', shell=True).strip()
        ftp = self.client.open_sftp()
        file=ftp.file(script_filename, 'w', -1)
        file.write(script)
        file.flush()
        ftp.chmod(script_filename, 0o744)
        ftp.close()

        # run the script in a pty so we get all output in order
        transport = self.client.get_transport()
        transport.set_keepalive(60)
        self.channel = channel = transport.open_session()
        channel.get_pty()
        out = channel.makefile()
        channel.exec_command(script_filename)
        self.stream = out

    def get_exit_code(self):
        exit_code = self.channel.recv_exit_status()
        self.client.close()
        return exit_code


class LocalExecutor(Executor):
    def setup_stream(self, script):
        fd, self.tmp_script_filename = tempfile.mkstemp()
        os.close(fd)
        f = open(self.tmp_script_filename, 'w')
        f.write(script)
        f.close()
        os.chmod(self.tmp_script_filename, 0o744)
        p = subprocess.Popen(
            self.tmp_script_filename, shell=True, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
        self.process = p
        self.stream = p.stdout

    def get_exit_code(self):
        self.process.wait()
        os.unlink(self.tmp_script_filename)
        return self.process.returncode
