"""
This script determines which files have been accessed within an ANSYS
directory and copies them over to a new directory.  This is used for
dockerizing MAPDL

The ``cutoff`` parameter is set from ``time.time()`` right before
running MAPDL with:

/ansys_inc/v211_docker/ansys/bin/mapdl -grpc -smp

or

/ansys_inc/v211_docker/ansys/bin/mapdl -grpc

---

You *must* modify `/etc/fstab` to use strictatime for the mount
containing ANSYS, otherwise the access times won't be updated
correctly.  Be sure to disable this when finished to avoid the extra
IO slowdown.

NOTE:
This misses some files that will be needed by different architectures, like:
/ansys_inc/v211/tp/IntelMKL/2020.0.166/linx64/lib/intel64/libmkl_avx512.so
/ansys_inc/v211/tp/IntelMKL/2020.0.166/linx64/lib/intel64/libmkl_def.so

"""
import shutil
import math
import stat
import time
import os

import numpy as np

source_directory = '/ansys_inc/v211/'

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


cutoff = 1607646816.3588207

total_size = 0
times = []
recent_files = []
for root, dirs, files in os.walk(source_directory, topdown=False):
    for name in files:
        if os.path.isfile(os.path.join(root, name)):
            stats = os.stat(os.path.join(root, name))
            # accesstime = time.ctime(stats[stat.ST_ATIME])
            accesstime = stats[stat.ST_ATIME]
            times.append(accesstime)
            if accesstime > cutoff:
                filepath = os.path.join(root, name)
                # print('%40s    %s' % (name, time.ctime(accesstime)))
                recent_files.append((filepath, name))
                total_size += os.path.getsize(filepath)


times = np.array(times)

# copy files over to a new directory while sorting by file size (for
# cool printouts!)
masked_times = times[times > cutoff]
for i in np.argsort(masked_times):
    accesstime = masked_times[i]
    print(recent_files[i][0])
    # print('%40s    %s' % (recent_files[i][1], time.ctime(accesstime)))
    dest = recent_files[i][0].replace('/v211/', '/v211_docker/')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy(recent_files[i][0], dest)


print(np.sum(times > cutoff), 'out of', len(times))
print(convert_size(total_size))
