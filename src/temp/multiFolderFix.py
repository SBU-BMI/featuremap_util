import sys
import os


def makeFolders(filepath):
    '''
    1) Figure out which slides we're going to need
    2) Read in that list and make subfolders
    '''
    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

    dir = ''
    with open(filepath) as fp:
        for line in fp:
            line = line.rstrip()
            x = line.split("/")
            if dir == x[5]:
                print("find . -name " + "prediction-" + x[6].replace(".tif", "") + " -exec mv -- \"{}\" ./" + x[
                    5] + "/ \;")
            else:
                dir = x[5]
                print("mkdir " + dir)
                print("find . -name " + "prediction-" + x[6].replace(".tif", "") + " -exec mv -- \"{}\" ./" + x[
                    5] + "/ \;")


# makeFolders('found_paths.out')


def copyFiles(filename, dst_folder):
    '''
    Problem. Output files are in different folders, all with the same name.
    Solution. Copy and rename.
    1) find [src_folder] -name *.csv > ~/results.in
    2) Run this > results.out (results.sh)
    '''

    if not os.path.isfile(filename):
        print("File path {} does not exist. Exiting...".format(filename))
        sys.exit()

    with open(filename) as fp:
        for line in fp:
            line = line.rstrip()
            arr = line.split("/")
            folder = arr[len(arr) - 2]  # folder name is unique name
            old_name = arr[len(arr) - 1]  # old name
            new_name = str(folder) + ".csv"
            print("sudo cp " + line + " " + dst_folder + "/" + new_name)
    print("find " + dst_folder + " -type f | wc -l")


# copyFiles('results.in', '/path/to/somewhere')
