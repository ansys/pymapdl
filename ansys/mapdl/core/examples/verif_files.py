"""loads a list of verification files
"""
import glob
import inspect
import os

module_path = os.path.dirname(inspect.getfile(inspect.currentframe()))


def load_vmfiles():
    """load vmfiles and store their filenames"""
    vmfiles = {}
    verif_path = os.path.join(module_path, "verif")
    for filename in glob.glob(os.path.join(verif_path, "*dat")):
        basename = os.path.basename(filename)
        vmname = os.path.splitext(basename)[0]
        vmfiles[vmname] = filename

    return vmfiles


# save the module from failing if the verification files are unavailable.
try:
    vmfiles = load_vmfiles()
except:
    vmfiles = []
