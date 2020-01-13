import numpy as np


# Extract data from color file
def get_wbr_im(color_file):
    data = np.loadtxt(color_file).astype(np.float32)
    # 5 columns in color file
    x = data[:, 0]  # x
    y = data[:, 1]  # y
    w = data[:, 2]  # white
    b = data[:, 3]  # black
    r = data[:, 4]  # red

    calc_width = x.min() + x.max()
    step = calc_width / len(np.unique(x))

    x = np.round((x + step / 2.0) / step)
    y = np.round((y + step / 2.0) / step)

    maxx = int(x.max())
    maxy = int(y.max())
    # Initialize matrices
    whiteness = np.zeros((maxx, maxy), dtype=np.uint8)
    blackness = np.zeros((maxx, maxy), dtype=np.uint8)
    redness = np.zeros((maxx, maxy), dtype=np.uint8)

    # Populate matrices
    for iter in range(len(x)):
        whiteness[int(x[iter] - 1), int(y[iter] - 1)] = w[iter]
        blackness[int(x[iter] - 1), int(y[iter] - 1)] = b[iter]
        redness[int(x[iter] - 1), int(y[iter] - 1)] = r[iter]

    return whiteness, blackness, redness, maxx, maxy
