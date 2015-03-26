# compiling-turbsim
Summary
-------
This directory contains two bash scripts and a src file with a gzipped
file structure that can be used to easily compile the TurbSim source
code produced by the National Renewable Energy Laboratory on Linux. 
The code has been tested on a Linux machine running Xubuntu 14.04 with
TurbSim v1.06.00 and the NWTC Library v1.07.0.

There are two bash scripts: one to set up the file structure and unzip
the source code and one to compile TurbSim. The set-up need only be
done once, but the compiling routine can be done any time changes have
been made to the TurbSim source code.

Compiling TurbSim requires downloading the NWTC Subroutine Library and
the TurbSim self-extracting archive from the NWTC Information Portal:  
 - [NWTC Library](https://nwtc.nrel.gov/wind-and-water-tools/utilities-cae)  
 - [TurbSim](https://nwtc.nrel.gov/TurbSim)

Usage
-----
To compile TurbSim, clone the repository into a local drive and add the
TurbSim and NWTC Library files to src/. If "TScompile_setup.sh" is not
executable, make it so

`$ chmod +x TScompile_setup.sh`

and then run it

`$ ./TScompile_setup.sh`

to extract the source code and folder structure and apply patches for 
Linux compiling. To compile TurbSim, make "TScompile_do.sh" executable
if it is not already

`$ chmod +x TScompile_do.sh`

then execute it with the name of the folder with the source code to
compile:  

`$ ./TScompile_do.sh <directory-name>`

Contacts
--------
For issues, questions, or concerns, contact Jenni Rinker at
jennifer.rinker@duke.edu.
