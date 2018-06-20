#!/bin/bash

# script to build manylinux binary wheel using docker
# inspired by/copied from:
# https://github.com/pypa/python-manylinux-demo/blob/master/travis/build-wheels.sh

# current run directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# start docker image and store the id
docker run -d -i quay.io/pypa/manylinux1_x86_64 /bin/bash
CONTAINERID=$(docker ps -q -n 1)

# build source
filename=$(ls $DIR/dist/*.tar.gz)
rm $filename
python $DIR/setup.py -q sdist
tarfile=$(ls $DIR/dist/*.tar.gz)
tarfile="${tarfile[0]}"
filename=$(basename -- "$tarfile")

# copy to image and untar
docker cp $tarfile $CONTAINERID:/root/
docker exec -it $CONTAINERID rm -rf /root/source  # temp
docker exec -it $CONTAINERID tar -xf /root/$filename -C /root
foldername="${filename%.tar.gz}"
docker exec -it $CONTAINERID mv /root/$foldername/ /root/source

# build wheels
docker exec -it $CONTAINERID yum install libXt -y -q -e 0 # for vtk
docker cp $DIR/docker.sh $CONTAINERID:/root/source/
docker exec -it $CONTAINERID chmod +x /root/source/docker.sh
docker exec -it $CONTAINERID ./root/source/docker.sh

# copy them back here
docker cp $CONTAINERID:/root/source/wheels /tmp/
mv /tmp/wheels/* dist/

echo 'Stopping docker:'
docker stop $CONTAINERID
echo 'Stopped'
