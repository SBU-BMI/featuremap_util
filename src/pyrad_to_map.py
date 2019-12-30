#!/usr/bin/env python
import json
import os
import sys

import numpy as np
import pandas as pd
from sklearn import preprocessing


def prRed(skk): print("\033[91m {}\033[00m".format(skk))


def normalize(df, column_names_to_normalize):
    try:
        # Convert non-numeric value 'None' to zero
        df.replace(r'None', '0', regex=True, inplace=True)
        df.apply(pd.to_numeric)
        x = df[column_names_to_normalize].values  # returns a numpy array
        # Normalize 0 to 255
        min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 255))
        x_scaled = min_max_scaler.fit_transform(x)
        df_temp = pd.DataFrame(x_scaled, columns=column_names_to_normalize, index=df.index)
        # Merge back into original dataframe
        df[column_names_to_normalize] = df_temp
    except ValueError as ex:
        # Catch outlier non-numeric values and exit
        prRed('FOUND NON-NUMERIC VALUES IN DATA COLUMNS')
        prRed(ex)
        exit(1)
    return df


def norm_ij_1(df):
    # Set i,j
    df['i'] = df['patch_x'] / df['patch_width']  # divide each x in the series by patch width
    df['j'] = df['patch_y'] / df['patch_height']

    # Round up to whole numbers
    df.i = np.ceil(df.i).astype(int)
    df.j = np.ceil(df.j).astype(int)

    return df


def get_meta_from_file(df, exec_id, exec_by):
    # Create JSON metadata
    imw = df['image_width'].iloc[0]  # at location 0, first row
    imh = df['image_height'].iloc[0]
    pw = df['patch_width'].iloc[0]
    ph = df['patch_height'].iloc[0]

    obj = {"img_width": str(imw),
           "img_height": str(imh),
           "patch_w": str(pw),
           "patch_h": str(ph),
           "png_w": str(np.ceil(imw / pw).astype(int)),
           "png_h": str(np.ceil(imh / ph).astype(int)),
           "exec_id": str(exec_id),
           "executed_by": str(exec_by)}

    return obj


# This function is for utilizing ALL columns in spreadsheet:
# def get_columns(df):
#     # Set i,j
#     df['i'] = df['patch_x'] / df['patch_width']  # divide each x in the series by patch width
#     df['j'] = df['patch_y'] / df['patch_height']
#
#     # Round up to whole numbers
#     df.i = np.ceil(df.i).astype(int)
#     df.j = np.ceil(df.j).astype(int)
#
#     to_be_removed = ['case_id', 'image_width', 'image_height', 'mpp_x', 'mpp_y', 'patch_x', 'patch_y', 'patch_width',
#                      'patch_height', 'datetime', 'i', 'j']
#     column_names_to_normalize = []
#     cols = list(df.columns)
#     column_names = ['i', 'j']
#     for c in cols:
#         if c not in to_be_removed:
#             column_names.append(c)  # column that we want
#             if c not in 'i' and c not in 'j':
#                 column_names_to_normalize.append(c)
#     return column_names, column_names_to_normalize


def process(input, output, exec_id, exec_by):
    # Do for all files in directory:
    for filename in os.listdir(input):
        if filename.endswith(".csv"):
            print("File:", filename)
            fin = os.path.join(input, filename)
            try:
                df = pd.read_csv(fin)
                var = df['image_width'].iloc[0]  # catch stuff that isn't pyradiomics
            except Exception as ex:
                prRed('image_width column not found')
                continue
            meta = get_meta_from_file(df, exec_id, exec_by)

            # For utilizing all columns:
            # cols, column_names_to_normalize = get_columns(df)

            # For the chosen 9 columns:
            cols = ['i', 'j',
                    'fg_firstorder_Mean', 'bg_firstorder_Mean', 'fg_firstorder_RootMeanSquared',
                    'bg_firstorder_RootMeanSquared', 'fg_glcm_Autocorrelation', 'bg_glcm_Autocorrelation',
                    'nuclei_ratio', 'nuclei_average_area', 'nuclei_average_perimeter']

            # For an experimental version of pyradiomics spreadsheet:
            # cols = ['i', 'j', 'patch_area_micro', 'nuclei_area_micro', 'nuclei_ratio', 'nuclei_average_area',
            #         'nuclei_average_perimeter']

            column_names_to_normalize = cols[2:]
            column_names = ",".join(cols)
            df = norm_ij_1(df)

            # Write first row JSON
            fout = os.path.join(output, filename)
            with open(fout, 'w') as f:
                f.write(json.dumps(meta) + '\n')
                f.write(column_names + '\n')

            df = df[cols]  # only the columns that we need
            df = normalize(df, column_names_to_normalize)
            df = df.sort_values(['i', 'j'], ascending=[1, 1])

            with open(fout, 'a') as f:
                df.to_csv(f, mode='a', header=False, index=False)


if __name__ == "__main__":
    # python3.7 pyrad_to_map.py ../input ../output testEXEC someone@somewhere.com
    base = os.path.basename(__file__)
    if len(sys.argv) != 5:
        prRed('\nUsage:\n    python ' + base + ' input_dir output_dir exec_id exec_by')
        exit(1)

    input = sys.argv[1]  # input
    output = sys.argv[2]  # output
    exec_id = sys.argv[3]  # execution id
    exec_by = sys.argv[4]  # executed by
    process(input, output, exec_id, exec_by)
    exit(0)
