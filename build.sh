#!/bin/bash

set -o errexit

source ./build.cfg

pushd "${BUILD_DIR}"

make init
make configure NOBUSTER=1 NOSTRETCH=1 PLATFORM=vs
make NOBUSTER=1 NOSTRETCH=1 SONIC_BUILD_JOBS=2 target/sonic-vs.img.gz

popd

mkdir -p "${DOCKER_CONTEXT}"
mv "${BUILD_DIR}/rootfs.tar" "${DOCKER_CONTEXT}/"

docker build -t robertvolkmann/ignite-sonic:202205 -f Dockerfile "${DOCKER_CONTEXT}"
