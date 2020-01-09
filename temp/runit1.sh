#!/usr/bin/env bash
# IF YOU NEED TO RUN SEVERAL FOLDERS.
# For each input folder, execute prediction-to-map.

IMAGE_NAME="quip_distro_maputil"
CONTAINER_NAME="quip-maputil"

folder_array=(
  "folder1"
  "folder2"
  "folder3"
  "folder4")

dir="/path/to/top/input/folder"
exec_id="someexecid"
peep="some.one@stonybrook.edu"
output="/your/featuremap_util/output"

for i in "${folder_array[@]}"; do
  :
  # REMOVE OLD CONTAINER
  docker stop $CONTAINER_NAME; docker rm $CONTAINER_NAME
  echo "$i"
  # MAKE SUBDIR
  mkdir "$output/$i"
  # RUN
  docker run --name "$CONTAINER_NAME" -v "$dir/$i/output/heatmap_txt":/data/input -v "$output/$i":"/data/output" -v "/path/to/wsi/folder":/data/wsi -itd "$IMAGE_NAME"
  # EXECUTE
  docker exec "$CONTAINER_NAME" pred_to_map "$exec_id" "$peep" tif
  exit 0 # Run once to see if OK!!
done

echo "$PROGNAME done."
