# nwtc_python_tools
Python tools for working with NWTC CAE tools (creating input files,
  writing .bat files, running code, post-processing, etc.)

Summary
-------
The NWTC CAE tools (e.g., FAST, TurbSim) require text input files that
the executables are called on to produce text output. I've generated
some tools to streamline the process to automatically generate input
file for different wind conditions and different turbines.

This directory is currently a work in progress.

Usage
-----
A basic demonstration of the tools' capabilities can be found in 
`demo.py`. The script performs as follows:  
1. Create Python dictionary from specified .fst file  
2. Create wind-dependent, turbine-specific files (FAST and AeroDyn templates)  
3. Create wind-independent, turbine-specific files (Blades, tower, and pitch files)  

Contacts
--------
For issues, questions, or concerns, contact Jenni Rinker at
jennifer.rinker@duke.edu.
