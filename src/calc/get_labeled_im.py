import numpy as np


# Extract data from prediction file
def get_labeled_im(pred_f, maxx, maxy):
    '''
    Using the x.max and y.max from the color- file to populate the til and nec matrices.
    It is more reliable than doing so by using the prediction- file
    because there are some tiles that got skipped when doing the prediction.
    :param pred_f:
    :param maxx:
    :param maxy:
    :return:
    '''
    pred_data = np.loadtxt(pred_f).astype(np.float32)
    # 4 columns in prediction file
    x = pred_data[:, 0]  # x
    y = pred_data[:, 1]  # y
    l = pred_data[:, 2]  # lymph
    n = pred_data[:, 3]  # necrosis

    patch_size = (x.min() + x.max()) / len(np.unique(x))

    x = np.round((x + patch_size / 2.0) / patch_size)
    y = np.round((y + patch_size / 2.0) / patch_size)

    # Initialize matrices
    iml = np.zeros((maxx, maxy), dtype=np.float32)  # img matrix lymph
    imn = np.zeros((maxx, maxy), dtype=np.float32)  # img matrix necrosis

    # Populate matrices
    for iter in range(len(x)):
        iml[int(x[iter] - 1), int(y[iter] - 1)] = l[iter]
        imn[int(x[iter] - 1), int(y[iter] - 1)] = n[iter]

    return iml, imn, patch_size
