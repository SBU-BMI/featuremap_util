def find_files(filepath):
    '''
    We're creating a shell script (findem.sh) based on input:
    ls -l FOLDER | awk '{print $9}' > images_to_find.list
    May or may not work if slide name was truncated.
    Output to foundem.out
    '''
    with open(filepath) as fp:
        for line in fp:
            line = line.rstrip()
            print("find $dir -name \"" + str(line) + "*\"")  # Modify line + '.tif' etc


# find_files('images_to_find.list')


def makeFolders(filepath):
    '''
    We're creating a script.
    1) Figure out which slides we're going to need
    2) Read in that list and make subfolders
    '''
    dir = ''
    with open(filepath) as fp:
        for line in fp:
            line = line.rstrip()
            x = line.split("/")
            if dir == x[5]:
                # Find input prediction file and move to subfolder
                print("find . -name " + "prediction-" + x[6].replace(".tif", "") + " -exec mv -- \"{}\" ./" + x[
                    5] + "/ \;")
            else:
                # Create subfolder
                dir = x[5]
                print("mkdir " + dir)
                print("find . -name " + "prediction-" + x[6].replace(".tif", "") + " -exec mv -- \"{}\" ./" + dir + "/ \;")


# makeFolders("foundem.out")


def copyFiles(file_to_read, dst_folder):
    '''
    Problem. Output files are in different folders, all with the same name.
    Solution. Create copy and rename script.
    1) find [src_folder] -name *.csv > ~/results.in
    2) Run this > results.out (results.sh)
    '''
    with open(file_to_read) as fp:
        for csv_file_path in fp:
            csv_file_path = csv_file_path.rstrip()
            arr = csv_file_path.split("/")
            folder = arr[len(arr) - 2]  # folder name is unique name
            # old_name = arr[len(arr) - 1]  # old name
            new_name = str(folder) + ".csv"
            print("sudo cp " + csv_file_path + " " + dst_folder + "/" + new_name)
    print("find " + dst_folder + " -type f | wc -l")
