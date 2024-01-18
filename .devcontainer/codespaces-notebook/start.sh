#/bin/bash
# Script to create the venv, and install the dependencies
echo "Starting local development container"

echo "Activating virtual environment..."

ln -s /home/mapdl/.venv /home/mapdl/pymapdl/.venv_pymapdl && echo "Linking venv original dir"
source ./.venv_pymapdl/bin/activate

echo "Installing PyMAPDL package and dependencies for development"
# let's first update everything
cd /home/mapdl/pymapdl/
git fetch && git pull

# Installation should be fast because the image is built with the dependencies installed.
pip install -e .

echo "Setting pre-commit..."
pre-commit install --install-hooks

cd /home/mapdl/
# cp /home/mapdl/pymapdl/.devco
echo "Done! Enjoy PyMAPDL!"