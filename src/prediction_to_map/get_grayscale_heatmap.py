import os
import sys
# import imageio
import numpy as np
# from datetime import datetime

from get_labeled_im import *
from get_tissue_map import *
from get_wbr_im import *
from fmap.featuremap import *

# startTime = datetime.now()

# Check num args
base = os.path.basename(__file__)
if len(sys.argv) != 7:
    print('\nUsage:\n    python ' + base + ' svs_name width height pred_file color_file output_dir')
    sys.exit(1)

# Get arguments
svs_name = sys.argv[1]
width = int(sys.argv[2])
height = int(sys.argv[3])
pred_file = sys.argv[4]
color_file = sys.argv[5]
output_dir = sys.argv[6]

# Get data from files
pred, necr, patch_size = get_labeled_im(pred_file)
whiteness, blackness, redness = get_wbr_im(color_file)

# Initialize m x n x c matrix
im = np.zeros((pred.shape[0], pred.shape[1], 3), dtype=np.uint8)

# Populate matrix
im[:, :, 0] = 255 * pred * (blackness > 30).astype(np.uint8) * (redness < 0.15).astype(np.uint8)  # Red channel
im[:, :, 1] = 255 * necr  # Green channel
im[:, :, 2] = 255 * get_tissue_map(whiteness)  # Blue channel

im = np.swapaxes(im, 0, 1)  # Transpose

filename = output_dir + '/{}.png'.format(svs_name)
# imageio.imwrite(filename, im)
# print(base + ':', datetime.now() - startTime)
write(im, [width, height], filename)
