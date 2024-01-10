#Create radial build of stellarator from an existing VMEC input file 

import argparse
import numpy as np
import matplotlib.pyplot as plt
import csv
import math

def make_build(input_file,Nphi,Ntheta,thickness_list,mag_ax):
 
    print("Nphi,Ntheta: ",Nphi,Ntheta)

    Coords = np.zeros((Nphi+1,Ntheta+1,3))
    Coords_orig = np.zeros((Nphi+1,Ntheta+1,3))
    X = np.zeros((Nphi+1,Ntheta+1))
    Y = np.zeros((Nphi+1,Ntheta+1))
    Z = np.zeros((Nphi+1,Ntheta+1))
    mag_ax = np.zeros((Nphi+1,3))
    #Read in 3D coords file  
    X_str = []
    Y_str = []
    Z_str = [] 

    counter = 0

    tot_layer = len(thickness_list)

    point_file = open(input_file, "r")
    file = csv.DictReader(point_file)

    for col in file:
    # count number of coils
        counter = counter + 1

    # Read in values
        X_str.append(col["X"])
        Y_str.append(col["Y"])
        Z_str.append(col["Z"])

    tot_point = counter

    counter=0
    Phi_count=0
  
    while Phi_count <= Nphi: 

        Theta_count = 0

        while Theta_count <=Ntheta:

            Coords_orig[Phi_count,Theta_count,0] = X_str[counter] 
            Coords_orig[Phi_count,Theta_count,1] = Y_str[counter] 
            Coords_orig[Phi_count,Theta_count,2] = Z_str[counter]

#            if Phi_count ==0: 
#                print(Phi_count,Theta_count,Coords_orig[Phi_count,Theta_count,0]) 
   
            counter=counter+1
            Theta_count = Theta_count+1

        Phi_count=Phi_count+1
    #Calculate average R0 
    half_loop = int((0.5*Ntheta))+1
    R0 = (Coords_orig[0,0,0] - (0.5*(Coords_orig[0,0,0] - Coords_orig[0,int((0.5*Ntheta))+1,0])))
 #   print(Coords_orig[0,0,0],Coords_orig[0,46,0])
    print("R0 estimate: ",R0)

    dPhi = (2*np.pi)/Nphi
    Phi=0.0 
    Phi_count = 0 

    centre_name= "central_loop.csv"
    centre = open(centre_name, "w")

    layer_count =0 

    while layer_count <=tot_layer-1: 

        P=0.0 
        Phi_count = 0
        thickness = thickness_list[layer_count] 
        print("layer: ", layer_count, "thickness of layer:",thickness)

       # filename= "layer_" + str(layer_count) +".csv"
        #layer_csv = open(filename, "w")

        geo_name= "layer_" + str(layer_count) +".geo"
        geo = open(geo_name, "w")

        print('SetFactory("OpenCASCADE");', file=geo)
        print("//+", file=geo)

    
    #  print("printing test values")
    #    print("X,Y,Z", file=layer_csv)

        while Phi_count<= Nphi : 

            T = 0.0 
            Theta_count=0

            while Theta_count <=Ntheta:
       
            # If layer =0, plasma keep same as VMEC boundary coords 
                if layer_count == 0: 
                    Coords[Phi_count,Theta_count,0]=Coords_orig[Phi_count,Theta_count,0]
                    Coords[Phi_count,Theta_count,1]=Coords_orig[Phi_count,Theta_count,1]
                    Coords[Phi_count,Theta_count,2]=Coords_orig[Phi_count,Theta_count,2]

                  #  print(Coords[Phi_count,Theta_count,0],  

            # If layer /= 0, add on the layer thickness to the plasma coords 
                else:
                    print("Creating layer ",layer_count) 
                    print("Layer thickness is :", thickness)

                    x_diff = Coords_orig[Phi_count,Theta_count,0] - mag_ax[Phi_count,0]
                    y_diff = Coords_orig[Phi_count,Theta_count,1] - mag_ax[Phi_count,1]
                    z_diff = Coords_orig[Phi_count,Theta_count,2] - mag_ax[Phi_count,2]

                    total_diff = math.sqrt(((x_diff)**2) + ((y_diff)**2) + ((z_diff)**2))
                    x_diff_ratio = x_diff/total_diff 
                    x_new_diff = x_diff + (thickness*x_diff_ratio) 
                    y_diff_ratio = y_diff/total_diff 
                    y_new_diff = y_diff + (thickness*y_diff_ratio)
                    z_diff_ratio = z_diff/total_diff 
                    z_new_diff = z_diff + (thickness*z_diff_ratio)

                    new_total_diff = math.sqrt(((x_new_diff)**2) + ((y_new_diff)**2) + ((z_new_diff)**2))

                    print("Previous difference: ",x_diff,y_diff,z_diff,total_diff)
                    print("New difference: ",x_new_diff,y_new_diff,z_new_diff,new_total_diff)

                    # SET NEW X,Y,Z based on scaling 
                  #  Coords[Phi_count,Theta_count,0]=mag_ax[Phi_count,0] + x_new_diff
                   # Coords[Phi_count,Theta_count,1]=mag_ax[Phi_count,1] + y_new_diff
                    #Coords[Phi_count,Theta_count,2]=mag_ax[Phi_count,2] + z_new_diff
                    Coords[Phi_count,Theta_count,0]=Coords[Phi_count,Theta_count,0]*(1+thickness)#mag_ax[Phi_count,0] 
                    Coords[Phi_count,Theta_count,1]=Coords[Phi_count,Theta_count,1]*(1+thickness)#mag_ax[Phi_count,1] 
                    Coords[Phi_count,Theta_count,2]=Coords[Phi_count,Theta_count,2]*(1+thickness)#mag_ax[Phi_count,2]             

