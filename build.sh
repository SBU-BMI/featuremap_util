#!/usr/bin/env bash
# ./build.sh "$(pwd)/input" "$(pwd)/output" "$(pwd)/wsi"

PROGNAME=$(basename "$0")
NORMAL="\\033[0;39m"
RED="\\033[1;31m"

if [[ "$#" -eq "0" ]]; then
  echo "No arguments supplied"
  printf "    ${RED}usage: $PROGNAME /path/to/input/dir /path/to/output/dir /path/to/wsi/dir$1${NORMAL}\n"
  exit 1
fi

IMAGE_NAME="maputil_dev"
CONTAINER_NAME="maputil-dev"

build() {
  docker stop $CONTAINER_NAME; docker rm $CONTAINER_NAME || echo "It's ok. Moving on..."
  docker rmi $IMAGE_NAME || echo "It's ok. Moving on..."
  docker build -t $IMAGE_NAME .
  docker run --name "$CONTAINER_NAME" -v "$1":/data/input -v "$2":/data/output -v "$3":/data/wsi -itd "$IMAGE_NAME"
}

build $1 $2 $3
