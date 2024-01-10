#!/bin/bash 

#SCRIPT TO RUN VMEC TO REGCOIL

/home/ssharpe/STELLOPT_2/bin/xvmec2000 input.ncsx_c09r00_fixed 
/home/ssharpe/STELLOPT_2/bin/xbnorm wout_ncsx_c09r00_fixed.nc 0.1 128 128 64 64 64 64
/home/ssharpe/REGCOIL/regcoil/regcoil regcoil_in.regcoilNCSX 
#/home/ssharpe/REGCOIL/regcoil/regcoilPlot regcoil_out.regcoilNCSX.nc
python stellarator_coil.py 
gmsh S_coil.geo -2 -o coils.stl -v 0 
