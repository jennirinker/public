#!/bin/bash
#
# Usage:
# 		$ ./TScompile_do.sh <directory-name>
#
# Linux bash script to compile TurbSim v1.0:
#		1) Compiles TurbSim, cleans up
#		2) Makes TurbSim executable
#		3) Moves file into /turbsim/
#
# Jenni Rinker, Duke University/NWTC
# 24-Mar-2015

# move into build_structure
cd ${1}/

echo "  Compiling TurbSim..."

# compile turbsim, make it exectuable
make turbsim
echo "  Cleaning..."
make clean
echo "  Making executable..."
chmod +x TurbSim

# rearrange /turbsim/, relocate to upper directory
mv -f TurbSim turbsim/

echo "  Script complete."