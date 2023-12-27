#/bin/bash
# Script to create the venv, and install the dependencies

mkdir -p /home/mapdl/pymapdl 


if [ -f /home/mapdl/pymapdl/.venv/bin/activate ] then
    echo "It seems a venv exists already. Stopping here"
else
    echo "Creating virtual environment..."
    python3.10 -m venv /home/mapdl/pymapdl/.venv
    source /home/mapdl/pymapdl/.venv/bin/activate

    echo "Installing PyMAPDL package and dependencies for development"
    pip install -e '.[tests,doc]'

    echo "Installing pre-commit..."
    pip install pre-commit
    pre-commit install
    echo "Done! Enjoy PyMAPDL!"
fi