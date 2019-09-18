import numpy as np
from get_labeled_im import *
from get_whiteness_im import *
from get_tissue_map import *
import sys
from scipy import misc
import imageio

svs_name = sys.argv[1]
width = int(sys.argv[2])
height = int(sys.argv[3])
pred_file = sys.argv[4]
color_file = sys.argv[5]

pred, necr, patch_size = get_labeled_im(pred_file)
whiteness, blackness, redness = get_whiteness_im(color_file)

im = np.zeros((pred.shape[0], pred.shape[1], 3), dtype=np.uint8)
im[:, :, 0] = 255 * pred * (blackness>30).astype(np.uint8) * (redness<0.15).astype(np.uint8)
im[:, :, 1] = 255 * necr
im[:, :, 2] = 255 * get_tissue_map(whiteness)

im = np.swapaxes(im, 0, 1)
# misc.imsave('grayscale_heatmaps/{}.png'.format(svs_name), im)
imageio.imwrite('grayscale_heatmaps/{}.png'.format(svs_name), im)