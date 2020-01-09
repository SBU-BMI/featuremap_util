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
    print("find . -name " + "prediction-" + fname.replace(".tif", "") + " -exec mv -- \"{}\" ./" + dir + "/ \;")
    print("find . -name " + "color-" + fname.replace(".tif", "") + " -exec mv -- \"{}\" ./" + dir + "/ \;")


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
            if dir == x[5]:
                # Same subdirectory
                # Given that the input data is local, find input prediction file and move to subfolder
                prt_ln(x[6], x[5])

            else:
                # New subdirectory!
                # Create subfolder
                dir = x[5]
                print("mkdir " + dir)
                prt_ln(x[6], dir)


# makeFolders("images_found.out")  # We found the images we were looking for.
