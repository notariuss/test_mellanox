import sys
from threading import Thread

import paramiko

class SSHThread(Thread):

    def __init__(self, host, port, username, secret, command):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.username = username
        self.secret = secret
        self.command = command
    
    def run(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.host, username=self.username, password=self.secret, port=self.port)
        stdin, stdout, stderr = client.exec_command(self.command)
        data = stdout.read() + stderr.read()
        client.close()
        print(f"{self.username}@{self.host} cmd result:")
        print(data.decode())
 
 
def main(tasks):
    for host, port, username, secret, command in tasks:
        thread = SSHThread(host, port, username, secret, command)
        thread.start()

if __name__ == "__main__":
    tasks = []
    for task in sys.argv[1:]:
        tasks.append(task.split(":"))
    main(tasks)

#main([["52.148.198.128", 22, "andrii", "JustD01tJustD01t", "sleep 5 && ls /"], ["51.137.215.9", 22, "andrii", "JustD01tJustD01t", "ls /"]])