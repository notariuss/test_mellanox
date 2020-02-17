#!/usr/bin/env python3
import subprocess
import time
import os

import psutil

partitions = psutil.disk_partitions()

X = 600 # free
Z = 2 # count
Y = 300 # file size
Data = "/dev/zero"

t1 = time.time()
for p in partitions:
    if X * 1024 * 1024 <= psutil.disk_usage(p.mountpoint).free:
        for i in range(1, Z + 1):
            file = os.path.join(p.mountpoint, f"file{i}")
            bashCommand = f"dd if={Data} of={file} count={Y * 1024} bs=1024"
            FNULL = open(os.devnull, 'w')
            process = subprocess.Popen(bashCommand.split(), stdout=FNULL, stderr=FNULL)
            output, error = process.communicate()
            break
else:
    print("There no suitable partition.")
print("Seconds spent: {}".format(time.time() - t1))