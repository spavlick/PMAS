import math

#Set switching frequency
f=10e6

#Material Information
sigma=5.8e7
mu0=4*math.pi*1e-7
mur=1500

#Layer Information
NumofLayer=4
h=[0.0175e-3,0.0175e-3,0.0175e-3,0.0175e-3]
s=[0.787e-3,0.14e-3,0.787e-3,1.353e-3]
w=[5e-3,5e-3,5e-3,5e-3]
m=[1,1,1,1]

#Winding Information
NumofWinding=2
WindingIndex=[1,2,2,1]
WindingStyle=[0,1]

#Core Information
g=0
Ae=78.3*7e-6
le=240e-3
nc=1
c=2.5e-3

