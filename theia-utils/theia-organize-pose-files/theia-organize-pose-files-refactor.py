#%% Theia3D Pose File Rename and Organize

# organize-rename-pose-files.py
# author(s): Rob Kanko and Jereme Outerleys
# created: March 2020
# refactored for MMOA project


""" Python script for renaming and organizing c3d pose files output after
processing video data in Theia3D, intended for general data collection use

 Input: directory where data to be renamed/reformatted is located, assumes it has the structure:
     - [studyname_c3d folder]               ... ends with "_c3d"
          > [subject folder]                
               > [task folder]              
                    > [trial folder]        
                         > pose_0.c3d file
                         > pose_filt_0.c3d

Output: restructured directory, with renamed files:
    - [studyname_v3d folder]
         - [subject folder]
             > subject_task_trial.c3d
             > subject_task_trial_filt.c3d
             > ... 
"""

import os
import shutil
import re
import tkinter
from tkinter import filedialog

# needed for file select gui to work
root = tkinter.Tk()
root.withdraw()
root.call('wm', 'attributes', '.', '-topmost', True)

# Option to rename and copy only filtered pose data
filt_only_flag = True

# checks if files exist to not overwrite and to make the directory if it doesn't exist
def safe_move(src_file, dst_file):
    #src_file = old_filename
    #dst_file = new_filename
    if os.path.isfile(dst_file):
        print(f"File {dst_file} already exists. Skipping...")
    else:
        if not os.path.isdir(os.path.dirname(dst_file)):
            os.makedirs(os.path.dirname(dst_file))
        shutil.copy(src_file, dst_file)
        print(f"File {dst_file} created.")

# ask user to select [studyname]_c3d folder or dated-session folder that contain c3ds to be reformatted
projdir = filedialog.askdirectory().replace('/','\\')

# find the path containing the _c3d folder and replace it with _v3d
match = re.search(r"(.*)\\[^\\]*_c3d", projdir)
if match:
    data_v3d_path = match.group(1) + "\\data_v3d"
else:
    data_v3d_path = os.path.join(projdir, "data_v3d")

# define a dictionary to hold the new filenames
renamed_files = {}

# iterate through the directory tree and find all the c3d files
for subdir, _, files in os.walk(projdir):
    
    # Extract only filt c3ds
    if filt_only_flag:
        files = [file for file in files if '_filt_' in file]
    
    for file in files:
       
        if file.endswith('.c3d') and 'pose' in file:
            
            # parse the subject, task, and trial information from the file path
            trial = subdir.split('\\')[-1]
            task = subdir.split('\\')[-2]
            subject = subdir.split('\\')[-3]
            
            # determine the new filename based on the subject, task, and trial
            new_filename = f"{subject}_{task}_{trial}.c3d"
            
            # check if this file has a filtered version
            if 'filt' in file:
                new_filename = new_filename.replace('.c3d', '_filt.c3d')
                
            # add the old and new filenames to the dictionary
            renamed_files[os.path.join(subdir, file)] = os.path.join(data_v3d_path,subject, new_filename)

# iterate through the dictionary and rename/move the files
for old_filename, new_filename in renamed_files.items():
    safe_move(old_filename, new_filename)
    
    
    