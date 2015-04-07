# compiling-turbsim-v2.0
Routines to compile TurbSim v2.0 on Linux

Summary
-------
This directory contains two bash scripts and a makefile that can be 
used to easily compile the TurbSim v2.0 source code produced by the 
National Renewable Energy Laboratory on Linux. The code has been 
tested on a Linux machine running Xubuntu 14.04 with TurbSim v2.00.01.  

There are two bash scripts: one to set up the file structure and unzip
the source code and one to compile TurbSim. The set-up need only be
done once, but the compiling routine can be done any time changes have
been made to the TurbSim source code.

Requirements
------------
The LAPACK and BLAS packages must be installed. This can be easily done
from the command line:  
`$ sudo apt-get install liblapack-dev`  
`$ sudo apt-get install libblas-dev`  

Download the compressed TurbSim source code from the NWTC Information
Portal:
 - [TurbSim v2.0](https://nwtc.nrel.gov/Alphas)  

Once this repository is cloned, put the TurbSim executable in src/.

Usage
-----
To compile TurbSim, clone the repository into a local drive and add the
TurbSim self-extracting archive to src/. If "TScompile_setup.sh" is not
executable, make it so

`$ chmod +x TScompile_setup.sh`

and then run it

`$ ./TScompile_setup.sh`

to extract the source code. To compile TurbSim, make "TScompile_do.sh"
executable if it is not already

`$ chmod +x TScompile_do.sh`

then execute it with the name of the folder with the source code to
compile:  

`$ ./TScompile_do.sh <directory-name>`



Contacts
--------
For issues, questions, or concerns, contact Jenni Rinker at
jennifer.rinker@duke.edu.
