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

coil_start = 2
coil_num = coil_start

coil_max =2
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

                   

                    #Connect points to other surfaces 
                    #If k=4 all other surface loops identified 
                    if k==4: 
                        
                        l=3 
                        while l >=0: 
                           # print(l)

                            if l==0: 
                                line_count=line_count+1 
                                print("Line(",line_count,") = {",(point_count-((l)*(tot_point-1))),",",(point_count-((3*(tot_point-1)))),"};",file=geo)
                                print('//+',file=geo)
                                #print(line_count,(point_count-((l)*(tot_point-1))),(point_count-((3*(tot_point-1)))))
                                l=l-1

                            else:
                                line_count=line_count+1 
                                print("Line(",line_count,") = {",(point_count-((l)*(tot_point-1))),",",(point_count-((l-1)*(tot_point-1))),"};",file=geo)
                                print('//+',file=geo)
                                #print(line_count,(point_count-((l)*(tot_point-1))),(point_count-((l-1)*(tot_point-1))))
                                l=l-1

                   # With all lines added, can now set the surfaces                                 
                    #print(point_count)
                count=count+1
        line_max_array[coil_num] = line_count
        #Step above complete, now set surfaces and volumes 

       # print("K:",k)
        if k==4: 

            count_2=int(line_max_array[coil_num-1]) +1
            print("coils ",coil_num,count_2)
            max_count = (count_2+tot_point-2)
            #print("COIL NUMBER :",coil_num)
            #print("TEST:",count_2,max_count)

            t1=count_2
            t4=count_2+(3*(tot_point-1)+3)
            t3=(count_2+(3*(tot_point-1)+4))
            t2=(count_2+(3*(tot_point-1)+8))
            curve_num=(2*count_2)-1

            l1=count_2
            l2=count_2+(3*(tot_point-1)+5)
            l3=(count_2+(1*(tot_point-1)))
            l4=(count_2+(3*(tot_point-1)))

            r1=count_2+(3*(tot_point-1)+4)
            r2=count_2+(3*(tot_point-1)+7)
            r3=(count_2+(2*(tot_point-1)))+1
            r4=(count_2+(3*(tot_point-1)))+2

            b1=count_2+(1*(tot_point-1))
            b2=count_2+(3*(tot_point-1)+6)
            b3=(count_2+(2*(tot_point-1)))
            b4=(count_2+(3*(tot_point-1)+1))

            curve_num=(2*count_2)-1
            curve_init[coil_num-coil_start]=(2*count_2)-1

            #print(curve_num,curve_init)

            #print("L values:") 
            # print(l1,l2,l3,l4)
            print("coil num: ",coil_num,"mod: ",(coil_num % 3))
            if((coil_num % 3) ==0) and ((coil_num %6) == 3): 
                print("problem coil - ignoring")
                max_count = 0 
            elif (coil_num % 4) ==0: 
                print("problem coil - ignoring")
                max_count = 0
 
            print("MAX COUNT: ",max_count)
            while count_2 <=max_count: 
 
                
               # print("CHECK: ", count_2,(count_2-max_count+tot_point-1-1))

                #Top surface 
               # print("MAX COUNT: ",max_count)
                if count_2 == max_count-1: 

                    tline1 = count_2
                    tline4=(1*(t4+((count_2-max_count+tot_point-1-1)*(5))))
                    tline3=(-1*(t3+((count_2-max_count+tot_point-1-1)*(5))))
                    tline2=(-1*(t2+((count_2-max_count+tot_point-1-1)*(5))))-1

                elif count_2 == max_count:

                    tline1 = count_2
                    tline4=(1*(t4+((count_2-max_count+tot_point-1-1)*(5))))+1
                    tline3=(-1*(t3+((count_2-max_count+tot_point-1-1)*(5))))+4
                    tline2=(-1*(t4))

                else:
                    tline1 = count_2
                    tline4=(1*(t4+((count_2-max_count+tot_point-1-1)*(5))))
                    tline3=(-1*(t3+((count_2-max_count+tot_point-1-1)*(5))))
                    tline2=(-1*(t2+((count_2-max_count+tot_point-1-1)*(5))))

                #print(line1,line2,line3,line4)

                print("Curve Loop(",curve_num,") = {",tline1,",",tline2,",",tline3,",",tline4,"};",file=geo)
                print('//+',file=geo)
                print("Surface(",curve_num,") = {",curve_num,"};",file=geo)
                print('//+',file=geo)
                curve_num=curve_num+2
                
                             
                #Left 

                if count_2 == max_count-1: 

                    lline1 = count_2
                    lline4=(-1*(l4+((count_2-max_count+tot_point-1-1)*(5))))
                    lline3=(-1*(l3+((count_2-max_count+tot_point-1-1)*(1))))
                    lline2=(1*(l2+((count_2-max_count+tot_point-1-1)*(5))))+1
                   # print(count_2,lline1,lline2,lline3,lline4)

                elif count_2 == max_count:

                    lline1 = count_2
                    lline4=(-1*(l4+((count_2-max_count+tot_point-1-1)*(5))))-1
                    lline3=(-1*(l3+((count_2-max_count+tot_point-1-1)*(1))))
                    lline2=(1*(l4))
                    #print(count_2,lline1,lline2,lline3,lline4)

                else:
                    
                    lline1 = count_2   
                    lline2=(1*(l2+((count_2-max_count+tot_point-1-1)*(5))))             
                    lline4=(-1*(l4+((count_2-max_count+tot_point-1-1)*(5))))
                    lline3=(-1*(l3+((count_2-max_count+tot_point-1-1)*(1))))           

                
                print("Curve Loop(",curve_num,") = {",lline1,",",lline2,",",lline3,",",lline4,"};",file=geo)
                print('//+',file=geo)
                print("Surface(",curve_num,") = {",curve_num,"};",file=geo)
                print('//+',file=geo)
                curve_num=curve_num+2


                #Right 
                if count_2 == max_count-1: 

                    rline1 = (1*(r1+((count_2-max_count+tot_point-1-1)*(5)))) 
                    rline2=(-1*(r2+((count_2-max_count+tot_point-1-1)*(5)))) -1            
                    rline4=(1*(r4+((count_2-max_count+tot_point-1-1)*(5))))
                    rline3=(-1*(r3+((count_2-max_count+tot_point-1-1)*(1))))+1
                   # print("Right: ",count_2,rline1,rline2,rline3,rline4)

                elif count_2 == max_count:

                    rline1 = (1*(r1+((count_2-max_count+tot_point-1-1)*(5)))) -4 
                    rline2=(-1*(r4))             
                    rline4=(1*(r4+((count_2-max_count+tot_point-1-1)*(5))))+1
                    rline3=(-1*(r3+((count_2-max_count+tot_point-1-1)*(1))))+1
                    #print("Right: ",count_2,rline1,rline2,rline3,rline4)

                else:
                    
                    rline1 = (1*(r1+((count_2-max_count+tot_point-1-1)*(5)))) 
                    rline2=(-1*(r2+((count_2-max_count+tot_point-1-1)*(5))))             
                    rline4=(1*(r4+((count_2-max_count+tot_point-1-1)*(5))))
                    rline3=(-1*(r3+((count_2-max_count+tot_point-1-1)*(1))))+1
                    #print("Right: ",count_2,rline1,rline2,rline3,rline4)


                if (max_count - count_2) >= 0:
                    print("Curve Loop(",curve_num,") = {",rline1,",",rline2,",",rline3,",",rline4,"};",file=geo)
                    print('//+',file=geo)
                    print("Surface(",curve_num,") = {",curve_num,"};",file=geo)
                    print('//+',file=geo)
                curve_num=curve_num+2

                #Bottom 
                if count_2 == max_count-1: 

                    bline1 = (1*(b1+((count_2-max_count+tot_point-1-1)*(1)))) 
                    bline2=(1*(b2+((count_2-max_count+tot_point-1-1)*(5)))) +1            
                    bline4=(-1*(b4+((count_2-max_count+tot_point-1-1)*(5))))
                    bline3=(-1*(b3+((count_2-max_count+tot_point-1-1)*(1))))
                    #print("Bottom: ",count_2,bline1,bline2,bline3,bline4)

                elif count_2 == max_count:

                    bline1 = (1*(b1+((count_2-max_count+tot_point-1-1)*(1)))) 
                    bline2=(1*(b4))             
                    bline4=(-1*(b4+((count_2-max_count+tot_point-1-1)*(5))))-1
                    bline3=(-1*(b3+((count_2-max_count+tot_point-1-1)*(1))))
                    #print("Bottom: ",count_2,bline1,bline2,bline3,bline4)

                else:
                    
                    bline1 = (1*(b1+((count_2-max_count+tot_point-1-1)*(1)))) 
                    bline2=(1*(b2+((count_2-max_count+tot_point-1-1)*(5))))             
                    bline4=(-1*(b4+((count_2-max_count+tot_point-1-1)*(5))))
                    bline3=(-1*(b3+((count_2-max_count+tot_point-1-1)*(1))))
                    #print("Bottom: ",count_2,bline1,bline2,bline3,bline4)

                if (max_count - count_2) == 0:

                    curve_final[coil_num-coil_start] = curve_num 

                if (max_count - count_2) >= 0:
                    print("Curve Loop(",curve_num,") = {",bline1,",",bline2,",",bline3,",",bline4,"};",file=geo)
                    print('//+',file=geo)
                    print("Surface(",curve_num,") = {",curve_num,"};",file=geo)
                    print('//+',file=geo)
                curve_num=curve_num+2

             
                #Front 
                #Back 

                count_2=count_2+1   

        k=k+1

  #  print(coil_num,curve_init,final_curve) 
    
    #SET VOLUME


    coil_num=coil_num+1


print("//+",file=geo)
print("Coherence;",file=geo)
print('//+',file=geo)
coil_num = coil_start
#coil_num = 10

while coil_num <= coil_max: 

    count_3 = curve_init[coil_num-coil_start]

    final_curve = curve_final[coil_num-coil_start]
    sl_num = 1 + (2*(coil_num-coil_start))
    #print(coil_num,sl_num,count_3,final_curve)

    string_sl="Surface Loop(" + str(sl_num) + ")= {"
    
    while count_3 <= final_curve:

        if count_3 ==final_curve: 

            string_sl=string_sl + str(int((count_3))) + "};"
            count_3 = count_3 + 2

        else:

            string_sl=string_sl + str(int((count_3))) + ", "
            count_3 = count_3 + 2

    print(string_sl,file=geo)
    print("//+",file=geo)
    print("Volume(",coil_num,") = {", sl_num,"};",file=geo) 
    print("//+",file=geo)

    coil_num=coil_num+1




