import psutil

partitions = psutil.disk_partitions()

X = 600 # free
Z = 2 # count
Y = 300 # file size
Data = "./data"

for p in partitions:
    if X <= psutil.disk_usage(p.mountpoint).total / 1024 / 1024:
        for i in range(0, Z):
            with open(f"{p.mountpoint}/file{i}", "wb") as f:
                f.seek(int((Y / 1024) * 1024 * 1024 * 1024))
                f.write(b'0')
                bashCommand = f"dd if={Data} of={p.mountpoint}/file{i}"
                import subprocess
                import time
                t1 = time.time()
                process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()
                print("{}/file{} seconds spent: {}".format(p.mountpoint, i, time.time() - t1))
