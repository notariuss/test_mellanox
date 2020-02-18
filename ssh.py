#!/usr/bin/env python3
import sys
from threading import Thread
import argparse
import paramiko
import uuid
import os


class SSHThread(Thread):
    def __init__(self, host, port, username, secret, command):
        Thread.__init__(self)
        self.exit_code = 0
        self.host = host
        self.port = port
        self.username = username
        self.secret = secret
        self.command = command
    
    def run(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname=self.host, username=self.username, password=self.secret, port=self.port)
        except paramiko.ssh_exception.AuthenticationException:
            print(f"{self.username}@{self.host} incorect password!")
            self.exit_code = 1
            return 1
        except Exception:
            print(f"{self.username}@{self.host} failed to connect!")
            self.exit_code = 1
            return 1
        chan = client.get_transport().open_session()
        chan.exec_command(self.command)
        content_name, errors_name = "." + str(uuid.uuid4()), "." + str(uuid.uuid4())
        content = open(content_name, "wb")
        errors = open(errors_name, "wb")
        while not chan.exit_status_ready():
            if chan.recv_ready():
                data = chan.recv(1024)
                while data:
                    content.write(data)
                    data = chan.recv(1024)

            if chan.recv_stderr_ready():            
                error_buff = chan.recv_stderr(1024)
                while error_buff:
                    errors.write(error_buff)
                    error_buff = chan.recv_stderr(1024)
        exit_status = chan.recv_exit_status()
        content.close()
        errors.close()
        content = open(content_name, "rb")
        errors = open(errors_name, "rb")
        print(f"{self.username}@{self.host} cmd exit status {exit_status}; cmd result:")
        print(content.read().decode() + errors.read().decode())
        content.close()
        errors.close()
        os.remove(content_name)
        os.remove(errors_name)


def main(hosts, command):
    command = " ".join(command)
    threads = []
    exit_code = 0
    for host, port, username, secret in hosts:
        thread = SSHThread(host, port, username, secret, command)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
        if thread.exit_code == 1:
            exit_code = 1
    exit(exit_code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", nargs="+")
    parser.add_argument('-host', action="append", nargs=4, required=True)
    args = parser.parse_args()
    main(args.host, args.cmd)
