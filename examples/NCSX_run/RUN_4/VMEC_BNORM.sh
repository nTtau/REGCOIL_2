#!/bin/bash 

#SCRIPT TO RUN VMEC TO REGCOIL

/home/ssharpe/STELLOPT_2/bin/xvmec2000 input.ncsx_c09r00_fixed 
/home/ssharpe/STELLOPT_2/bin/xbnorm wout_ncsx_c09r00_fixed.nc 0.1 64 64 64 64 64 64
/home/ssharpe/REGCOIL/regcoil/regcoil regcoil_in.regcoilNCSX 
#/home/ssharpe/REGCOIL/regcoil/regcoilPlot regcoil_out.regcoilNCSX.nc
