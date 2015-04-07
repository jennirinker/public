#!/bin/bash
#
# Usage:
# 		$ ./TScompile_setup.sh
#
# Linux bash script to set up source files/structure necessary for
# TurbSim v2.0 compilation. Script has four steps:
#		1) Clear/create build structure folder
#		2) Unzip source code/file structure to folder
#		3) Apply patches for Linux compilation
#		4) Delete Windows executables bundled in source code
#
# Jenni Rinker, Duke University/NWTC
# 07-Apr-2015

# if file structure already exists, remove it
if [ -d trunk ] ; then rm -rf trunk ; fi

echo "  Unzipping files..."

# extract the subroutine library and the turbsim source code
unzip -q src/TurbSim_v2.00.01a-bjj.exe -d trunk/

#echo "  Deleting Windows executables..."

# delete executables
rm -f trunk/bin/TurbSim_Win32.exe
rm -f trunk/bin/TurbSim_x64.exe

echo "  Setup for TurbSim v2.0 compilation complete."