#!/usr/bin/env bash
# Modified from quip_lymphocyte/download_heatmap/get_grayscale_heatmaps/get_grayscale_heatmap.sh

PROGNAME=$(basename "$0")
error_exit() {
  echo "${PROGNAME}: ${1:-"Error"}" 1>&2
  echo "Line $2"
  exit 1
}

if [ "$#" -ne 3 ]; then
  # CMD: ./prediction_to_map.sh ../input ../output ../wsi svs testEXEC someone@somewhere.com
  echo "Usage: $0 svs executionid executedby" >&2
  exit 1
fi

# Locations of unmodified heatmaps
# The filenames of the unmodifed heatmaps should be:
#   prediction-${slide_id}
# For example:
#   prediction-TCGA-XX-XXXX-01Z-00-DX1
HEAT_LOC="/data/input"
output_dir="/data/output"
SLIDES="/data/wsi"

ext="$1"
executionid="$2"
executedby="$3"
found=0

echo "args: $1 $2 $3"

color_files="$HEAT_LOC/color-*"
for f in $color_files; do

  ## Check if the glob gets expanded to existing files.
  ## If not, f here will be exactly the pattern above
  ## and the exists test will evaluate to false.
  [ -e "$f" ] && found=1 || echo "There are no color files."

  ## This is all we needed to know, so we can break after the first iteration
  break
done

if [[ $found -eq 1 ]]; then

  # We get the slides based on what's in this heatmap_txt folder
  for files in $HEAT_LOC/color-*; do

    # From the color- file name, deduce the matching slide name (minus the extension)
    SVS=$(echo ${files} | awk -F'/' '{print $NF}' | awk -F'color-' '{print $2}')

    # Find the unmodified heatmap
    PRED=$(ls -1 ${HEAT_LOC}/prediction-${SVS}* | grep -v low_res)
    COLOR=${files}

    # Find the slide
    FILE="$(ls -1 ${SLIDES}/${SVS}*.$ext)"
    if [ -f "$FILE" ]; then
      SVS_FILE=$(ls -1 ${SLIDES}/${SVS}*.$ext | head -n 1)
    fi

    if [ -z "$SVS_FILE" ]; then
      echo "Could not find slide."
      continue
    fi

    # Get width and height
    WIDTH=$(openslide-show-properties ${SVS_FILE} |
      grep "openslide.level\[0\].width" | awk '{print substr($2,2,length($2)-2);}')
    HEIGHT=$(openslide-show-properties ${SVS_FILE} |
      grep "openslide.level\[0\].height" | awk '{print substr($2,2,length($2)-2);}')

    # Generate CSVs and PNGs.
    python "$(pwd)/prediction_to_map.py" ${SVS} ${WIDTH} ${HEIGHT} ${PRED} ${COLOR} ${output_dir} ${executionid} ${executedby}
  done
fi

exit 0
