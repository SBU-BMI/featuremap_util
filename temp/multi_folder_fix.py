def find_files(filepath):
    '''
    We're creating a shell script (images_to_find.sh) based on input:
    ls -l | awk '{print $9}' > ~/images_to_find.list
    Find/replace when necessary. "prediction-"
    ./images_to_find.sh > images_found.out
    '''
    print("dir=\"/path/to/images\"")
    with open(filepath) as fp:
        for line in fp:
            line = line.rstrip()
            # step 1 (for prediction): Fix images_to_find.list
            # if "color" in line:
            #     print(line.replace("color-", ""))
            # step 2:
            print("find $dir -name \"" + str(line) + "*.tif\"")  # Modify line + '.tif' & identify 'dir'


# find_files('images_to_find.list')  # Start here.


def prt_ln(fname, dir):
    fname = fname.replace(".tif", "")
    # print("find . -name " + "prediction-" + fname + " -exec mv -- \"{}\" ./" + dir + "/ \;")
    # print("find . -name " + "color-" + fname + " -exec mv -- \"{}\" ./" + dir + "/ \;")
    print("mv prediction-" + fname + " ./" + dir)
    print("mv prediction-" + fname + ".low_res ./" + dir)
    print("mv color-" + fname + " ./" + dir)


def makeFolders(filepath):
    '''
    We're creating a script (make_move.sh)
    ** Unless, of course, all image files are in one folder. Then this is not necessary.
    1) Figure out which slides we're going to need
    2) Read in that list and make subfolders
    '''
    dir = ''
    with open(filepath) as fp:
        for line in fp:
            line = line.rstrip()
            x = line.split("/")
            pos_file = len(x) - 1
            pos_dir = len(x) - 2
            if dir == x[pos_dir]:
                # Same subdirectory
                # Given that the input data is local, find input prediction file and move to subfolder
                prt_ln(x[pos_file], x[pos_dir])

            else:
                # New subdirectory!
                # Create subfolder
                dir = x[pos_dir]
                print("mkdir " + dir)
                prt_ln(x[pos_file], dir)


# makeFolders("images_found.out")  # We found the images we were looking for.
