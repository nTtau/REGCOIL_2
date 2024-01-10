import csv
import numpy as np
from numpy import linspace
from pylab import *

#Create geo file

geo=open('S_coil.geo', 'w')
print('SetFactory("OpenCASCADE");',file=geo)
print('//+',file=geo)
print('//+',file=geo)

#Read in coordinates 
#fy = open("y.csv", "r")
#fz = open("z.csv", "r")

coil_start = 1
coil_num = coil_start

coil_max =1
k=1 #number of loops defining the surfaces 
point_count=0
line_count=0

curve_init = np.zeros(coil_max)
curve_final = np.zeros(coil_max)

line_max_array=np.zeros(coil_max+1)

while coil_num <=coil_max: 
    k=1

    while k<=2:

        count=0
        x1_str = []
        y1_str = []
        z1_str = []

        filex="test_"+ str(coil_num) + ".csv"

        #print(coil_num)
        print(filex)
        filename = open(filex, 'r')
        file = csv.DictReader(filename)

        for col in file:

        #count number of coils
            count=count+1
            print(count)

        #Read in values
            x1_str.append(col['x'])
            y1_str.append(col['y'])
            z1_str.append(col['z'])
  

        tot_point=count

        print(x1_str)
        count=0


        x = np.zeros(tot_point)
        y = np.zeros(tot_point)
        z = np.zeros(tot_point)
          #  print("tot_point",tot_point)
    # convert to correct type (integer/float) and create complete loop

        while count<= tot_point:
   
            if count<= tot_point-2: 
                x[count]=float(x1_str[count]) 
                y[count]=float(y1_str[count])
                z[count]=float(z1_str[count])

               #REORDER POINTS AS NECESSARY 

               # count=0

            if count<=tot_point-2:
                #print(count,x[count],y[count],z[count]) 
                point_count=point_count+1  
                print("coil:",coil_num, "point:",point_count)     
                print("Point(",point_count,") = {",x[count],",",y[count],",",z[count],", 1.0};",file=geo)
                print('//+',file=geo)
                line_num=point_count-1

                if count ==0: 
                     # print("NEW SURFACE LOOP")
                        #Remember start point of loop 
                        start_point = point_count 
                elif count == tot_point-2:
                    #Connect to previous point 
                    line_count=line_count+1
                    print("Line(",line_count,") = {",point_count-1,",",point_count,"};",file=geo)
                    print('//+',file=geo)
                    #Connect to start point 
                    line_count=line_count+1
                    print("Line(",line_count,") = {",point_count,",",start_point,"};",file=geo)
                    print('//+',file=geo)
                        #print(tot_point,line_num+1)
                else:
                    #Connect to previous point 
                    line_count=line_count+1
                    print("Line(",line_count,") = {",point_count-1,",",point_count,"};",file=geo)
                    print('//+',file=geo)

            count=count+1

        k=k+1

    coil_num=coil_num+1


