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
root = tkinter.Tk()
root.withdraw()
root.call('wm', 'attributes', '.', '-topmost', True)

#%% Functions

def remove_empty_dir(path):
    try:
        os.rmdir(path)
    except OSError:
        pass

def remove_empty_dirs(path):
    for root, dirnames, filenames in os.walk(path, topdown = False):
        for dirname in dirnames:
            #remove_empty_dir(os.path.readpath(os.path.join(root, dirname)))
            remove_empty_dir(os.path.realpath(os.path.join(root, dirname)))


#%% Options Flags

# Extract only sony
sony_only_flag = False

# Copy only filtered c3ds
filt_only_flag = True

# Include '_filt' in new filenames
filt_filename_flag = False

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


#%% Get Directory
# ask user to select [studyname]_c3d folder that will be reformatted
projdir = filedialog.askdirectory().replace('/','\\')

# make sure we create a path at the same level as the _c3d folder
c3d_level = projdir.split("\\")
# find index of file path that contains _c3d, searching backwards
c3d_level_index = 0
for level in reversed(c3d_level):
    if "_c3d" in level:
        c3d_level_index = level.find("_c3d")

if c3d_level_index != 0:
    c3d_level_path = "\\".join(c3d_level[0:c3d_level_index])
    last_folder_name = c3d_level[c3d_level_index]
    last_folder_name = last_folder_name.replace("_c3d", "_v3d")
    data_v3d_path = os.path.join(c3d_level_path, last_folder_name)

else:
    data_v3d_path = os.path.join(projdir, "data_v3d")



#%% Rename and Organize

# create a list of files within directory
filelist = get_list_of_files(projdir, fullpaths=True, search_subfolders=True)

# remove spaaces in filelist
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
    #file = filelist[0]
    # getting file info
    filenameparts = file.split('\\')
            
    filename = filenameparts[-1]
    trialname = filenameparts[-2]
    taskname = filenameparts[-3]
    subjname = filenameparts[-4]
    projname = filenameparts[-5].replace("_c3d", "")
    datefolder = filenameparts[-6]
    c3d_suffix = '.c3d'
    filt_c3d_suffix = '_filt.c3d'
    # creating new name
    if '_filt_' in file:
        if filt_filename_flag:
            #newname = subjname + '_' + taskname + '_' + trialname + '_filt.c3d'
            newname = subjname + '_' + taskname + '_' + trialname + filt_c3d_suffix
        else:
            #newname = subjname + '_' + taskname + '_' + trialname + '.c3d'
            #newname = subjname + '_' + taskname + '_' + trialname + filename_no_filt
            newname = subjname + '_' + taskname + '_' + trialname + c3d_suffix

    else:                 
        #newname = subjname + '_' + taskname + '_' + trialname + '.c3d'
        #newname = subjname + '_' + taskname + '_' + trialname + filename
        newname = subjname + '_' + taskname + '_' + trialname + c3d_suffix

    
    # creating nested subject folders, or not
    if nested_subject_flag:
        v3d_path = os.path.join(data_v3d_path,subjname)

    else:
        v3d_path = data_v3d_path
    
    print(v3d_path)

    # creating v3d-data folder, for all options
    if not os.path.isdir(v3d_path):
        os.makedirs(v3d_path)
    newfile = os.path.join(v3d_path,newname)
    
    # Probably want to make sure we check to see if file exists to not
    # overwrite?
    # copy+rename the file
    shutil.copy(file, newfile)
    
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