#                T = T + dtheta
                Theta_count = Theta_count + 1 
#            P = P + dphi
            Phi_count=Phi_count+1

        #All points determined - make geo file 

        # Reorder loops and remove overlapping points
        loop_jump = Ntheta +1 
        # Last loop is a repeat of the first, ignore
        loop_num_tot = Nphi
        # loop_num_tot = 5
        loop_num = 1
        final_point=(int(((loop_num_tot - 1) * (loop_jump-1))) + loop_jump-2)
        #print("FINAL POINT:",final_point)

        # Define array to store coordinates for each loop

        while loop_num <= loop_num_tot:
  #  print("Loop number: ", loop_num)
            count_min = int(((loop_num - 1) * loop_jump) -(1*(loop_num-1)))
            count_max = count_min + loop_jump-1
            count = count_min
            #filename2 = "NEW_RUN/layer_" + str(layer_count) + "_loop_" +str(loop_num) + ".csv"
           # output_file = open(filename2, "w")
          #  print("Count max: ", count_max)

            while count <= count_max-1:
                point_num = count - count_min
                #print("POINT NUM:,",point_num,count)

               # print( X[loop_num-1,point_num],",", Y[loop_num-1,point_num],",", Z[loop_num-1,point_num],file=output_file)
                print(
                    "Point(",
                    count,
                    ") = {",
                    Coords[loop_num-1,point_num,  0],
                    ",",
                    Coords[ loop_num-1,point_num, 1],
                    ",",
                    Coords[ loop_num-1,point_num, 2],
                    ",",
                    "1.0};",
                    file=geo,
                )
                print("//+", file=geo)

                count = count + 1

            loop_num = loop_num + 1

        # Send lines to GMSH
# loop_num_tot = 10
        loop_num = 1
        loop_max = loop_num_tot

        line_shift = Ntheta*Nphi

        while loop_num <= loop_num_tot:
            count_min = int(((loop_num - 1) * loop_jump) -(1*(loop_num-1)))
            count_max = count_min + loop_jump-1
          #  print("count_max : " , count_max)
            count = count_min

            while count <= count_max-1:
                point_num = count - count_min

        # Connect points of the loop
                if count == count_max-1:
            # print("Line(",count,") = {",count,",",point_num,"};",file=geo)
            # print('//+',file=geo)
               #     print(count)

                    print(
                        "Line(",
                        count,
                        ") = {",
                        count,
                        ",",
                        count - (loop_jump - 2),
                        "};",
                        file=geo,
                    )
                    print("//+", file=geo)

                else:
                    print("Line(", count, ") = {", count, ",", count + 1, "};", file=geo)
                    print("//+", file=geo)
        # Final loop must connect back to the first

                if loop_num == loop_num_tot:
                    print(
                        "Line(",
                        count + line_shift,
                        ") = {",
                        count,
                        ",",
                        point_num,
                        "};",
                        file=geo,
                    )
                    print("//+", file=geo)

                else:
                    print(
                        "Line(",
                        count + line_shift,
                        ") = {",
                        count,
                        ",",
                        count + loop_jump-1,
                        "};",
                        file=geo,
                    )
                    print("//+", file=geo)

        # print("Point(",count,") = {",Coords[loop_num-1,point_num,0],",",Coords[loop_num-1,point_num,1],",",Coords[loop_num-1,point_num,2],",","1.0};",file=geo)
        # print('//+',file=geo)

                count = count + 1

            loop_num = loop_num + 1

        #ADD SURFACES
        loop_num = 1

