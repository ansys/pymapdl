"""Validate the PNG images in the build/latex/ directory

Removes invalid PNGs (probably GIF)

"""

from glob import glob
import os
from pathlib import Path

from PIL import Image

this_path = os.path.dirname(os.path.abspath(__file__))
check_path = os.path.join(this_path, "_build", "latex")
if not os.path.isdir(check_path):
    raise FileNotFoundError(f"Invalid path {check_path}")

for filename in glob(os.path.join(check_path, "*.png")):
    im = Image.open(filename)
    im.save(filename, format="png")
    im.close()  # reload is necessary in my case

print("Replacing animated GIFs for static PNGs in Latex")
latex_file = glob(os.path.join(check_path, "*.tex"))[0]

files_to_replace = []

for filename in glob(os.path.join(check_path, "*.gif")):
    im = Image.open(filename)

    new_file_name = filename.split(".")[0] + ".png"
    files_to_replace.append([filename, new_file_name])

    im.save(new_file_name, format="png")
    im.close()  # reload is necessary in my case
    print(f"Replaced {filename} with {new_file_name}")

# Replace in tex file
with open(latex_file, "r") as fid:
    content = fid.read()

for old_file_name, new_file_name in files_to_replace:
    old_file_name = os.path.basename(old_file_name)
    new_file_name = os.path.basename(new_file_name)

    name = Path(new_file_name).stem  # no extension

    old_file_pattern = "{{" + f"{name}" + "}.gif}"  # {{manifold}.gif}
    new_file_pattern = "{{" + f"{name}" + "}.png}"  # {{manifold}.gif}

    content = content.replace(old_file_pattern, new_file_pattern)

with open(latex_file, "w") as fid:
    fid.write(content)
