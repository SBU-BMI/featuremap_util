# Modified from quip_lymphocyte/get_grayscale_heatmap.py
import os
import sys
# import imageio
import numpy as np
from calc.featuremap import *
from pyrad_to_map import *

from calc.get_labeled_im import *
from calc.get_tissue_map import get_tissue_map
from calc.get_wbr_im import get_wbr_im
from calc.featuremap import write_map_from_matrix


base = os.path.basename(__file__)
print("python script", base)
print("len", len(sys.argv))


if len(sys.argv) != 8:
    print('\nUsage:\n    python3.7 ' + base + ' svs_name width height pred_file color_file output_dir exec_id')
    sys.exit(1)

svs_name = sys.argv[1]
width = int(sys.argv[2])
height = int(sys.argv[3])
pred_file = sys.argv[4]
color_file = sys.argv[5]
output_dir = sys.argv[6]
exec_id = sys.argv[7]

pred_data = []
if has_header(pred_file):
    print(pred_file, exec_id, width, height)
    classification(pred_file, exec_id, width, height)
else:
    pred_data = np.loadtxt(pred_file).astype(np.float32)
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
    write_map_from_matrix(im, [width, height], filename, exec_id, False)
