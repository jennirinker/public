# update-nrel-m4-data
Routines to update local copies of M$ data from NREL

Summary
-------
Routines to update local version of folder structure and .mat files from online
directory at specified URL. Works for both 20-Hz and 10-min M4 data. Repository
contains Python module with helper functions (URLDataDownload.py) and script to
call from command line to perform update (update_nrel.py).

Currently structured for Windows file paths/filewrite options. To get it to work
on Linux, modify the base paths below and the path construction/file writing 
flags in help function updateDirectory.

Usage
-----
From a Python interpreter:  
`>>> execfile('update_nrel.py')`  
From Windows terminal:  
`> python update_nrel.py`

Contacts
--------
For issues or questions about the data, email Andrew Clifton at 
Andrew.Clifton@nrel.gov. Lots of information can be found online at the [NWTC
portal](https://wind.nrel.gov/forum/wind/viewforum.php?f=31&sid=d8b2a72a85b37ab5a9690e97f79f4760).
For issues with the script, email me at jennifer.rinker@duke.edu.
