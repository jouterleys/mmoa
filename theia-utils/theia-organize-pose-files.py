#%% Theia3D Pose File Rename and Organize

# organize-rename-pose-files.py
# author: Rob Kanko and Jereme Outerleys
# created: March 2020


""" Python script for renaming and organizing c3d pose files output after
processing video data in Theia3D, intended for general data collection use."""

# Input: 
# - directory where data to be renamed/reformatted is located, assumes it has the structure:
#     - [studyname_c3d folder]               ... can be anything, but expected to end with "_c3d"
#          > [subject folder]                ... can be anything
#               > [task folder]              ... can be anything
#                    > [trial folder]        ... can be anything
#                         > pose_0.c3d file
#                         > pose_filt_0.c3d

# Output:
# - restructured directory, with renamed files:
#    - [studyname_c3d folder]
#         - [subject folder] (optional, set nested_subject_flag = True)
#             > subject_task_trial.c3d
#             > subject_task_trial_filt.c3d
#             > ... etc.

#%% Imports
import os
import tkinter
from tkinter import filedialog
import shutil
import sys

#%% Options Flags

# Extract only sony (looks for sony in the file path)
sony_only_flag = False

# Copy only filtered c3ds
filt_only_flag = True

# Keep '_filt' in new filenames
filt_filename_flag = True

# Copy only person 0
person_zero_flag = True

# Nested Subject Folders
nested_subject_flag = True

# Delete c3d directory flag
delete_dir_flag = False

# Extract only forced merged c3ds flag
force_merge_flag = False

# Replace c3d directory flag
replace_dir_flag = False
if replace_dir_flag and not delete_dir_flag:
    mismatch_check = input("Delete directory flag is False, while Replace directory flag is True. Do you want to continue and Replace (delete) the original directory? y/[n]: ")
    if mismatch_check == "y":
        delete_dir_flag = True
    else:
        sys.exit()
        
#%% Functions
def get_file_directory():
    """ ask user to select [studyname]_c3d folder that will be reformatted
     and correct for operating system specific path separator """
     
    # needed for tinker dialog to not hang
    root = tkinter.Tk()
    root.withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)
    projdir = filedialog.askdirectory()
    projdir = os.path.normpath(projdir)
    return projdir   

            
# checks if files exist to not overwrite and to make the directory if it doesn't exist
def safe_move(src_file, dst_file):
    """checks if files exist to not overwrite and to make the directory if it doesn't exist"""

    if os.path.isfile(dst_file):
        print(f"File {dst_file} already exists. Skipping...")
    else:
        if not os.path.isdir(os.path.dirname(dst_file)):
            os.makedirs(os.path.dirname(dst_file))
        shutil.copy(src_file, dst_file)
        print(f"File {dst_file} created.")

def make_data_v3d_folder_path(dirName):
    """create output folder (*_v3d) at the same level as the *_c3d folder"""
    
    c3d_level = dirName.split(os.path.sep)
    # find index of file path that contains _c3d, searching backwards
    c3d_level_index = 0
    for i, level in reversed(list(enumerate(c3d_level))):
        if "_c3d" in level:
            c3d_level_index = i
            break

    if c3d_level_index != 0:
        c3d_level_path = os.path.sep.join(c3d_level[0:c3d_level_index])
        last_folder_name = c3d_level[c3d_level_index]
        last_folder_name = last_folder_name.replace("_c3d", "_v3d")
        data_v3d_path = os.path.join(c3d_level_path, last_folder_name)

    else:
        # if no *_c3d found just create a data_v3d in the dirName provided
        data_v3d_path = os.path.join(dirName, "data_v3d")
    
    return data_v3d_path


