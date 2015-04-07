#!/bin/bash
#
# Usage:
# 		$ ./TScompile_do.sh <directory-name>
#
# Linux bash script to compile TurbSim v2.0:
#		1) Compiles TurbSim, cleans up
#		2) Makes TurbSim executable
#		3) Moves file into /turbsim/
#
# Jenni Rinker, Duke University/NWTC
# 07-Apr-2015

echo "  Copying makefile..."

# copy makefile into trunk/compiling/
cp Makefile ${1}/compiling/

# move into build_structure
cd ${1}/compiling/

echo "  Compiling TurbSim..."

# compile turbsim, make it exectuable
make
echo "  Cleaning..."
make clean
echo "  Making executable..."
chmod +x ../bin/TurbSim_glin64

echo "  Script complete."