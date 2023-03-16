# MMOA
	WIP
Contact me for updates Or submit an [issue](https://github.com/jouterleys/mmoa) in the Repo

## Overview
This documentation is for the processsing scripts found in the [MMOA GitHub Repo](https://github.com/jouterleys/mmoa).
In that repo are scripts for data management and processing for the MMOA project. The purpose of this repo and documenation is to provide a unified processing approach for members of the project across different collection sites.

## Data Pipeline
A solid Data Pipeline is key to this project and can briefly be broken down into the following steps: 

* Video File Organization `Theia3D`
* Video File Batch Processing `Theia3D`
* C3D File Organization `Python`
* C3D File Analysis `Visual3D`

Each step will generally involve the execution of codes/scripts across a few different `programs`.

## Data Layout

    data
		...session-date
			...subjectencounter
				... action
					... trial
    data_c3d
		...session-date
			...subjectencounter
				... action
					... trial
	data_workspace
		...session-date
			...subjectencounter
				... action
					... trial
	data_v3d
		...subjectencounter
