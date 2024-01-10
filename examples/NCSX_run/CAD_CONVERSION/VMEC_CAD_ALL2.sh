#!/bin/bash 

#Set values of nphi and ntheta 
nphi=90
ntheta=90
#Lists have to be read in as a string initially 
#a and b values for each layer 
#ie if a =2.0 one layer, next layer was 2.2 that'd be 0.2m thickness for the outer layer 
thickness="[0.0]"
#number of layers 
#create points for meshing
echo 'Generating Points and geo files'
python VMEC_CAD_ALL.py --file_in "input.ncsx_c09r00_fixed" --nP $nphi --nT $ntheta --t_list $thickness 

echo 'Generating stl and step files '
gmsh layer_0.geo -nt 16 -2 -o layer_0.stl
gmsh layer_0.geo -nt 16 -3 -o layer_0.step  

#echo 'Creating final step file with all layers' 

#Call code that sets the physical surf/vols here 
#Run meshing command on the geo file 








