import io
import tempfile
import os
import paramiko
import subprocess


class Executor(object):
    def __init__(self, config={}):
        self.config = config
        self.log = []

    def open(self):
        """Opens any connections needed"""
        pass

    def close(self):
        """Closes any open connections"""
        pass

    def run_script(self, script):
        pass

    def run(self, script):
        self.run_script(script)
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
    def open(self):
        """Open the ssh connection"""
        key_str = io.StringIO(self.config['key'])
        pkey = paramiko.RSAKey.from_private_key(key_str)
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())
        self.client.connect(
            self.config['hostname'], username=self.config['username'],
            pkey=pkey, timeout=60, banner_timeout=60)
        self.transport = self.client.get_transport()
        self.transport.set_keepalive(60)
        self.script_filename = self.get_tmp_script_filename()

    def close(self):
        """Close the ssh connection"""
        ftp = self.client.open_sftp()
        ftp.remove(self.script_filename)
        ftp.close()
        self.client.close()

    def upload_file(self, filename, content, mode=None):
        ftp = self.client.open_sftp()
        file = ftp.file(filename, 'w', -1)
        file.write(content)
        file.flush()
        if mode:
            ftp.chmod(self.script_filename, 0o744)
        ftp.close()

    def get_tmp_script_filename(self):
        channel = self.transport.open_session()
        channel.get_pty()
        out = channel.makefile()
        channel.exec_command('mktemp')
        tmpfilename = out.readline().strip()
        channel.recv_exit_status()
        channel.close()
        return tmpfilename

    def run_script(self, script):
        # upload the script
        self.upload_file(self.script_filename, script, 0o755)

        # run the script in a pty so we get all output in order
        channel = self.transport.open_session()
        channel.get_pty()
        out = channel.makefile()
        channel.exec_command(self.script_filename)

        self.channel = channel
        self.stream = out

    def get_exit_code(self):
        exit_code = self.channel.recv_exit_status()
        self.channel.close()
        return exit_code


class LocalExecutor(Executor):
    def run_script(self, script):
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
