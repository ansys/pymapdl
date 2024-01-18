#/bin/bash
# Script to create the venv, and install the dependencies
echo "Starting local development container"

echo "Activating virtual environment..."

ln -s /home/mapdl/.venv /home/mapdl/pymapdl/.venv_pymapdl && echo "Linking venv original dir"
source /home/mapdl/.venv/bin/activate

echo "Installing PyMAPDL package and dependencies for development"
# let's first update everything
cd /home/mapdl/pymapdl/
git fetch && git pull

# Overwriting example
cp /home/mapdl/pymapdl/.devcontainer/codespaces-notebook/example-bracket_static.ipynb /home/mapdl/

# Installation should be fast because the image is built with the dependencies installed.
pip install -e .

echo "Setting pre-commit..."
pre-commit install --install-hooks

cd /home/mapdl/

# launching xvfb
echo "Setting xvfb"
/usr/bin/Xvfb :0 -screen 0 1024x768x24 &
export DISPLAY=":0"
echo 'export DISPLAY=":0"' >> ~/.bashrc


echo "Done! Enjoy PyMAPDL!"