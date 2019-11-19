#!/usr/bin/env bash
# Modified from quip_lymphocyte/get_grayscale_heatmap.sh

PROGNAME=$(basename "$0")
error_exit() {
  echo "${PROGNAME}: ${1:-"Error"}" 1>&2
  echo "Line $2"
  exit 1
}

if [ "$#" -ne 5 ]; then
  # CMD: ./prediction_to_map.sh ../input ../output ../wsi svs 12345
  echo "Usage: $0 /data/input /data/output /data/wsi svs exec_id" >&2
  exit 1
fi

# Locations of unmodified heatmaps
# The filenames of the unmodifed heatmaps should be:
#   prediction-${slide_id}
# For example:
#   prediction-TCGA-XX-XXXX-01Z-00-DX1
HEAT_LOC="$1"
echo "$HEAT_LOC"

output_dir="$2"
echo "$output_dir"

# This is used for getting wsi width and height
SLIDES="$3"
echo "$SLIDES"

ext="$4"
echo "$ext"

exec_id="$5"
echo "$exec_id"

# We get the slides based on what's in this heatmap_txt folder
for files in ${HEAT_LOC}/color-*; do

  if [ ${files[0]} == "${HEAT_LOC}/color-*" ]; then
    error_exit "There are no color files." $LINENO
  fi

  # From the color- file name, deduce the matching slide name (minus the extension)
  SVS=$(echo ${files} | awk -F'/' '{print $NF}' | awk -F'color-' '{print $2}')

  # Find the unmodified heatmap
  PRED=$(ls -1 ${HEAT_LOC}/prediction-${SVS}* | grep -v low_res)
  COLOR=${files}

  # Find the slide
  if [[ ! $(ls -1 ${SLIDES}/${SVS}*.$ext) ]]; then
    echo "${SLIDES}/${SVS}.XXXX.$ext does not exist."
  else
    SVS_FILE=$(ls -1 ${SLIDES}/${SVS}*.svs | head -n 1)
  fi

  if [[ -z "$SVS_FILE" ]]; then
    echo "Could not find slide."
    continue
  fi

  # Get width and height
  WIDTH=$(openslide-show-properties ${SVS_FILE} |
    grep "openslide.level\[0\].width" | awk '{print substr($2,2,length($2)-2);}')
  HEIGHT=$(openslide-show-properties ${SVS_FILE} |
    grep "openslide.level\[0\].height" | awk '{print substr($2,2,length($2)-2);}')

  # Generate CSVs and PNGs.
  python ./prediction_to_map.py ${SVS} ${WIDTH} ${HEIGHT} ${PRED} ${COLOR} ${output_dir} ${exec_id}
done

exit 0
