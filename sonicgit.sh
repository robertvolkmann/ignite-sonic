#!/bin/bash
source ./build.cfg

if [ -d "${BUILD_DIR}" ];then
   echo "directory sonic-buildimage already exists, aborting git"
   exit 1
fi

git clone --branch ${BRANCH} --single-branch https://github.com/robertvolkmann/sonic-buildimage.git "${BUILD_DIR}"

git submodule update --init --recursive

echo "${BUILD_DIR}"
git status | grep branch