def get_list_of_files(dirName, fullpaths=True, search_subfolders=True):
    """Get a list of all files and folders within the provided directory."""
    
    import os
    
    # names in the given directory 
    listOfFiles = sorted(os.listdir(dirName))
    allFiles = list()
    
    # Iterate over all the entries
    for entry in listOfFiles:
        
        # Create full path
        fullPath = os.path.join(dirName, entry)
        
        # If entry is a directory:
        if os.path.isdir(fullPath) and search_subfolders == True:
            
            # get the files within and add them to the list
            allFiles = allFiles + get_list_of_files(fullPath, search_subfolders=True)
        
        # is directory and search_subfolders=False
        elif os.path.isdir(fullPath) and search_subfolders == False:
            
            # move on to the next entry, without adding this folder to the list
            continue
        
        # is not directory (i.e. is a file)
        elif not os.path.isdir(fullPath):
            
            # add to the list
            allFiles.append(fullPath)
            
    if fullpaths == True:
        return allFiles
    else:
        outFiles = [os.path.split(file)[1] for file in allFiles]
        return outFiles
    
def remove_empty_dir(path):
    try:
        os.rmdir(path)
    except OSError:
        pass

def remove_empty_dirs(path):
    for root, dirnames, filenames in os.walk(path, topdown = False):
        for dirname in dirnames:
            remove_empty_dir(os.path.realpath(os.path.join(root, dirname)))
            
            
#%% Get Directory
# ask user to select [studyname]_c3d folder that will be reformatted
projdir = get_file_directory()

# create output *_v3d folder path
data_v3d_path = make_data_v3d_folder_path(projdir)

#%% Rename and Organize

# create a list of files within directory
filelist = get_list_of_files(projdir, fullpaths=True, search_subfolders=True)

# remove spaces in filelist
# filelist = [file.replace(" ", "") for file in filelist]

# Extract only c3ds
filelist = [file for file in filelist if '.c3d' in file]

# Extract only sony
if sony_only_flag:
    filelist = [file for file in filelist if '-Sony' in file]

# Extract only filt
if filt_only_flag:
    filelist = [file for file in filelist if '_filt_' in file]

# Extract only person 0
if person_zero_flag:
    filelist = [file for file in filelist if ('pose_0' in file) or ('filt_0' in file)]
    
# Extract only person 0
if force_merge_flag:
    filelist = [file for file in filelist if '_merged' in file]
   
# organize and rename, if only person 0 available or only keeping person 0
for file in filelist:

    # getting file info
    filenameparts = file.split(os.path.sep)
            
    filename = filenameparts[-1]
    trialname = filenameparts[-2]
    taskname = filenameparts[-3]
    subjname = filenameparts[-4]

    c3d_suffix = '.c3d'
    filt_c3d_suffix = '_filt.c3d'
    
    # creating new name
    
    
    if '_filt_' in file:
        if filt_filename_flag:
            newname = subjname + '_' + taskname + '_' + trialname + filt_c3d_suffix
        else:
            newname = subjname + '_' + taskname + '_' + trialname + c3d_suffix

    else:                 
        newname = subjname + '_' + taskname + '_' + trialname + c3d_suffix

    
    # creating nested subject folders, or not
    if nested_subject_flag:
        v3d_path = os.path.join(data_v3d_path,subjname)
    else:
        v3d_path = data_v3d_path
    
    # new file name 
    newfile = os.path.join(v3d_path,newname)
    
    # copy+rename the file
    safe_move(file, newfile)
    
    # Delete c3d directory flag
    if delete_dir_flag:
        # delete trial directory (it's either empty or includes person 1 etc. data)
        shutil.rmtree(os.path.join(projdir,subjname,taskname,trialname))
    
        # delete empty task folder
        if not os.listdir(os.path.join(projdir,subjname,taskname)):
            os.rmdir(os.path.join(projdir,subjname,taskname))
    
        # delete empty subject folder
        if not os.listdir(os.path.join(projdir,subjname)):
            os.rmdir(os.path.join(projdir,subjname))
            
            
# Replace c3d directory flag
if replace_dir_flag:
    source_folder = os.path.join(projdir,"v3d-data")
    dest_folder = projdir
    
    for root, dirs, files in os.walk(source_folder):
        if nested_subject_flag:
            for thisdir in dirs:
                shutil.move(os.path.join(root, thisdir), projdir)

        else:
            for name in files:
                shutil.move(os.path.join(root, name), projdir)
        
    os.rmdir(os.path.join(projdir,"v3d-data"))
    
    
# Remove empty folders
#remove_empty_dirs(projdir)