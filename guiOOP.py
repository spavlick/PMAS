from Tkinter import *
from ttk import *
import tkFileDialog

class GUI(Frame):
  def __init__(self,root):
    Frame.__init__(self,root)

    root.title('Planar Magnetics Analyzing System (PMAS)')

    self.file_opt=options={}
    options['defaultextension']='.txt'
    options['filetypes']=[('all files','.*'),('text files','.txt')]
    options['initialdir']='C:\\'
    options['initialfile']='geometry.txt'
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
    self.fentry=None
    self.murentry=None
    self.nlayerentry=None
    self.hentry=None
    self.sentry=None
    self.wentry=None
    self.mentry=None
    self.nwindingentry=None
    self.wstyleentry=None
    self.lindexentry=None
    self.gentry=None
    self.Aeentry=None
    self.leentry=None
    self.ncentry=None
    self.centry=None

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

    #call functions to display interface
    self.printlabels()
    self.createentries()
    self.entrygrid()
    self.createbuttons()

  def askopenfilename(self):
    self.geofilename=tkFileDialog.askopenfilename(**self.file_opt)

  def asksaveasfilename(self):
    self.geofilename=tkFileDialog.asksaveasfilename(**self.file_opt)

  def savegeom(self):
    self.asksaveasfilename()
    f=open(self.geofilename,'w')
    for key in self.entries.keys():
      f.write(key + ' = ' + self.entries[key].get() + '\n')
    f.close()

  def loadgeom(self):
    self.askopenfilename()
    f=open(self.geofilename,'r')
    for line in f:
      self.entries[line.split()[0]]=line.split()[2]
    f.close()
    
  
    

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
    Button(self,text='Reset Geometry').grid(row=0,column=2)
    Button(self,text='Check Geometry Status').grid(row=16,columnspan=3)
    Button(self,text='Generate Netlist').grid(row=18,columnspan=3)

  


if __name__=='__main__':
  root=Tk()
  GUI(root).pack()
  root.mainloop()
