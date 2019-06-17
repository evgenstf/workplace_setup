#!/bin/bash

now_dir=`echo ${PWD##*/}`

if [ "$now_dir" != 'build' ];
then
  mkdir build
  cd build
  echo "maked new dir build"
fi
cmake ..
make tests -j20
