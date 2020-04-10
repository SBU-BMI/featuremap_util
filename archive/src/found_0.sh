if [[ $found -eq 0 ]]; then
  something="don't do anything"

  for files in $HEAT_LOC/prediction-*; do

    # From the prediction- file name, deduce the matching slide name (minus the extension)
    SVS=$(echo ${files} | awk -F'/' '{print $NF}' | awk -F'prediction-' '{print $2}')

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
    # python "$(pwd)/prediction_to_map.py" ${SVS} ${WIDTH} ${HEIGHT} ${files} "dummy" ${output_dir} ${executionid} ${executedby}
    python "$(pwd)/prediction_to_map.py" $SVS_FILE $WIDTH $HEIGHT $files "dummy" $output_dir $executionid $executedby

  done
fi
