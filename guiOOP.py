from Tkinter import *
from ttk import *
import tkFileDialog
import tkMessageBox
import math
import literal_eval

SIGMA=5.8e7
MU0=4*math.pi*1e-7

class GUI(Frame):
  def __init__(self,root):
    Frame.__init__(self,root)

    root.title('Planar Magnetics Analyzing System (PMAS)')

    self.file_opt=options={}
    options['defaultextension']='.txt'
    options['filetypes']=[('all files','.*'),('text files','.txt')]
    options['initialdir']='C:\\'
    options['initialfile']='file.txt'
    options['parent']=root

    self.dir_opt=options={}
    options['initialdir']='C:\\'
    options['mustexist']=False
    options['parent']=root

    #initialize variables for GUI input
    self.f=StringVar() #switching frequency
    self.mur=StringVar() #relative permeability
    self.nlayer=StringVar() #number of layers
    self.h=StringVar() #layer thickness
    self.s=StringVar() #Spacing thickness
    self.w=StringVar() #window width
    self.m=StringVar() #turns per layer
    self.nwinding=StringVar() #number of windings
    self.wstyle=StringVar() #connection style of each winding
    self.lindex=StringVar() #layer indices
    self.g=StringVar() #core gap length
    self.Ae=StringVar() #effective gap area
    self.le=StringVar() #effective length
    self.nc=StringVar() #number of cores
    self.c=StringVar() #thickness of top and bottom ferrite

    #create variables for entry objects
    self.fentry=Entry(self)
    self.murentry=Entry(self)
    self.nlayerentry=Entry(self)
    self.hentry=Entry(self)
    self.sentry=Entry(self)
    self.wentry=Entry(self)
    self.mentry=Entry(self)
    self.nwindingentry=Entry(self)
    self.wstyleentry=Entry(self)
    self.lindexentry=Entry(self)
    self.gentry=Entry(self)
    self.Aeentry=Entry(self)
    self.leentry=Entry(self)
    self.ncentry=Entry(self)
    self.centry=Entry(self)

    self.createentries()

    #create dictionary of input values
    self.entries={}
    self.entries['f']=self.fentry
    self.entries['mur']=self.murentry
    self.entries['nlayer']=self.nlayerentry
    self.entries['h']=self.hentry
    self.entries['s']=self.sentry
    self.entries['w']=self.wentry
    self.entries['m']=self.mentry
    self.entries['nwinding']=self.nwindingentry
    self.entries['wstyle']=self.wstyleentry
    self.entries['lindex']=self.lindexentry
    self.entries['g']=self.gentry
    self.entries['Ae']=self.Aeentry
    self.entries['le']=self.leentry
    self.entries['nc']=self.ncentry
    self.entries['c']=self.centry

    self.geofilename='geometry.txt'
    self.netlistfilename='netlist.txt'

    #variables for getImpe function
    self.Ra=None
    self.La=None
    self.Rb=None
    self.Lb=None
    self.Ls=None
    self.Lfb=None
    self.Lft=None

    #call functions to display interface
    self.printlabels()
    self.entrygrid()
    self.createbuttons()

  def askopengeofilename(self):
    self.geofilename=tkFileDialog.askopenfilename(**self.file_opt)

  def asksaveasgeofilename(self):
    self.geofilename=tkFileDialog.asksaveasfilename(**self.file_opt)
  
  def asksaveasnetlistfilename(self):
    self.netlistfilename=tkFileDialog.asksaveasfilename(**self.file_opt)

  def savegeom(self):
    self.asksaveasgeofilename()
    f=open(self.geofilename,'w')
    for key in self.entries.keys():
      f.write(key + ' = ' + self.entries[key].get() + '\n')
    f.close()

  def loadgeom(self):
    self.askopengeofilename()
    f=open(self.geofilename,'r')
    for line in f:
      self.entries[line.split()[0]].insert(0,line.split()[2])
    f.close()

  def resetgeom(self):
    for key in self.entries.keys():
      self.entries[key].delete(0,END)
    
  def checkgeom(self):
    nwinding=int(self.nwinding.get()) 
    nlayer=int(self.nlayer.get())   

    if nwinding!= max(literal_eval(self.lindex.get())):
      tkMessageBox.showerror('NumofWinding and WindingIndex do not match')
    if nwinding!= len(literal_eval(self.wstyle.get())):
      tkMessageBox.showerror('NumofWinding and WindingStyle do not match')
    if nlayer!=len(literal_eval(self.h.get())):
      tkMessageBox.showerror('NumofLayer mismatch with h, please revise #layer or #h')
    if nlayer!=len(literal_eval(self.s.get())):
      tkMessageBox.showerror('NumofLayer mismatch with h\s, please revise #layer or #s')
    

  def printlabels(self):
    Label(self,text='Fundamental Frequency (kHz)').grid(column=0,row=1,sticky=W)
    Label(self,text='Relative Permeability').grid(column=0,row=2,sticky=W)
    Label(self,text='Number of Layers (nlayer)').grid(column=0,row=3,sticky=W)
    Label(self,text='Layer Thickness (h)').grid(column=0,row=4,sticky=W)
    Label(self,text='Spacing Thickness (s)').grid(column=0,row=5,sticky=W)
    Label(self,text='Window Width (w)').grid(column=0,row=6,sticky=W)
    Label(self,text='Number of Turns Each Layer (m)').grid(column=0,row=7,sticky=W)
    Label(self,text='Number of Windings (nwinding)').grid(column=0,row=8,sticky=W)
    Label(self,text='Connection Style of Each Winding (wstyle)').grid(column=0,row=9,sticky=W)
    Label(self,text='Belongings of Each Layer to Windings (lindex)').grid(column=0,row=10,sticky=W)
    Label(self,text='Core Gap Length (mm)').grid(column=0,row=11,sticky=W)
    Label(self,text='Effective Core Area (m^2)').grid(column=0,row=12,sticky=W)
    Label(self,text='Effective Length (m)').grid(column=0,row=13,sticky=W)
    Label(self,text='Number of Cores').grid(column=0,row=14,sticky=W)
    Label(self,text='Thickness of the Top and Bottom Core (m)').grid(column=0,row=15,sticky=W)

  def createentries(self):
    self.fentry=Entry(self,width=15,textvariable=self.f)
    self.murentry=Entry(self,width=15,textvariable=self.mur)
    self.nlayerentry=Entry(self,width=15,textvariable=self.nlayer)
    self.hentry=Entry(self,width=15,textvariable=self.h)
    self.sentry=Entry(self,width=15,textvariable=self.s)
    self.wentry=Entry(self,width=15,textvariable=self.w)
    self.mentry=Entry(self,width=15,textvariable=self.m)
    self.nwindingentry=Entry(self,width=15,textvariable=self.nwinding)
    self.wstyleentry=Entry(self,width=15,textvariable=self.wstyle)
    self.lindexentry=Entry(self,width=15,textvariable=self.lindex)
    self.gentry=Entry(self,width=15,textvariable=self.g)
    self.Aeentry=Entry(self,width=15,textvariable=self.Ae)
    self.leentry=Entry(self,width=15,textvariable=self.le)
    self.ncentry=Entry(self,width=15,textvariable=self.nc)
    self.centry=Entry(self,width=15,textvariable=self.c)

  def entrygrid(self):
    self.fentry.grid(column=1,row=1,sticky=(W,E),columnspan=2)
    self.murentry.grid(column=1,row=2,sticky=W,columnspan=2)
    self.nlayerentry.grid(column=1,row=3,sticky=W,columnspan=2)
    self.hentry.grid(column=1,row=4,sticky=W,columnspan=2)
    self.sentry.grid(column=1,row=5,sticky=W,columnspan=2)
    self.wentry.grid(column=1,row=6,sticky=W,columnspan=2)
    self.mentry.grid(column=1,row=7,sticky=W,columnspan=2)
    self.nwindingentry.grid(column=1,row=8,sticky=W,columnspan=2)
    self.wstyleentry.grid(column=1,row=9,sticky=W,columnspan=2)
    self.lindexentry.grid(column=1,row=10,sticky=W,columnspan=2)
    self.gentry.grid(column=1,row=11,sticky=W,columnspan=2)
    self.Aeentry.grid(column=1,row=12,sticky=W,columnspan=2)
    self.leentry.grid(column=1,row=13,sticky=W,columnspan=2)
    self.ncentry.grid(column=1,row=14,sticky=W,columnspan=2)
    self.centry.grid(column=1,row=15,sticky=W,columnspan=2)

  def createbuttons(self):
    Button(self,text='Load Geometry',command=self.loadgeom).grid(row=0,column=0)
    Button(self,text='Save Geometry',command=self.savegeom).grid(row=0,column=1)
    Button(self,text='Reset Geometry',command=self.resetgeom).grid(row=0,column=2)
    Button(self,text='Check Geometry Status',command=self.checkgeom).grid(row=16,columnspan=3)
    Button(self,text='Generate Netlist',command=self.generate_netlist).grid(row=18,columnspan=3)

  def getImpe(self):
    le=float(self.le.get())
    nc=float(self.nc.get())
    h=literal_eval(self.h.get())
    NumofLayer=int(self.nlayer.get())
    mur=float(self.mur.get())
    s=literal_eval(self.s.get())
    w=literal_eval(self.w.get())
    g=float(self.g.get())
    f=float(self.f.get())
    c=float(self.c.get())
    Ae=float(self.Ae.get())

    d=le*nc #effective length of the winding

    Xa=[]
    Xb=[]
    Xs=[]
    for i1 in range(NumofLayer):
      delta=(2/(f*2*math.pi)/MU0/SIGMA)**0.5
      Psi=complex(1/delta,1/delta)
      Z=Psi/SIGMA
      A=cmath.exp(-Psi*h[i1])
      Za=Z*(1-A)/(1+A)
      Zb=Z*2*A/(1-A**2)
      Xa.append(d/w[i1]*Za)
      Xb.append(d/w[i1]*Zb)
      Xs.append(complex(0,1)*(f*2*math.pi)*MU0*s[i1]*d/w[i1])

    #impedance for the ferrite core
    Xfb=complex(0,1)*(f*2*math.pi)*MU0*Ae/(g+Ae*w[i1]/(mur*c*d))
    Xft=complex(0,1)*(f*2*math.pi)*MU0*mur*c*d/w[i1]

    #calculate output
    self.Ra=numpy.array([e.real for e in Xa])
    self.La=numpy.array([e.imag for e in Xa])/(f*2*math.pi)
    self.Rb=numpy.array([e.real for e in Xb])
    self.Lb=numpy.array([e.imag for e in Xb])/(f*2*math.pi)
    self.Ls=numpy.array([e.imag for e in Xs])/(f*2*math.pi)
    self.Lfb=Xfb.imag/(f*2*math.pi)
    self.Lft=Xft.imag/(f*2*math.pi)

  def generate_netlist(self):

    self.asksaveasnetlistfilename()

    mur=float(self.mur.get())
    NumofLayer=int(self.nlayer.get())
    NumofWinding=int(self.nwinding.get())
    h=literal_eval(self.h.get())
    s=literal_eval(self.s.get())
    w=literal_eval(self.w.get())
    m=float(self.m.get())
    g=float(self.g.get())
    Ae=float(self.Ae.get())
    le=float(self.le.get())
    nc=int(self.nc.get())
    c=float(self.c.get())

    self.getImpe()

    #Repeat and summarizing the input information
    Serieslayers={}
    f=open(self.netlistfilename,'w')
    f.write('*Summary of the Transformer Structure in the I/O Ports')
    f.write('\n*There are {} Windings in total'.format(NumofWinding))
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

      f.write('\n*NetList for Layer {}'.format(index+1))
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
    


if __name__=='__main__':
  root=Tk()
  GUI(root).grid()
  root.mainloop()
