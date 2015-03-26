#!/bin/bash
#
# Usage:
# 		$ ./TScompile_setup.sh
#
# Linux bash script to set up source files/structure necessary for
# TurbSim compilation. Script has four steps:
#		1) Clear/create build structure folder
#		2) Unzip source code/file structure to folder
#		3) Apply patches for Linux compilation
#		4) Delete Windows executables bundled in source code
#
# Jenni Rinker, Duke University/NWTC
# 24-Mar-2015

echo "  Creating structure..."

# if file structure already exists, remove it
if [ -d build_structure ] ; then rm -rf build_structure ; fi

echo "  Unzipping files..."

# extract the folder structure
tar -zxf src/build_structure.tar.gz

# extract the subroutine library and the turbsim source code
tar -zxf src/NWTC_Lib_v1.07.00b-mlb.tar.gz -C build_structure/nwtc/
unzip -q src/TurbSim_v1.06.00.exe -d build_structure/turbsim

echo "  Applying patches..."

# apply patches for compiling on Linux
cd build_structure
patch -s --dry-run -p1 -i all.patch
patch -s -p1 -i all.patch

echo "  Deleting Windows executables..."

# delete executables
rm -f turbsim/TurbSim.exe
rm -f turbsim/TurbSim64.exe

echo "  Setup for TurbSim compilation complete."