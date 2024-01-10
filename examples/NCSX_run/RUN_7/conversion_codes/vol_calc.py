from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import *
from OCC.Extend.DataExchange import read_step_file
import argparse
import numpy
from stl import mesh

def Vol_from_STEP(step_name,tolerance):
    my_shape = read_step_file(step_name)
    prop = GProp_GProps()
    vol_out = brepgprop.VolumeProperties(my_shape, prop, tolerance)
    print(vol_out)
    return(vol_out)


#READ IN VALS FROM SHELL SCRIPT

# Set up the argument parser
parser = argparse.ArgumentParser(description="Calculate volume of any step file.")
parser.add_argument("--Name", type=str, required=True, help="Name of step file")
parser.add_argument("--tol", type=float, required=True, help="Tolerance level")


# Parse the arguments
args = parser.parse_args()

#Convert to lists
# Now call your function with the parsed arguments
vol = Vol_from_STEP(args.Name,args.tol)
print(vol)


myshape2 = read_step_file('box2.step')
prop = GProp_GProps()
tolerance = 1e-510# Adjust to your liking
volume = brepgprop_VolumeProperties(myshape2, prop, tolerance)
print(volume)


your_mesh = mesh.Mesh.from_file('coils.stl')
volume, cog, inertia = your_mesh.get_mass_properties()
print("Volume = {0}".format(volume))
