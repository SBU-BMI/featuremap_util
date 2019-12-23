#!/usr/bin/env bash
# Run for each slide subfolder

PROGNAME=$(basename "$0")
count_array=("20181218"
  "20180504"
  "20181016"
  "20190307"
  "20180622"
  "20181003"
  "20181015"
  "20181203"
  "20190411"
  "20181018"
  "20181127"
  "20181108"
  "20180627"
  "TAS71"
  "20181005"
  "20180628"
  "20180814"
  "20180822"
  "20181001"
  "20180608"
  "20190409"
  "20190131"
  "20180724"
  "20181029"
  "20190301"
  "20180925"
  "TAS94"
  "20181011"
  "20180917"
  "20180731"
  "20180710")

dir="/path/to/images"

for i in "${count_array[@]}"; do
  :
  echo "$i"
  docker stop class-dev
  docker rm class-dev
  # RUN
  docker run --name "maputil-dev" -v "$(pwd)/input/$i":/data/input -v "$(pwd)/output":/data/output -v "$dir/$i":/data/wsi -itd "maputil_dev"
  # EXECUTE
  docker exec "maputil-dev" pred_to_map "something" tif
done

echo "$PROGNAME done."
