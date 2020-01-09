#!/usr/bin/env bash
# EXAMPLE!!  CREATED FROM MULTIFOLDERFIX.PY
# Make directories for each image subfolder
# Move corresponding input prediction files to the created output subfolder

mkdir somedir
find . -name prediction-lalala -exec mv -- "{}" ./somedir/ \;
# etc...

echo "Done! :)"
