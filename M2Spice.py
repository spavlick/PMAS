from Tkinter import *
from Tkinter import Tk, Frame, BOTH
import tkFileDialog
import tkMessageBox
import math
import cmath
import numpy
import time
import Tkinter as tk
import ttk
import getpass
from ast import literal_eval
import sys,os

class GUI(Frame):
  def __init__(self,root):
    self.root=root
    Frame.__init__(self,self.root, background="white")

    self.root.title('Planar Magnetics to SPICE Netlist Converter - M2Spice - MIT Power Electronics Research Group')

    self.file_opt=options={}
    options['defaultextension']='.txt'
    options['filetypes']=[('all files','.*'),('text files','.txt')]
    #options['initialdir']='C:\\'
    options['initialfile']='file.txt'
    options['parent']=self.root

    self.dir_opt=options={}
    #options['initialdir']='C:\\'
    options['mustexist']=False
    options['parent']=self.root

    #initialize variables for GUI input

    self.f=StringVar()          #switching frequency
    self.mur=StringVar()        #relative permeability
    self.nlayer=StringVar()     #number of layers
    self.h=StringVar()          #layer thickness
    self.sigmac=StringVar()      #layer conductivity
    self.s=StringVar()          #spacing thickness
    self.mus=StringVar()	#spacing permeabilities
    self.w=StringVar()          #window width
    self.m=StringVar()          #turns per layer
    self.nwinding=StringVar()   #number of windings
    self.wstyle=StringVar()     #connection style of each winding
    self.lindex=StringVar()     #layer indices
    self.gt=StringVar()         #core gap length on the top side
    self.gb=StringVar()         #core gap length on the bottom side
    self.Ae=StringVar()         #effective gap area
    self.le=StringVar()         #effective length
    #self.nc=StringVar()         #number of cores
    self.c=StringVar()          #thickness of top and bottom ferrite

    #create variables for entry objects
    self.fentry=None
    self.murentry=None
    self.nlayerentry=None
    self.hentry=None
    self.sigmacentry=None
    self.sentry=None
    self.musentry=None
    self.wentry=None
    self.mentry=None
    self.nwindingentry=None
    self.wstyleentry=None
    self.lindexentry=None
    self.gtentry=None
    self.gbentry=None
    self.Aeentry=None
    self.leentry=None
    self.centry=None
    
    #create error messages
    self.errorMsg=StringVar()

    #call functions to display interface
    self.createbuttons()
    self.printlabels()
    self.createentries()

    #create dictionary of input values
    self.entries={}
    self.entries['f']=self.fentry
    self.entries['mur']=self.murentry
    self.entries['nlayer']=self.nlayerentry
    self.entries['h']=self.hentry
    self.entries['sigmac']=self.sigmacentry
    self.entries['s']=self.sentry
    self.entries['mus']=self.musentry
    self.entries['w']=self.wentry
    self.entries['m']=self.mentry
    self.entries['nwinding']=self.nwindingentry
    self.entries['wstyle']=self.wstyleentry
    self.entries['lindex']=self.lindexentry
    self.entries['gt']=self.gtentry
    self.entries['gb']=self.gbentry
    self.entries['Ae']=self.Aeentry
    self.entries['le']=self.leentry
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
    self.createbuttons()
    self.printlabels()
    self.centerWindow()
    
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
                                
        return os.path.join(base_path, relative_path)
  
    path1 = resource_path("multiwinding.gif")
    self.image1 = PhotoImage(file = path1)
    self.display = Label(self, image = self.image1, bg='white')
    self.display.grid(row=1,column=5, columnspan=1,rowspan=10,sticky=W+E+N+S)

    # always center the window in the middle of the screen
  def centerWindow(self):
    w = 1000
    h = 400
    sw = self.root.winfo_screenwidth()
    sh = self.root.winfo_screenheight()
    x = (sw - w)/2
    y = (sh - h)/2
    self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

  def OnFrameConfigure(self, event):
    '''Reset the scroll region to encompass the inner frame'''
    self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # ask for open geometry file name
  def askopengeofilename(self):
    self.geofilename=tkFileDialog.askopenfilename(**self.file_opt)

    # ask for save geometry file name
  def asksaveasgeofilename(self):
    self.geofilename=tkFileDialog.asksaveasfilename(**self.file_opt)
  
    # ask for save netlist file name
  def asksaveasnetlistfilename(self):
    self.netlistfilename=tkFileDialog.asksaveasfilename(**self.file_opt)

  def savegeom(self):
    try:
      self.asksaveasgeofilename()
      f=open(self.geofilename,'w')
      for key in self.entries.keys():
        f.write(key + ' = ' + self.entries[key].get() + '\n')
      f.close()
      tkMessageBox.showinfo(message='Geometry is successfully saved at:\n\n' + self.geofilename)
    except Exception as e:
      tkMessageBox.showerror(message='Geometry is not saved.\n System reported the following errors: \n\n' +e.message + '\n\nPlease check the geometry status.')

  def loadgeom(self):
    try:
      self.resetgeom()
      self.askopengeofilename()
      f=open(self.geofilename,'r')
      for line in f:
        self.entries[line.split()[0]].insert(0,line.split()[2])
      f.close()
      tkMessageBox.showinfo(message='Geometry is successfully loaded.\n Please check the geometry format ("Check Geometry").')
    except Exception as e:
      tkMessageBox.showerror(message='Geometry is not loaded.\n System reported the following errors: \n\n' +e.message + '\n\nPlease check the input file format.')


  def resetgeom(self):
    for key in self.entries.keys():
      self.entries[key].delete(0,END)
    
  def checkgeom(self):
    self.errorMsg=''
    self.errorCheck()


    # error format and value check
  def errorCheck(self):
    try:
      len(literal_eval(self.h.get()))
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid winding thickness (h), please enter a list of float values ("[" and "]" are required).'

    try:
      len(literal_eval(self.w.get()))
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid winding width (w), please enter a list of float values ("[" and "]" are required).'
      
    try:
      len(literal_eval(self.s.get()))
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid winding spacing (s), please enter a list of float values ("[" and "]" are required).'
      
    try:
      len(literal_eval(self.mus.get()))
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid spacing permeability (mus), please enter a list of float values ("[" and "]" are required).'
    
    try:
      len(literal_eval(self.m.get()))
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid number of turns on each layer (m), please enter a list of integer values ("[" and "]" are required).'
    
    try:
      len(literal_eval(self.wstyle.get()))
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid winding style (wstyle), please enter a list of integers ("[" and "]" are required).'
    
    try:
      len(literal_eval(self.lindex.get()))
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid layer belongings (lindex), please enter a list of integers ("[" and "]" are required).'
    
    try:
      len(literal_eval(self.sigmac.get()))
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid layer conductivity (sigmac), please enter a list of float values ("[" and "]" are required).'
      
      
      
    try:
      float(self.mur.get())
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid relative permeability (mur), please enter a float value.'
    try:
      int(self.nlayer.get())
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid total number of layers (nlayer), please enter an integer.'
    try:
      int(self.nwinding.get())
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid total number of windings (nwinding), please enter an integer.'
    try:
      float(self.gt.get())
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid top gap length (gt), please enter a float value.'
    try:
      float(self.gb.get())
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid bottom gap length (gb), please enter a float value.'
    try:
      float(self.Ae.get())
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid effective gap area (Ae), please enter a float value.'
    try:
      float(self.le.get())
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid effective core length (le), please enter a float value.'
    try:
      float(self.c.get())
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid top and bottom core thickness (c), please enter an integer.'

        # finished format check, start value check
    if self.errorMsg.strip()=='':
      nwinding=int(self.nwinding.get())
      nlayer=int(self.nlayer.get())
      if nwinding!= max(literal_eval(self.lindex.get())):
        self.errorMsg=self.errorMsg+'\n -- _nwinding_ mismatch with _lindex_, please check if length(lindex) == nwinding ?'
      if nwinding!= len(literal_eval(self.wstyle.get())):
        self.errorMsg=self.errorMsg+'\n -- _nwinding_ mismatch with _wstyle_, please check if length(wstyle) == nwinding ?'
      if nlayer!=len(literal_eval(self.h.get())):
        self.errorMsg=self.errorMsg+'\n -- _nlayer_ mismatch with _h_, please check if length(h) == nlayer ?'
      if nlayer!=len(literal_eval(self.sigmac.get())):
        self.errorMsg=self.errorMsg+'\n -- _nlayer_ mismatch with _sigmac_, please check if length(sigmac) == nlayer ?'
      if nlayer!=(len(literal_eval(self.s.get()))-1):
        self.errorMsg=self.errorMsg+'\n -- _nlayer_ mismatch with _s_, please check if length(s) == nlayer+1 ? \n There is always one more spacing than the number of conductive layers.'
      if nlayer!=(len(literal_eval(self.mus.get()))-1):
        self.errorMsg=self.errorMsg+'\n -- _nlayer_ mismatch with _mus_, please check if length(mus) == nlayer+1 ? \n There is always one more spacing than the number of conductive layers.'
      if nlayer!=len(literal_eval(self.w.get())):
        self.errorMsg=self.errorMsg+'\n -- _nlayer_ mismatch with _w_, please check if length(w) == nlayer ?'
      if nlayer!=len(literal_eval(self.lindex.get())):
        self.errorMsg=self.errorMsg+'\n -- _nlayer_ mismatch with _lindex_, please check if length(lindex) == nlayer ?'
      if nlayer!=len(literal_eval(self.m.get())):
        self.errorMsg=self.errorMsg+'\n -- _nlayer_ mismatch with _m_, please check if length(m) == nlayer ?'
      if self.errorMsg.strip()=='':
        tkMessageBox.showinfo('Congratulations', message='Geometry is correct, please continue.')
      else:
        tkMessageBox.showerror('Warnings', message='Find geometry errors:\n'+self.errorMsg)
    else:
      tkMessageBox.showerror('Warnings', message='Find geometry errors:\n'+self.errorMsg)


  def printlabels(self):
    Label(self,text='Analysis Frequency (f)',bg='white').grid(column=0,row=1,sticky=W)
    Label(self,text='Relative Permeability of the Core (mur)',bg='white').grid(column=0,row=2,sticky=W)
    Label(self,text='Total Number of Layers (nlayer)',bg='white').grid(column=0,row=3,sticky=W)
    Label(self,text='Layer Thickness (h)',bg='white').grid(column=0,row=4,sticky=W)
    Label(self,text='Layer Conductivities (sigmac)',bg='white').grid(column=0,row=5,sticky=W)
    Label(self,text='Spacing Thickness (s)',bg='white').grid(column=0,row=6,sticky=W)
    Label(self,text='Spacing Permeabilities (mus)',bg='white').grid(column=0,row=7,sticky=W)
    Label(self,text='Core Window Width (w)',bg='white').grid(column=0,row=8,sticky=W)
    Label(self,text='Number of Turns on Each Layer (m)',bg='white').grid(column=0,row=9,sticky=W)
    Label(self,text='Number of Windings (nwinding)',bg='white').grid(column=0,row=10,sticky=W)
    Label(self,text='Connection Style of Each Winding (wstyle)',bg='white').grid(column=0,row=11,sticky=W)
    Label(self,text='Belongings of Each Layer to Windings (lindex)',bg='white').grid(column=0,row=12,sticky=W)
    Label(self,text='Core Gap Length on the Top Side (gt)',bg='white').grid(column=0,row=13,sticky=W)
    Label(self,text='Core Gap Length on the Bottom Side (gb)',bg='white').grid(column=0,row=14,sticky=W)
    Label(self,text='Effective Core Area (Ac)',bg='white').grid(column=0,row=15,sticky=W)
    Label(self,text='Effective Winding Length per Turn (d)',bg='white').grid(column=0,row=16,sticky=W)
    Label(self,text='Thickness of the Top and Bottom Core (c)',bg='white').grid(column=0,row=17,sticky=W)
    Label(self,text='--------------------------------------------',bg='white').grid(column=5,row=13,columnspan=5)
    
    Label(self,text='Created and Maintained by:',bg='white').grid(column=5,row=14,columnspan=5)
    Label(self,text='S.A. Pavlick, M. Chen, and D.J. Perreault',bg='white').grid(column=5,row=15,columnspan=5)
    Label(self,text='MIT Power Electronics Research Group',bg='white').grid(column=5,row=16,columnspan=5)
    Label(self,text='v1.0, Feb 2015, All Rights Reserved',bg='white').grid(column=5,row=17,columnspan=5)
    
    
    Label(self,text='Geometry Reference Figures',bg='white').grid(column=5,row=0,columnspan=5)

    Label(self,text='Unit: Hz',bg='white').grid(column=3,row=1,sticky=W)
    Label(self,text='Unit: 1',bg='white').grid(column=3,row=2,sticky=W)
    Label(self,text='Unit: 1',bg='white').grid(column=3,row=3,sticky=W)
    Label(self,text='Unit: meters',bg='white').grid(column=3,row=4,sticky=W)
    Label(self,text='Unit: S/m',bg='white').grid(column=3,row=5,sticky=W)
    Label(self,text='Unit: meters',bg='white').grid(column=3,row=6,sticky=W)
    Label(self,text='Unit: H/m',bg='white').grid(column=3,row=7,sticky=W)
    Label(self,text='Unit: meters',bg='white').grid(column=3,row=8,sticky=W)
    Label(self,text='Unit: 1',bg='white').grid(column=3,row=9,sticky=W)
    Label(self,text='Unit: 1',bg='white').grid(column=3,row=10,sticky=W)
    Label(self,text='0=series, 1=parallel',bg='white').grid(column=3,row=11,sticky=W)
    Label(self,text='Winding index',bg='white').grid(column=3,row=12,sticky=W)
    Label(self,text='Unit: meters',bg='white').grid(column=3,row=13,sticky=W)
    Label(self,text='Unit: meters',bg='white').grid(column=3,row=14,sticky=W)
    Label(self,text='Unit: meter^2',bg='white').grid(column=3,row=15,sticky=W)
    Label(self,text='Unit: meters',bg='white').grid(column=3,row=16,sticky=W)
    Label(self,text='Unit: meters',bg='white').grid(column=3,row=17,sticky=W)
  

    Label(self,text='e.g.: 1e6',bg='white').grid(column=4,row=1,sticky=W)
    Label(self,text='e.g.: 1000',bg='white').grid(column=4,row=2,sticky=W)
    Label(self,text='e.g.: 4',bg='white').grid(column=4,row=3,sticky=W)
    Label(self,text='e.g.: [1e-3, 1e-3, 1e-3, 1e-3]',bg='white').grid(column=4,row=4,sticky=W)
    Label(self,text='e.g.: [5.8e7, 5.8e7, 5.8e7, 5.8e7]',bg='white').grid(column=4,row=5,sticky=W)
    Label(self,text='e.g.: [1e-3, 1e-3, 1e-3, 1e-3, 1e-3]',bg='white').grid(column=4,row=6,sticky=W)
    Label(self,text='e.g.: [1.26e-6, 1.26e-6, 1.26e-6, 1.26e-6, 1.26e-6]',bg='white').grid(column=4,row=7,sticky=W)
    Label(self,text='e.g.: [5e-3, 5e-3, 5e-3, 5e-3]',bg='white').grid(column=4,row=8,sticky=W)
    Label(self,text='e.g.: [1, 1, 2, 1]',bg='white').grid(column=4,row=9,sticky=W)
    Label(self,text='e.g.: 2',bg='white').grid(column=4,row=10,sticky=W)
    Label(self,text='e.g.: [0, 1]',bg='white').grid(column=4,row=11,sticky=W)
    Label(self,text='e.g.: [1, 2, 1, 2]',bg='white').grid(column=4,row=12,sticky=W)
    Label(self,text='e.g.: 1e-3',bg='white').grid(column=4,row=13,sticky=W)
    Label(self,text='e.g.: 1e-3',bg='white').grid(column=4,row=14,sticky=W)
    Label(self,text='e.g.: 60e-6',bg='white').grid(column=4,row=15,sticky=W)
    Label(self,text='e.g.: 2e-2',bg='white').grid(column=4,row=16,sticky=W)
    Label(self,text='e.g.: 1e-3',bg='white').grid(column=4,row=17,sticky=W)


  def createentries(self):
    self.fentry=Entry(self,textvariable=self.f,bg='yellow')
    self.murentry=Entry(self,textvariable=self.mur,bg='yellow')
    self.nlayerentry=Entry(self,textvariable=self.nlayer,bg='yellow')
    self.hentry=Entry(self,textvariable=self.h,bg='yellow')
    self.sigmacentry=Entry(self,textvariable=self.sigmac,bg='yellow')
    self.sentry=Entry(self,textvariable=self.s,bg='yellow')
    self.musentry=Entry(self,textvariable=self.mus,bg='yellow')
    self.wentry=Entry(self,textvariable=self.w,bg='yellow')
    self.mentry=Entry(self,textvariable=self.m,bg='yellow')
    self.nwindingentry=Entry(self,textvariable=self.nwinding,bg='yellow')
    self.wstyleentry=Entry(self,textvariable=self.wstyle,bg='yellow')
    self.lindexentry=Entry(self,textvariable=self.lindex,bg='yellow')
    self.gtentry=Entry(self,textvariable=self.gt,bg='yellow')
    self.gbentry=Entry(self,textvariable=self.gb,bg='yellow')
    self.Aeentry=Entry(self,textvariable=self.Ae,bg='yellow')
    self.leentry=Entry(self,textvariable=self.le,bg='yellow')
    self.centry=Entry(self,textvariable=self.c,bg='yellow')

    self.fentry.grid(column=1,row=1,sticky=(W,E))
    self.murentry.grid(column=1,row=2,sticky=(W,E))
    self.nlayerentry.grid(column=1,row=3,sticky=(W,E))
    self.hentry.grid(column=1,row=4,sticky=(W,E))
    self.sigmacentry.grid(column=1,row=5,sticky=(W,E))
    self.sentry.grid(column=1,row=6,sticky=(W,E))
    self.musentry.grid(column=1,row=7,sticky=(W,E))
    self.wentry.grid(column=1,row=8,sticky=(W,E))
    self.mentry.grid(column=1,row=9,sticky=(W,E))
    self.nwindingentry.grid(column=1,row=10,sticky=(W,E))
    self.wstyleentry.grid(column=1,row=11,sticky=(W,E))
    self.lindexentry.grid(column=1,row=12,sticky=(W,E))
    self.gtentry.grid(column=1,row=13,sticky=(W,E))
    self.gbentry.grid(column=1,row=14,sticky=(W,E))
    self.Aeentry.grid(column=1,row=15,sticky=(W,E))
    self.leentry.grid(column=1,row=16,sticky=(W,E))
    self.centry.grid(column=1,row=17,sticky=(W,E))

  def createbuttons(self):
    buttonframe=Frame(self, bg='white')
    Button(buttonframe, text='Load Geometry', command=self.loadgeom).pack(side=LEFT,padx=5)
    Button(buttonframe, text='Save Geometry', command=self.savegeom).pack(side=LEFT,padx=5)
    Button(buttonframe, text='Clear Geometry', command=self.resetgeom).pack(side=LEFT,padx=5)
    Button(buttonframe, text='Check Geometry', command=self.checkgeom).pack(side=LEFT,padx=5)
    Button(buttonframe, text='Generate Netlist',command=self.generate_netlist_errors).pack(side=LEFT,padx=5)
    buttonframe.grid(row=0, columnspan=5)

    #netlist_button.configure(command=self.generate_netlist_errors)

  def getImpe(self):
 
    le=float(self.le.get())
    h=literal_eval(self.h.get())
    NumofLayer=int(self.nlayer.get())
    sigmac=literal_eval(self.sigmac.get())
    mur=float(self.mur.get())
    s=literal_eval(self.s.get())
    mus=literal_eval(self.mus.get())
    w=literal_eval(self.w.get())
    gt=float(self.gt.get())
    gb=float(self.gb.get())
    f=float(self.f.get())
    c=float(self.c.get())
    Ae=float(self.Ae.get())

    d=le #effective length of the winding

    Xa=[]
    Xb=[]
    Xs=[]
    for i1 in range(NumofLayer):
      delta=(2/(f*2*math.pi)/mus[i1]/sigmac[i1])**0.5
      Psi=complex(1/delta,1/delta)
      Z=Psi/sigmac[i1]
      A=cmath.exp(-Psi*h[i1])
      Za=Z*(1-A)/(1+A)
      Zb=Z*2*A/(1-A**2)
      Xa.append(d/w[i1]*Za)
      Xb.append(d/w[i1]*Zb)
      Xs.append(complex(0,1)*(f*2*math.pi)*mus[i1+1]*s[i1+1]*d/w[i1])

    #impedance for the ferrite core
    Xfb=complex(0,1)*(f*2*math.pi)*4*math.pi*1e-7*Ae/(gt+Ae*w[i1]/(mur*c*d))
    Xft=complex(0,1)*(f*2*math.pi)*4*math.pi*1e-7*Ae/(gb+Ae*w[i1]/(mur*c*d))
    Xts=complex(0,1)*(f*2*math.pi)*mus[0]*s[0]*d/w[i1]

    #calculate output
    self.Ra=numpy.array([e.real for e in Xa])
    self.La=numpy.array([e.imag for e in Xa])/(f*2*math.pi)
    self.Rb=numpy.array([e.real for e in Xb])
    self.Lb=numpy.array([e.imag for e in Xb])/(f*2*math.pi)
    self.Ls=numpy.array([e.imag for e in Xs])/(f*2*math.pi)
    self.Lfb=Xfb.imag/(f*2*math.pi)
    self.Lft=Xft.imag/(f*2*math.pi)
    self.Lts=Xts.imag/(f*2*math.pi)

    #start generating netlist
  def generate_netlist(self):

    self.asksaveasnetlistfilename()

    sigmac=literal_eval(self.sigmac.get())
    mur=float(self.mur.get())
    NumofLayer=int(self.nlayer.get())
    NumofWinding=int(self.nwinding.get())
    h=literal_eval(self.h.get())
    s=literal_eval(self.s.get())
    mus=literal_eval(self.mus.get())
    w=literal_eval(self.w.get())
    m=literal_eval(self.m.get())
    WindingStyle=literal_eval(self.wstyle.get())
    WindingIndex=literal_eval(self.lindex.get())
    gt=float(self.gt.get())
    gb=float(self.gb.get())
    Ae=float(self.Ae.get())
    le=float(self.le.get())
    c=float(self.c.get())

    self.getImpe()


    Serieslayers={}
    #Repeat and summarizing the input information
    f=open(self.netlistfilename,'w')
    
    #Generate netlist identification information
    localtime = time.asctime( time.localtime(time.time()))
    user = getpass.getuser()
    f.write('\n******************************************************************')
    f.write('\n*        {0}    by {1}'.format(localtime,user))
    f.write('\n******************************************************************')
    
    #Start describing the transformer structure
    f.write('\n******************************************************************')
    f.write('\n******* Comprehensive  Summary of the Magnetic Structure  ********')
    f.write('\n******************************************************************')
    f.write('\n\n* This planar structure has {0} windings and {1} layers'.format(NumofWinding, NumofLayer))

    for index_winding in range(NumofWinding):
        #Parallel Connected
      if WindingStyle[index_winding]==1:
        f.write('\n\n* -> Winding {0} is Parallel Connected'.format(index_winding+1))
        totalturn=0
        for index_layer in range(NumofLayer):
          if WindingIndex[index_layer]==index_winding+1:
            f.write('\n* --> Includes Layer {}'.format(index_layer+1))
            f.write('\n* ---> thickness {}, width {}, turns {}, spacing above {:4.2f}m, spacing below {:4.2f}m'.format(h[index_layer], w[index_layer], m[index_layer], s[index_layer]*1e3, s[index_layer+1]*1e3))
            totalturn=totalturn+m[index_layer]
        f.write('\n* -> Winding {0} has {1} total turns; \n* --> External Port Name: PortP{0}, PortN{0}'.format(index_winding+1, totalturn))

    
        #Series Connected
      if WindingStyle[index_winding]==0:
        f.write('\n\n* -> Winding {0} is Series Connected;'.format(index_winding+1))
        numSeriesLayers=1
        totalturn=0
        for index_layer in range(NumofLayer):
          if WindingIndex[index_layer]==index_winding+1:
            f.write('\n* --> Includes Layer {}'.format(index_layer+1))
            f.write('\n* ---> thickness {}, width {}, turns {}, spacing above {:4.2f}m, spacing below {:4.2f}m'.format(h[index_layer], w[index_layer], m[index_layer], s[index_layer]*1e3, s[index_layer+1]*1e3))
            numSeriesLayers+=1
            totalturn=totalturn+m[index_layer]
        f.write('\n* -> Winding {0} has {1} total turns; \n* --> External Port Name: PortP{0}, PortN{0}'.format(index_winding+1, totalturn))

    f.write('\n******************************************************************\n')

    f.write('\n******************************************************************')
    f.write('\n*****                   Netlist Starts                    ********')
    f.write('\n******************************************************************')

    #Generate the SPICE netlist
    for index in range(NumofLayer):
      ra=self.Ra[index]
      la=self.La[index]
      rb=self.Rb[index]
      lb=self.Lb[index]
      ls=self.Ls[index]
      mx=m[index]

      f.write('\n\n*NetList for Layer {}'.format(index+1))
      f.write('\nLe{0} N{0} P{0} {1}'.format(index,mx**2))
      f.write('\nLi{0} G Md{0} {1}'.format(index,1))
      f.write('\nLg{0} Mg{0} Md{0} {1:14.2f}p'.format(index,lb*1e12))
      f.write('\nRg{0} Mc{0} Mg{0} {1:14.2f}m'.format(index,rb*1e3))
      f.write('\nRt{0} Mc{0} Mt{0} {1:14.2f}u'.format(index,ra*1e6))
      f.write('\nRb{0} Mb{0} Mc{0} {1:14.2f}u'.format(index,ra*1e6))
      f.write('\nLt{0} T{0} Mt{0} {1:14.2f}p'.format(index,la*1e12))
      f.write('\nLb{0} Mb{0} B{0} {1:14.2f}p'.format(index,la*1e12))
      f.write('\nLs{0} B{0} T{1} {2:14.2f}n'.format(index,index+1,ls*1e9))
      f.write('\nK{0} Le{0} Li{0} 1'.format(index))

    #Print the ferrite cores and top spacing
    f.write('\n\n*NetList for Top and Bottom Ferrites, as well as the First Spacing on Top Side')
    f.write('\nLft T0 G {:14.2f}u'.format(self.Lft*1e6))
    f.write('\nLfb T{} G {:14.2f}u'.format(NumofLayer+1,self.Lfb*1e6))
    f.write('\nLs0 T1 T0 {:14.2f}n'.format(self.Lts*1e9))

    #Print the external connections
    f.write('\n\n*NetList for Winding Interconnects')
    f.write('\n*A few 1n ohm resistors are used as short interconnects')

    #Create External Winding Ports
    for index_winding in range(NumofWinding):
      #Parallel Connected
      if WindingStyle[index_winding]==1:
        f.write('\n\n* -> Winding {} is Parallel Connected'.format(index_winding+1))
        for index_layer in range(NumofLayer):
          if WindingIndex[index_layer]==index_winding+1:
            f.write('\n* -->Include layer {}'.format(index_layer+1))
            f.write('\nRexP{0} PortP{1} P{0}    1n'.format(index_layer+1,index_winding+1))
            f.write('\nRexN{0} PortN{1} N{0}    1n'.format(index_layer+1,index_winding+1))


      #Series Connected
      if WindingStyle[index_winding]==0:
        f.write('\n\n* -> Winding {} is Series Connected'.format(index_winding+1))
        
        #identify which layers it contains
        numSeriesLayers=1
        for index_layer in range(NumofLayer):
          if WindingIndex[index_layer]==index_winding+1:
            f.write('\n* -->Include layer {}'.format(index_layer+1))
            Serieslayers[numSeriesLayers]=index_layer+1
            numSeriesLayers+=1
        #defining two wires from external port to the front and end layers
        f.write('\nRexP{0} PortP{1} P{0}    1n'.format(Serieslayers[1],index_winding+1))
        f.write('\nRexN{0} PortN{1} N{0}    1n'.format(Serieslayers[numSeriesLayers-1],index_winding+1))
        #defining the interconnects among series connected layers
        for index_SeriesLayers in range(numSeriesLayers-2):
          f.write('\nRexM{0} N{0} P{1}      1n'.format(Serieslayers[index_SeriesLayers+1],Serieslayers[index_SeriesLayers+2]))



    #netlist finalized
    f.write('\n******************************************************************')
    f.write('\n*****                   Netlist Ends                      ********')
    f.write('\n******************************************************************')
    f.close()
    tkMessageBox.showinfo(message='Successfully Generated Netlist')
  
  def generate_netlist_errors(self):
    try:
      self.generate_netlist()
    except Exception as e:
      tkMessageBox.showerror(message='Conversion Failed. System reported the following errors: \n\n' +e.message + '\n\nPlease check the geometry status again.')

class ScrollbarFrame(Frame):
  def __init__(self, root):
    Frame.__init__(self, root,height=400,width=1000)
    self.canvas = Canvas(root, borderwidth=0, bg='white')
    self.frame = GUI(root)
    self.hsb = Scrollbar(root, orient="horizontal", command=self.canvas.xview)
    self.vsb = Scrollbar(root, orient="vertical", command=self.canvas.yview)
    self.canvas.configure(xscrollcommand=self.hsb.set,yscrollcommand=self.vsb.set)

    self.vsb.pack(side="right", fill="y")
    self.hsb.pack(side="bottom",fill="x")
    self.canvas.pack(side="top", fill="both", expand=True)
    self.canvas.create_window((4,4),window=self.frame, anchor="nw", tags="self.frame")

    self.frame.bind("<Configure>", self.OnFrameConfigure)

  def OnFrameConfigure(self, event):
    '''Reset the scroll region to encompass the inner frame'''
    self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__=='__main__':
    
  root=Tk()
  mainframe=ScrollbarFrame(root)
  root.mainloop()
