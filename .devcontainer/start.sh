#/bin/bash
# Script to create the venv, and install the dependencies

mkdir -p /home/mapdl/pymapdl 

echo "Creating virtual environment..."

python3.10 -m venv /home/mapdl/pymapdl/.venv
source /home/mapdl/pymapdl/.venv/bin/activate
cd /home/mapdl/pymapdl

echo "Installing PyMAPDL package and dependencies for development"
pip install -e '.[tests,doc]

echo "Done! Enjoy PyMAPDL!"
