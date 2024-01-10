import csv
import numpy as np
from numpy import linspace
from pylab import *

#Create geo file

geo=open('S_coil.geo', 'w')
print('SetFactory("OpenCASCADE");',file=geo)
print('//+',file=geo)
print("//+",file=geo)
#print("Coherence;",file=geo)
#print('//+',file=geo)
#print("Coherence;",file=geo)
#print('//+',file=geo)

#Read in coordinates 
#fy = open("y.csv", "r")
#fz = open("z.csv", "r")

coil_start = 6
coil_num = coil_start

coil_max =6
k=1 #number of loops defining the surfaces 
point_count=0
line_count=0

curve_init = np.zeros(coil_max)
curve_final = np.zeros(coil_max)

line_max_array=np.zeros(coil_max+1)

while coil_num <=coil_max: 
    k=1

    while k<=4:

        count=0
        x1_str = []
        y1_str = []
        z1_str = []

        filex="coords/x_"+ str(coil_num) + "_" + str(k) + ".csv"
        filey="coords/y_"+ str(coil_num) + "_" + str(k) + ".csv"
        filez="coords/z_"+ str(coil_num) + "_" + str(k) + ".csv"

        #print(coil_num)
        print(filex)

        with open(filex, "r") as file:

            for item in file:
                count=count+1
            #print(item)
                x1_str.append(item)

            #print(count,x1_str)
            tot_point=count
        
        print("Coil:",coil_num,"points",tot_point)
        with open(filey, "r") as file:

            for item in file:
        #count=count+1
       # print(item)
                y1_str.append(item)

   # print(count,x1_str)
   # tot_point=count

        with open(filez, "r") as file:

            for item in file:
      #  count=count+1
       # print(item)
                z1_str.append(item)

    #print(count,x1_str)
    #tot_point=count

            x = np.zeros(tot_point)
            y = np.zeros(tot_point)
            z = np.zeros(tot_point)
            count=0
          #  print("tot_point",tot_point)
    # convert to correct type (integer/float) and create complete loop
            tot_length = 0.0
            while count<= tot_point-1:
   
                if count<= tot_point: 
                    x[count]=float(x1_str[count]) 
                    y[count]=float(y1_str[count])
                    z[count]=float(z1_str[count])

                    #Update length 
                    if count >=1:
                        dist = math.sqrt(((x[count]-x[count-1])**2) +((y[count]-y[count-1])**2) +((z[count]-z[count-1])**2))
                        tot_length = tot_length + dist

                count=count+1
      #  print(x,y,z)
        print(tot_length)
        k=k+1
    coil_num=coil_num+1

