# import argparse
import threading
from spoonybard.core import ssh


def main():
    # parser = argparse.ArgumentParser(
    #    description='Run the spoonybard server.')
    # parser.add_argument('-c', help='Configuration file path')
    # args = parser.parse_args()
    # start ssh server
    ssh_server = ssh.SSHServer(("localhost", 8022))
    ssh_server_thread = threading.Thread(target=ssh_server.serve_forever)
    ssh_server_thread.start()
