#/bin/bash
# Script to create the venv, and install the dependencies

if [ -f $VEN ]; then
    echo "It seems a venv exists already. Stopping here"

else
    echo "Creating virtual environment..."

    echo "Installing PyMAPDL package and dependencies for development"
    pip install -e '.[tests,doc]'

    echo "Installing pre-commit..."
    pre-commit install
    echo "Done! Enjoy PyMAPDL!"

fi