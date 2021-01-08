import json
import os
import sys


# Write feature map
def write_map_from_matrix(im, dim, filename, executionid, executedby, bgr):
    png_w = im.shape[1]
    png_h = im.shape[0]

    x_arr = []
    y_arr = []
    r_arr = []
    g_arr = []
    b_arr = []

    idx = [0, 1, 2]
    if bgr:
        idx = [2, 1, 0]  # bgr

    for x in range(0, png_w):
        for y in range(0, png_h):
            # Ignore [0,0,0] b/c it will be generated at construction of JSON file to viewable web image
            if not (im[y, x][0] == 0 and im[y, x][1] == 0 and im[y, x][2] == 0):
                x_arr.append(x)
                y_arr.append(y)
                r_arr.append(int(im[y, x][idx[0]]))
                g_arr.append(int(im[y, x][idx[1]]))
                b_arr.append(int(im[y, x][idx[2]]))

    feature = os.getenv('FEAT')
    if 'TIL' in feature:
        foo = "Cancer"
        bar = "Tissue"
    else:
        if 'Cancer' in feature:
            foo = "TIL"
            bar = "Tissue"
            # foo = "null1" # If Classified (3 class, 6 class, etc.) then uncomment null1, null2, and add type (see below).
            # bar = "null2"
        else:
            foo = "null1"
            bar = "null2"

    # TODO: Need a 'type' field to identify the new types; such as: Pyradiomics, Gleason, etc.
    my_obj = {
        "metadata": {
            "img_width": dim[0],
            "img_height": dim[1],
            "png_w": png_w,
            "png_h": png_h,
            "patch_w": 200,
            "patch_h": 200,
            "executionid": executionid,
            "executedby": executedby
            # ,"type": "resnet34_probability" # If classified, uncomment and modify line.
        },
        "data": {
            "locations": {
                "i": x_arr,
                "j": y_arr
            },
            "features": {
                feature: r_arr,
                foo: g_arr,
                bar: b_arr
            }
        }
    }

    json_str = json.dumps(my_obj)
    try:
        ff = open(filename.replace('png', 'json'), "w")  # open file in write mode
        ff.write(json_str)  # write to file
        ff.close()
    except IOError as e:
        errno, strerror = e.args
        print("I/O error({0}): {1}".format(errno, strerror))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
