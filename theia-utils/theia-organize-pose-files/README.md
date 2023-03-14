# theia-organize-pose-files
	Script to organize and rename pose files saved through batch processing using Theia3D.
	Behaviour of output is changed using flags.
	Default Flags are as follows:
			- filt_only_flag = True: Copy only filtered c3ds
			- person_zero_flag = True: Copy only person 0
			- nested_subject_flag = True: Results in Nested Subject Folders (but all action and trial folders are ommitted)
			- delete_dir_flag = False: Does not delete original folders+data
# Data Formats:
    Example saved batch pose files:  
        data_c3d
            S000001
                Walk
                    001
                        pose_0.c3d
                        pose_filt_0.c3d
                    002
                        pose_0.c3d
                        pose_filt_0.c3d
                Run
                    001
                        pose_0.c3d
                        pose_filt_0.c3d
            S000002
                Walk
                    001
                        pose_0.c3d
                        pose_filt_0.c3d
                    002
                        pose_0.c3d
                        pose_filt_0.c3d
                Run
                    001
                        pose_0.c3d
                        pose_filt_0.c3d
                        
    Input:
        - select 'data_c3d' folder when prompted

    Output:
		data_c3d
			S000001
				S000001_Walk_001.c3d
				S000001_Walk_001_filt.c3d
				S000001_Walk_002.c3d
				S000001_Walk_002_filt.c3d
				S000001_Run_001.c3d
				S000001_Run_001_filt.c3d
				S000002_Walk_001.c3d
				S000002_Walk_001_filt.c3d
				S000002_Walk_002.c3d
				S000002_Walk_002_filt.c3d
				S000002_Run_001.c3d
				S000002_Run_001_filt.c3d