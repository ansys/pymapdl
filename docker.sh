#!/bin/bash

# builds python wheels on docker container and tests installation

cd /root/source
mkdir wheels  # final directory
for PYBIN in /opt/python/*/bin; do
    # skip Python 3.4 and 3.7
    if [[ $PYBIN =~ .*37.* ]]
    then
    	continue
    elif [[ $PYBIN =~ .*34.* ]]
    then
	continue
    elif [[ $PYBIN =~ .*27mu.* ]]
    then  # must be ucs4
	PYBIN='/opt/_internal/cpython-2.7.15-ucs4/bin'
    fi

    pyver="$(cut -d'/' -f4 <<<$PYBIN)"
    echo 'Running for' $pyver    
    "${PYBIN}/pip" install numpy -q --no-cache-dir  # required for setup.py
    "${PYBIN}/pip" install cython --upgrade -q --no-cache-dir

    # build wheel
    "${PYBIN}/python" setup.py -q bdist_wheel

    # test wheel
    wheelfile=$(ls /root/source/dist/*.whl)
    auditwheel repair $wheelfile > /dev/null
    rm dist/*

    wheelfile=$(ls /root/source/wheelhouse/*.whl)
    "${PYBIN}/pip" install $wheelfile -q --no-cache-dir
    mv $wheelfile wheels/

    # pytest doesn't seem to work here
    # "${PYBIN}/pip" install pytest -q
    # "${PYBIN}/python" -m pytest

    # test
    "${PYBIN}/python" tests/test_pyansys.py

done
