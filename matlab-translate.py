import math
from impedance import getImpe

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

#Packaging Information into Cells
MaterialInfo=[sigma,mu0,mur]
WindingInfo=[NumofLayer,h,s,w,m]
CoreInfo=[g,Ae,le,nc,c]


#get the impedance matrix
ImpeValue=getImpe(f,MaterialInfo,WindingInfo,CoreInfo)
(Ra,La,Rb,Lb,Ls,Lfb,Lft)=ImpeValue

#Repeat and summarizing the input information
f=open('netlist.txt','w')
f.write('Summary of the Transformer Structure in the I/O Ports'
f.write('There are %d Windings in total',NumofWinding)
for index_winding in range(NumofWinding):
  if WindingStyle[index_winding]==1:
    f.write('*Winding %d is Parallel Connected with Winding Port PortP%d and PortN%d',index_winding,index_winding,index_winding)
    for index_layer in range(NumofLayer):
      if WindingIndex[index_layer]==index_winding:
        f.write('*Include Layer %d, thickness %d, width %d, turns %d, spacing %d', index_layer, h[index_layer], w[index_layer], m[index_layer], s[index_layer]
        continue
  if WindingStyle[index_winding]==0:
    f.write('*Winding %d is Series Connected with Winding Port Port%d and PortN%d', index_winding, index_winding, index_winding)
    numSeriesLayers=1
    for index_layer in range(NumofLayer):
      if WindingIndex[index_layer]==index_winding:
        f.write('*Include Layer %d, thickness %d, width %d, turns %d, spacing %d',index_layer,h[index_layer],w[index_layer],m[index_layer],s[index_layer])
        Serieslayers[numSeriesLayers]=index_layer 

#find out how to initialize Serieslayers

        numSeriesLayers+=1

#Generate the SPICE netlist
for index in NumofLayer:
  ra=Ra[index]
  la=La[index]
  rb=Rb[index]
  lb=Lb[index]
  ls=Ls[index]
  mx=m[index]

  f.write('*NetList for Layer %d',index)
  f.write('Le%d N%d P%d %d', index,index,index,mx**2)
  f.write('Li%d G Md%d %d',index,index,1)
  f.write('Lg%d Mg%d Md%d %14.2f',index,index,index,lb*1e12)
  f.write('Rg%d Mc%d Mg%d %14.2f',index,index,index,rb*1e3)
  f.write('Rt%d Mc%d Mt%d %14.2f',index,index,index,ra*1e6)
  f.write('Rb%d Mb%d Mc%d %14.2f',index,index,index,ra*1e6)
  f.write('Lt%d T%d Mt%d %14.2f',index,index,index,la*1e12)
  f.write('Lb%d Mb%d B%d %14.2f',index,index,index,la*1e12)
  f.write('Ls%d B%d T%d %14.2f',index,index,index+1,ls*1e12)
  f.write('K%d Le%d Li%d 1',index,index,index)

#Print the ferrite cores
f.write('*******************************')
f.write('*NetList for Top and Bottom Ferrites')
f.write('Lft T1 G %14.2f',Lft*1e6)
f.write('Lfb T%d G %14.2f', NumofLayer+1,Lfb*1e6)

#Print the external connections
f.write('**************************')
f.write('*Winding Connections')
f.write('*Using ZERO ohm resistors')

#Check if data is correct
if NumOfWinding!=max(WindingIndex):
  f.write('NumofWinding and WindingIndex does not match')

if NumofWinding!=len(WindingStyle):
  f.write('NumofWinding and WindingStyle does not match')

#Create External Winding Ports
for index_winding in range(NumofWinding):
  #Parallel Connected
  if WindingStyle[index_winding]==1:
    f.write('*Winding %d is Parallel Connected',index_winding)
    for index_layer in range(NumofLayer):
      if WindingIndex[index_layer]==index_winding:
        f.write('*Include layer %d',index_layer)
        f.write('RexP%d PortP%d P%d ln',index_layer,index_winding,index_layer)
        f.write('RexN%d PortN%d N%d ln',index_layer,index_winding,index_layer)
        continue

  #Series Connected
  if WindingStyle[index_winding]==0:
    f.write('*Winding %d is Series Connected',index_winding)
    
    #identify which layers it contains
    numSeriesLayers=1
    for index_layer in NumofLayer:
      if WindingIndex[index_layer]==index_winding:
        f.write('*Include layer %d',index_layer)
        Serieslayers[numSeriesLayers]=index_layer
        numSeriesLayers+=1
    f.write('RexP%d PortP%d P%d ln',Serieslayers[1],index_winding,Serieslayers[1])
    f.write('RexN%d PortN%d N%d ln',Serieslayers[numSeriesLayers-1],index_winding,Serieslayers[numSeriesLayers-1]
    for index_SeriesLayers in range(numSeriesLayers-2):
      f.write('RexM%d N%d P%d ln',Serieslayers[index_SeriesLayers],Serieslayers[index_SeriesLayers],Serieslayers[index_SeriesLayers+1]

#netlist finalized
f.write('***************************')
f.write('*This is the END of the Netlist')
f.close()