# line_shift = tot_point
#print(line_shift)
        sloop_str = "Surface Loop(1) = {"


        while loop_num <= loop_num_tot:
    #  if loop_num == loop_num_tot:
    #     loop_num = loop_max
    #    print("loop max =, ",loop_max)
    #   loop_num_tot = loop_max

            count_min = int(((loop_num - 1) * loop_jump) -(1*(loop_num-1)))
            count_max = count_min + loop_jump-2
          #  print("Surface count max: ",count_max)
            count = count_min

            while count <= count_max:
                point_num = count - count_min

                if count == count_max:
                    if loop_num == loop_num_tot:
                       # print("FINAL LOOP")
                        print(
                            "Curve Loop(",
                            ((2 * count) + 1),
                            ") = {",
                            count,
                            ",",
                            count + line_shift,
                            ",",
                            point_num,
                            ",",
                            (-1 * (line_shift + count - point_num)),
                            "};",
                            file=geo,
                        )
                        print("//+", file=geo)
                        print("Surface(", count, ") = {", ((2 * count) + 1), "};", file=geo)
                        print("//+", file=geo)


                    else:
                        print(
                            "Curve Loop(",
                            ((2 * count) + 1),
                            ") = {", 
                            count,
                            ",",
                            count + line_shift,
                            ",",
                            count_max + point_num+1,
                            ",",
                            (-1 * (line_shift + count - point_num)),
                            "};",
                            file=geo,
                        )
                        print("//+", file=geo)
                        print("Surface(", count, ") = {", ((2 * count) + 1), "};", file=geo)
                        print("//+", file=geo)

            # print(count,(2*count)+1,(-1*(line_shift+count-point_num)))

                else:
                    if loop_num == loop_num_tot:
                      #  print("FINAL LOOP")
                        print(
                            "Curve Loop(",
                            ((2 * count) + 1),
                            ") = {",
                            count,
                            ",",
                            count + line_shift,
                            ",",
                            point_num,
                            ",",
                           (-1 * (count + line_shift + 1)),
                           "};",
                           file=geo,
                        )
                        print("//+", file=geo)
                        print("Surface(", count, ") = {", ((2 * count) + 1), "};", file=geo)
                        print("//+", file=geo)


                    else:
                        print(
                            "Curve Loop(",
                            ((2 * count) + 1),
                            ") = {",
                            count,
                            ",",
                            count + line_shift,
                            ",",
                            count_max + point_num+1,
                            ",",
                            (-1 * (count + line_shift + 1)),
                            "};",
                            file=geo,
                        )
                        print("//+", file=geo)
                        print("Surface(", count, ") = {", ((2 * count) + 1), "};", file=geo)
                        print("//+", file=geo)

            # Add surface to surface loop
                if count == final_point:
                    sloop_str = sloop_str + str(count) + "};"
                    print(sloop_str, file=geo)
                    print("//+", file=geo)
                    print("Volume(1) = {1};", file=geo)
                else:
                    sloop_str = sloop_str + str(count) + ","

                count = count + 1

            loop_num = loop_num + 1


        #print(Coords)
        layer_count=layer_count+1 

   
#Set a and b for each stellarator layer 
#a_vals = [2.0,2.2,2.5] 
#b_vals = [1.0,1.2,1.5]
#print(len(a_vals),len(b_vals))


#make_stellarator(5.0,3,a_vals,b_vals)

# Set up the argument parser
#parser = argparse.ArgumentParser(description="Plot a stellarator configuration from VMEC file.")
#parser.add_argument("--file_in", type=str, required=True, help="Name of input file")
#parser.add_argument("--nP", type=int, required=True, help="Number of Phi values in 2 pi")
#parser.add_argument("--nT", type=int, required=True, help="Number of theta values in 2 pi")
#parser.add_argument("--t_list", type=str, required=True, help="Thicknesses of the layers")

# Parse the arguments
#args = parser.parse_args()
#
#thicknesses = list(map(float, args.t_list.strip('[]').split(',')))

#Call VMEC boundary to 3D coord convertor

# Now call your function with the parsed arguments
#make_build(args.file_in,args.nP,args.nT,thicknesses)
