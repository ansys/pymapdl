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
esac

# build and install
"${PYBIN}/pip" install -r /io/requirements_build.txt
"${PYBIN}/pip" wheel /io/ -w /io/wheelhouse/
"${PYBIN}/python" -m pip install $package_name -f /io/wheelhouse/ --no-index

# test
"${PYBIN}/pip" install -r /io/requirements_test.txt
"${PYBIN}/pip" install pytest-azurepipelines
cd /io/tests
"${PYBIN}/pytest"

# move and rename wheels to dist
ls /io/wheelhouse
mkdir -p /io/dist
rm -rf /io/dist/*
cd /io/
find wheelhouse -name $package_name-* | while read FILE ; do
  NEWFILE="$(echo $FILE |sed -e 's/\linux/manylinux1/')"
  NEWFILE="$(echo $NEWFILE |sed -e 's/\wheelhouse/dist/')"
  cp $FILE $NEWFILE
done
ls /io/dist
