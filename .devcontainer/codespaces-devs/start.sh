#/bin/bash
# Script to activate the venv, and install the PyMAPDL

echo "Activating virtual environment..."
source /home/mapdl/pymapdl/.venv/bin/activate

echo "Installing PyMAPDL package and dependencies for development"
# It should be fast because the image is build with the dependencies installed.
pip install -e '.[tests]'

echo "Setting pre-commit..."
pre-commit install

echo "Done! Enjoy PyMAPDL!"