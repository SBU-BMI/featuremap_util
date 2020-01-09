def find_files(filepath):
    '''
    We're creating a shell script (findem.sh) based on input:
    ls -l | awk '{print $9}' > ~/images_to_find.list
    Find/replace when necessary. "prediction-"
    ./findem.sh > foundem.out
    '''
    print("dir=\"/path/to/images\"")
    with open(filepath) as fp:
        for line in fp:
            line = line.rstrip()
            # step 1 (for prediction):
            # if "color" in line:
            #     print(line.replace("color-", ""))
            # step 2:
            print("find $dir -name \"" + str(line) + "*.tif\"")  # Modify line + '.tif' & identify 'dir'


# find_files('images_to_find.list')  # Start here.


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
                # Given that the input data is local, find input prediction file and move to subfolder
                print("find . -name " + "prediction-" + x[6].replace(".tif", "") + " -exec mv -- \"{}\" ./" + x[
                    5] + "/ \;")
            else:
                # Create subfolder
                dir = x[5]
                print("mkdir " + dir)
                print("find . -name " + "prediction-" + x[6].replace(".tif",
                                                                     "") + " -exec mv -- \"{}\" ./" + dir + "/ \;")


# makeFolders("foundem.out")  # We found the images we were looking for.
