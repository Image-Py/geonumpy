#!/usr/bin/env bash


pip install shapely
pip install fiona


if which apt-get > /dev/null;
then
    # ubuntu
    sudo apt-get install libgdal1i libgdal1-dev libgdal-dev \
                         libevent-dev \
                         build-essential \
                         python-dev python3-dev
    sudo add-apt-repository ppa:ubuntugis && sudo apt-get update
    sudo apt-get install gdal-bin
    sudo apt-get -y install gcc gcc-c++  # gcc version
    sudo pip install --upgrade setuptools
    sudo pip install gdal
    pip install -e geonumpy
elif which yum > /dev/null;
then
    # centos
    sudo yum -y install gcc gcc-c++
    sudo yum install python-devel python3-devel
    sudo yum install libevent-devel openssl-devel libffi-devel
    pip install -e geonumpy
elif which brew > /dev/null; 
then
    # Mac
    # TODO
    pip install -e geonumpy
fi
