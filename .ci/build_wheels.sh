#!/bin/bash
# builds python wheels on docker container and tests installation

set -e -x

# build based on python version from args
PYTHON_VERSION="$1"
case $PYTHON_VERSION in
2.7)
  PYBIN="/opt/python/cp27-cp27m/bin"
  ;;
3.5)
  PYBIN="/opt/python/cp35-cp35m/bin"
  ;;
3.6)
  PYBIN="/opt/python/cp36-cp36m/bin"
  ;;
3.7)
  PYBIN="/opt/python/cp37-cp37m/bin"
  ;;
3.8)
  PYBIN="/opt/python/cp38-cp38/bin"
  ;;
esac

# build, don't install
cd io
"${PYBIN}/pip" install -r requirements_build.txt
"${PYBIN}/python" setup.py bdist_wheel
auditwheel repair dist/pyansys*.whl
rm -f dist/*
mv wheelhouse/*manylinux1* dist/
