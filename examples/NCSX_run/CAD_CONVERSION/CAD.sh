#!/bin/bash 

#SCRIPT TO RUN VMEC TO REGCOIL

./VMEC_CAD_ALL2.sh
python stellarator_coil.py 
gmsh S_coil.geo -2 -o coils.stl -v 0 
