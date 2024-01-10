#Create radial build of stellarator from an existing VMEC input file 

import argparse
import numpy as np
import matplotlib.pyplot as plt
import csv
import math
from RZ_convert import * 
from Radial_from_VMEC_working import *


# Set up the argument parser
parser = argparse.ArgumentParser(description="Plot a stellarator configuration from VMEC file.")
parser.add_argument("--file_in", type=str, required=True, help="Name of input file")
parser.add_argument("--nP", type=int, required=True, help="Number of Phi values in 2 pi")
parser.add_argument("--nT", type=int, required=True, help="Number of theta values in 2 pi")
parser.add_argument("--t_list", type=str, required=True, help="Thicknesses of the layers")

# Parse the arguments
args = parser.parse_args()

thicknesses = list(map(float, args.t_list.strip('[]').split(',')))

#Call VMEC boundary to 3D coord convertor

# Now call your function with the parsed arguments
m_axis = np.zeros((args.nP +1,args.nT +1,3))
plasma_coords = np.zeros((args.nP +1,args.nT +1,3))
MAG_AX("input.ncsx_c09r00_fixed",args.nP,m_axis)
VMEC_TO_RZ("RZ_coords.csv",args.nP,args.nT,3,plasma_coords)

print(m_axis) 
print("plasma coordinates") 
print(plasma_coords)
make_build(args.file_in,args.nP,args.nT,thicknesses,m_axis)
