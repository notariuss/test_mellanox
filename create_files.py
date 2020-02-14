import psutil

partitions = psutil.disk_partitions()

X = 600 # free
Z = 2 # count
Y = 300 # file size

for p in partitions:
    if X <= p.mountpoint, psutil.disk_usage(p.mountpoint).total / 1024 / 1024:
        for i in range(0, Z):
            with open(f"file{i}", "wb") as f:
                f.seek(int(300 / 1024) * 1024 * 1024 * 1024)
                f.write('0')