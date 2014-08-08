import math
from impedance import getImpe
from material-info import *

#Packaging Information into Cells
MaterialInfo=[sigma,mu0,mur]
WindingInfo=[NumofLayer,h,s,w,m]
CoreInfo=[g,Ae,le,nc,c]


#get the impedance matrix
ImpeValue=getImpe(f,MaterialInfo,WindingInfo,CoreInfo)
(Ra,La,Rb,Lb,Ls,Lfb,Lft)=ImpeValue

#Repeat and summarizing the input information
Serieslayers={}
f=open('netlist.txt','w')
f.write('Summary of the Transformer Structure in the I/O Ports')
f.write('\nThere are {} Windings in total'.format(NumofWinding))
for index_winding in range(NumofWinding):
  #Parallel Connected
  if WindingStyle[index_winding]==1:
    f.write('\n*Winding {0} is Parallel Connected with Winding Port PortP{0} and PortN{0}'.format(index_winding))
    for index_layer in range(NumofLayer):
      if WindingIndex[index_layer]==index_winding:
        f.write('\n*Include Layer {}, thickness {}, width {}, turns {}, spacing {}'.format(index_layer, h[index_layer], w[index_layer], m[index_layer], s[index_layer]))
        break
  if WindingStyle[index_winding]==0:
    f.write('\n*Winding {0} is Series Connected with Winding Port Port{0} and PortN{0}'.format(index_winding))
    numSeriesLayers=1
    for index_layer in range(NumofLayer):
      if WindingIndex[index_layer]==index_winding:
        f.write('\n*Include Layer {}, thickness {}, width {}, turns {}, spacing {}'.format(index_layer,h[index_layer],w[index_layer],m[index_layer],s[index_layer]))
        Serieslayers[numSeriesLayers]=index_layer+1 
        numSeriesLayers+=1

#Generate the SPICE netlist
for index in range(NumofLayer):
  ra=Ra[index]
  la=La[index]
  rb=Rb[index]
  lb=Lb[index]
  ls=Ls[index]
  mx=m[index]

  f.write('\n*NetList for Layer {}'.format(index))
  f.write('\nLe{0} N{0} P{0} {1}'.format(index,mx**2))
  f.write('\nLi{0} G Md{0} {1}'.format(index,1))
  f.write('\nLg{0} Mg{0} Md{0} {1:14.2f}p'.format(index,lb*1e12))
  f.write('\nRg{0} Mc{0} Mg{0} {1:14.2f}m'.format(index,rb*1e3))
  f.write('\nRt{0} Mc{0} Mt{0} {1:14.2f}u'.format(index,ra*1e6))
  f.write('\nRb{0} Mb{0} Mc{0} {1:14.2f}u'.format(index,ra*1e6))
  f.write('\nLt{0} T{0} Mt{0} {1:14.2f}p'.format(index,la*1e12))
  f.write('\nLb{0} Mb{0} B{0} {1:14.2f}p'.format(index,la*1e12))
  f.write('\nLs{0} B{0} T{1} {2:14.2f}p'.format(index,index+1,ls*1e12))
  f.write('\nK{0} Le{0} Li{0} 1'.format(index))

#Print the ferrite cores
f.write('\n*******************************')
f.write('\n*NetList for Top and Bottom Ferrites')
f.write('\nLft T1 G {:14.2f}u'.format(Lft*1e6))
f.write('\nLfb T{} G {:14.2f}u'.format(NumofLayer+1,Lfb*1e6))

#Print the external connections
f.write('\n**************************')
f.write('\n*Winding Connections')
f.write('\n*Using ZERO ohm resistors')

#Check if data is correct
if NumofWinding!=max(WindingIndex):
  f.write('\nNumofWinding and WindingIndex does not match')

if NumofWinding!=len(WindingStyle):
  f.write('\nNumofWinding and WindingStyle does not match')

#Create External Winding Ports
for index_winding in range(NumofWinding):
  #Parallel Connected
  if WindingStyle[index_winding]==1:
    f.write('\n*Winding {} is Parallel Connected'.format(index_winding+1))
    for index_layer in range(NumofLayer):
      if WindingIndex[index_layer]==index_winding+1:
        f.write('\n*Include layer {}'.format(index_layer+1))
        f.write('\nRexP{0} PortP{1} P{0} 1n'.format(index_layer+1,index_winding+1))
        f.write('\nRexN{0} PortN{1} N{0} 1n'.format(index_layer+1,index_winding+1))


  #Series Connected
  if WindingStyle[index_winding]==0:
    f.write('\n*Winding {} is Series Connected'.format(index_winding+1))
    
    #identify which layers it contains
    numSeriesLayers=1
    for index_layer in range(NumofLayer):
      if WindingIndex[index_layer]==index_winding+1:
        f.write('\n*Include layer {}'.format(index_layer+1))
        Serieslayers[numSeriesLayers]=index_layer+1
        numSeriesLayers+=1
    f.write('\nRexP{0} PortP{1} P{0} 1n'.format(Serieslayers[1],index_winding+1))
    f.write('\nRexN{0} PortN{1} N{0} 1n'.format(Serieslayers[numSeriesLayers-1],index_winding+1))
    for index_SeriesLayers in range(numSeriesLayers-2):
      f.write('\nRexM{0} N{0} P{1} 1n'.format(Serieslayers[index_SeriesLayers+1],Serieslayers[index_SeriesLayers+2]))

#netlist finalized
f.write('\n***************************')
f.write('\n*This is the END of the Netlist')
f.close()
