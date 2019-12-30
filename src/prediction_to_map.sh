#!/usr/bin/env bash
# Modified from quip_lymphocyte/get_grayscale_heatmap.sh

PROGNAME=$(basename "$0")
error_exit() {
  echo "${PROGNAME}: ${1:-"Error"}" 1>&2
  echo "Line $2"
  exit 1
}

if [ "$#" -ne 6 ]; then
  # CMD: ./prediction_to_map.sh ../input ../output ../wsi svs 12345 someone@somewhere.com
  echo "Usage: $0 /data/input /data/output /data/wsi svs exec_id exec_by email_addr" >&2
  exit 1
fi

# Locations of unmodified heatmaps
# The filenames of the unmodifed heatmaps should be:
#   prediction-${slide_id}
# For example:
#   prediction-TCGA-XX-XXXX-01Z-00-DX1
HEAT_LOC="$1"
output_dir="$2"
SLIDES="$3"
ext="$4"
exec_id="$5"
exec_by="$6"
found=0

# We get the slides based on what's in this heatmap_txt folder
for files in $HEAT_LOC/color-*; do
  found=1

  # From the color- file name, deduce the matching slide name (minus the extension)
  SVS=$(echo ${files} | awk -F'/' '{print $NF}' | awk -F'color-' '{print $2}')

  # Find the unmodified heatmap
  PRED=$(ls -1 ${HEAT_LOC}/prediction-${SVS}* | grep -v low_res)
  COLOR=${files}

  # Find the slide
  FILE="$(ls -1 ${SLIDES}/${SVS}*.$ext)"
  if [ -f "$FILE" ]; then
    SVS_FILE=$(ls -1 ${SLIDES}/${SVS}*.$ext | head -n 1)
  else
    echo "$FILE does not exist"
    continue
  fi

  # Get width and height
  WIDTH=$(openslide-show-properties ${SVS_FILE} |
    grep "openslide.level\[0\].width" | awk '{print substr($2,2,length($2)-2);}')
  HEIGHT=$(openslide-show-properties ${SVS_FILE} |
    grep "openslide.level\[0\].height" | awk '{print substr($2,2,length($2)-2);}')

  # Generate CSVs and PNGs.
  python "$(pwd)/prediction_to_map.py" ${SVS} ${WIDTH} ${HEIGHT} ${PRED} ${COLOR} ${output_dir} ${exec_id} ${exec_by}
done

if [ $found == 0 ]; then
  error_exit "There are no color files."
fi

exit 0
