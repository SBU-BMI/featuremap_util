import csv
import json
import os
import sys

import pandas as pd


def prRed(skk): print("\033[91m {}\033[00m".format(skk))


# Expecting a file in pseudo-csv format (1st row is json)
def get_metadata(filename):
    my_obj = {}
    try:
        # Get first line (metadata)
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            # Each row is a list
            for row in csv_reader:
                # Get the metadata
                if line_count == 0:
                    line_count += 1
                    # If the string ended up getting split by csv
                    if len(row) > 1:
                        # Concatenate list
                        blah = ','.join(row)
                        x = json.loads(blah)
                    else:
                        # Info string is good to go
                        x = json.loads(row[0])
                    my_obj["metadata"] = x
                else:
                    break
        csv_file.close()
    except FileNotFoundError as e:
        print(filename, ":", e.strerror)
        exit(1)
    except:  # catch all exceptions
        print("Unexpected error:", sys.exc_info()[0])
        raise
    # print(my_obj["metadata"])
    return my_obj


# Data contains feature probabilities as RGB values per location
def get_data(filename):
    my_obj = {
        "data": {
            "locations": {
                "i": [],
                "j": []
            },
            "features": {
            }
        }
    }
    df = pd.read_csv(filename, skiprows=[0])  # Skipping metadata row
    n_rows, n_columns = df.shape

    my_obj["data"]["locations"]["i"] = df["i"].tolist()  # Get column data
    my_obj["data"]["locations"]["j"] = df["j"].tolist()

    for x in range(2, n_columns):  # Skipping i, j columns
        # Save feature data to our dictionary
        my_obj["data"]["features"][df.columns[x]] = df[df.columns[x]].tolist()

    return my_obj


def save_file(fName, data1, data2):
    final_obj = {}
    final_obj.update(data1)
    final_obj.update(data2)
    json_str = json.dumps(final_obj)
    try:
        ff = open(fName, "w")  # open file in write mode
        ff.write(json_str)  # write to file
        ff.close()
    except IOError as e:
        errno, strerror = e.args
        print("I/O error({0}): {1}".format(errno, strerror))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    # print('OUT: ' + filename)


if __name__ == '__main__':
    base = os.path.basename(__file__)

    # python3.7 csv_to_json.py ../input ../output
    if len(sys.argv) < 3:
        prRed('\nUsage:\n    python ' + base + ' input_folder output_folder')
        exit(1)

    # Get args
    input_folder = sys.argv[1]  # Folder path
    output_folder = sys.argv[2]
    files_exist = False
    for file in os.listdir(input_folder):
        if file.endswith(".csv"):
            files_exist = True
            f = os.path.join(input_folder, file)
            meta = get_metadata(f)
            data = get_data(f)
            f = f.replace("csv", "json")
            f = f.replace(input_folder, output_folder)
            save_file(f, meta, data)
    if not files_exist:
        prRed("There were no files to process.")
