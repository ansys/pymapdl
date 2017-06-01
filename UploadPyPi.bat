rem Register and upload source
rem python setup.py register -r pypi
python setup.py sdist upload -r pypi

rem Python 3.6
"C:\Program Files\Anaconda3\python.exe" setup.py bdist_wheel upload -r pypi

activate python35
python setup.py bdist_wheel upload -r pypi
deactivate python35

rem Python 2
python setup.py bdist_wheel upload -r pypi

pause