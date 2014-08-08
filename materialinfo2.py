import math

f=10e6

#Material Information;
sigma=5.8e7        #copper conductivity, S/m
mu0=4*math.pi*1e-7     #permeability of air and the FR4 material
mur=1500           #relative permeability of the ferrite material, H/m

#Layer Information;
NumofLayer=6                                           #number of layers
h=[0.0175e-3,0.0175e-3,0.0175e-3,0.0175e-3,0.0175e-3,0.0175e-3]           #Thickness of the conductor, from top to bottom, in meter
s=[0.787e-3,0.14e-3,0.787e-3,1.353e-3,0.787e-3,1.353e-3]                 #Spacings BELOW each layer, from top to bottom, in meter
w=[5e-3,5e-3,5e-3,5e-3,5e-3,5e-3]                        #Width of layers, from top to bottom, in meter
m=[1,1,1,1,2,3]                                           #Number of turns per layer, from top to bottom, in meter

#Winding Information;
NumofWinding=3 # a total of 3 windings
#Here layer 1 belongs to winding 4, layer 2 belongs to winding 1, etc...
WindingIndex=[1,2,2,1,3,3]    #1=winding group 1; 2=winding group 2;
#Winding group style, here winding group 1,2,3 are in series, and winding
#group 4,5 are in parallel. 
WindingStyle=[0,1,1]        
##############################################################

#Core Information;
g=0         #length of the core gap, m
Ae=78.3*7e-6         #effective gap area, m2
le=240e-3         #effective length, m
nc=1              #number of cores;
c=2.5e-3            #Thickness of the top and bottom ferrite
