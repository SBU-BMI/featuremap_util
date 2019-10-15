import numpy as np


# Extract data from prediction file
def get_labeled_im(pred_f):
    pred_data = np.loadtxt(pred_f).astype(np.float32)
    # 4 columns in prediction file
    x = pred_data[:, 0]  # x
    y = pred_data[:, 1]  # y
    l = pred_data[:, 2]  # lymph
    n = pred_data[:, 3]  # necrosis

    calc_width = x.min() + x.max()
    patch_size = calc_width / len(np.unique(x))

    x = np.round((x + patch_size / 2.0) / patch_size)
    y = np.round((y + patch_size / 2.0) / patch_size)

    maxx = int(x.max())
    maxy = int(y.max())
    # Initialize matrices
    iml = np.zeros((maxx, maxy), dtype=np.float32)  # img matrix lymph
    imn = np.zeros((maxx, maxy), dtype=np.float32)  # img matrix necrosis

    # Populate matrices
    for iter in range(len(x)):
        iml[int(x[iter] - 1), int(y[iter] - 1)] = l[iter]
        imn[int(x[iter] - 1), int(y[iter] - 1)] = n[iter]

    return iml, imn
