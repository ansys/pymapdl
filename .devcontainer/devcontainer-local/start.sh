#!/bin/bash
# Script to create the venv, and install the dependencies
echo "Starting local development container"

echo "Activating virtual environment..."

ln -s /home/mapdl/.venv /home/mapdl/pymapdl/.venv_pymapdl && echo "Linking venv original dir"
source ./.venv_pymapdl/bin/activate

echo "Installing PyMAPDL package and dependencies for development"
# let's first update everything
git fetch && git pull

# Installation should be fast because the image is built with the dependencies installed.
pip install -e '.[tests]'

echo "Setting pre-commit..."
pre-commit install --install-hooks

echo "Done! Enjoy PyMAPDL!"