rem Register and upload source
python setup.py sdist upload -r pypi
python setup.py bdist_wheel upload -r pypi

activate python3.5
python setup.py bdist_wheel upload -r pypi

activate python3.6
python setup.py bdist_wheel upload -r pypi

pause