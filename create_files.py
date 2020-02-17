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

for p in partitions:
<<<<<<< HEAD
    if X <= psutil.disk_usage(p.mountpoint).free / 1024 / 1024:
        for i in range(1, Z + 1):
            file = os.path.join(p.mountpoint, f"file{i}")
            with open(file, "wb") as f:
                bashCommand = f"dd if={Data} of={file} count={Y * 1024} bs=1024"
=======
    if X <= psutil.disk_usage(p.mountpoint).total / 1024 / 1024:
        for i in range(0, Z):
            with open(f"{p.mountpoint}/file{i}", "wb") as f:
                f.seek(int((Y / 1024) * 1024 * 1024 * 1024))
                f.write(b'0')
                bashCommand = f"dd if={Data} of={p.mountpoint}/file{i}"
                import subprocess
                import time
>>>>>>> 760303475a4c15c939855ac4ed96c01c9b589674
                t1 = time.time()
                FNULL = open(os.devnull, 'w')
                process = subprocess.Popen(bashCommand.split(), stdout=FNULL, stderr=FNULL)
                output, error = process.communicate()
<<<<<<< HEAD
                print("{} seconds spent: {}".format(file, time.time() - t1))
=======
                print("{}/file{} seconds spent: {}".format(p.mountpoint, i, time.time() - t1))
>>>>>>> 760303475a4c15c939855ac4ed96c01c9b589674
