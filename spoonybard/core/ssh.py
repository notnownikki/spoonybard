import socketserver
import time
import paramiko
import spoonybard
from paramiko.py3compat import decodebytes

# This is all prototype code, no automated tests exist.
# The auth needs sorting out, timeouts configurable etc. etc.
# but it works in manual tests.

# TODO: configure path to host key
host_key = paramiko.RSAKey(filename='test_rsa.key')
command_timeout = 2


class SSHHandler(socketserver.StreamRequestHandler):
    def handle(self, *args, **kwargs):
        t = paramiko.Transport(self.request)
        t.add_server_key(host_key)
        # Note that this actually spawns a new thread to handle the requests.
        # (Actually, paramiko.Transport is a subclass of Thread)
        t.start_server(server=self.server)
        # wait for auth
        chan = t.accept(20)
        time_taken = 0.0
        while getattr(chan, 'spoonybard_command', False) is False:
            time.sleep(0.25)
            time_taken += 0.25
            if time_taken > command_timeout:
                break
        if chan is None:
            print('No channel')
            t.close()
            return
        if getattr(chan, 'spoonybard_command', False):
            cmd = chan.spoonybard_command.split(' ')[0]
            args = ' '.join(chan.spoonybard_command.split(' ')[1:])
            command = spoonybard.engine.plugins.get_command_handler(cmd)
            if command is None:
                chan.send('Sorry, %s is an unknown command.\n' % cmd)
            else:
                if command.parse_args(args):
                    command.execute(chan)
                else:
                    command.help(chan)
        chan.close()
        t.close()


data = b'AAAAB3NzaC1yc2EAAAADAQABAAABAQCewIggKdjP+U2r2vD292Y7dKm0V6+SXF7NCtp' \
       b'fR9y53anv9u7CkgrLvTPBx7YdXBaazqzi5CSrdpo5bD40490n8IqLfsxnIvhqKc4+Y3' \
       b'kPrOcwrQErndafPhFm/IJp+zsgmqBi1fL5lozV7gBllwZcCaor8zeaEQXb0GlbJhsBa' \
       b'XoD3GpFcCIjj5TxxRBf1yvukrtV1Kw0UGNoGh6lGt8FW9+TdiJbaxTuMqz94N0zre2Q' \
       b'zxPd5VWpfDWgFjxi580AZl712sPWLUjaITevlEQfH8YC6tYlTB+XChBdifi3m+cDGN/' \
       b'lVHo/EvX6LxpkKFe/G3oCWfhnH2QwcfPHwcsD'
good_pub_key = paramiko.RSAKey(data=decodebytes(data))


class SSHServer(
        socketserver.ThreadingMixIn, socketserver.TCPServer,
        paramiko.ServerInterface):
    def __init__(self, address):
        socketserver.TCPServer.__init__(self, address, SSHHandler)

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_exec_request(self, channel, exec_command):
        # TODO: permissions check for running commands
        #       i.e. can the auth'd user run this command?
        channel.spoonybard_command = exec_command.decode()
        return True

    def get_allowed_auths(self, username):
        return 'publickey'

    def check_channel_shell_request(self, channel):
        """No interactive sessions"""
        return False

    def check_channel_pty_request(self, channel, term, width, height,
                                  pixelwidth, pixelheight, modes):
        """No interactive sessions"""
        return False

    def check_auth_publickey(self, username, key):
        # TODO: look up public keys from disk based on configured
        #       public key storage path
        if (username == 'nikki') and (key == good_pub_key):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
