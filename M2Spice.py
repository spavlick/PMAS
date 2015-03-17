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
import ScrolledText as tkst
import tkFont

class GUI(Frame):
  def __init__(self,root):
    self.root=root
    Frame.__init__(self,self.root, background="white")

    self.root.title('M2Spice - Planar Magnetics to SPICE Netlist Conversion Tool')

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
    self.sigmac=StringVar()     #layer conductivity
    self.s=StringVar()          #spacing thickness
    self.mus=StringVar()        #spacing permeabilities
    self.w=StringVar()          #window width
    self.m=StringVar()          #turns per layer
    self.nwinding=StringVar()   #number of windings
    self.wstyle=StringVar()     #connection style of each winding
    self.lindex=StringVar()     #layer indices
    self.gt=StringVar()         #core gap length on the top side
    self.gb=StringVar()         #core gap length on the bottom side
    self.Ac=StringVar()         #effective gap area
    self.d=StringVar()          #effective length
    self.c=StringVar()          #thickness of top and bottom ferrite
    self.x=StringVar()          #define the subcircuit name x    

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
    self.Acentry=None
    self.dentry=None
    self.centry=None
    self.xentry=None
    
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
    self.entries['Ac']=self.Acentry
    self.entries['d']=self.dentry
    self.entries['c']=self.centry
    self.entries['x']=self.xentry

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

    # always center the window in the middle of the screen
  def centerWindow(self):
    sw = self.root.winfo_screenwidth()
    sh = self.root.winfo_screenheight()
    w = int(sw*0.75)
    h = int(sh*0.6)
    x = (sw - w)/2
    y = (sh - h)/2
    self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

  def OnFrameConfigure(self, event):
    '''Reset the scroll region to encompass the inner frame'''
    self.canvas.configure(scrollregion=self.canvas.bbox("all"))
  
  def designref(self):
    img = tk.Toplevel(self)
    img.title("M2Spice - Design Reference")
    
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
  
    path1 = resource_path("multiwinding.gif")
    img.image1 = PhotoImage(file = path1)
    img.display = Label(img, image = img.image1, bg='white')
    img.display.grid(row=0,column=0, columnspan=6,rowspan=12,sticky=W+E+N+S)
    sw = self.root.winfo_screenwidth()
    sh = self.root.winfo_screenheight()
    w = int(sw*0.38)
    h = int(sh*0.6)
    x = sw-w
    y = 0
    img.geometry('%dx%d+%d+%d' % (w, h, x, y))
  

    # ask for open geometry file name
  def askopengeofilename(self):
    self.geofilename=tkFileDialog.askopenfilename(**self.file_opt)

    # ask for save geometry file name
  def asksaveasgeofilename(self):
    self.geofilename=tkFileDialog.asksaveasfilename(**self.file_opt)
  
    # ask for save netlist file name
  def asksaveasnetlistfilename(self):
    self.netlistfilename=tkFileDialog.asksaveasfilename(**self.file_opt)
  
  def askopennetlistfilename(self):
    self.netlistfilename=tkFileDialog.askopenfilename(**self.file_opt)

  def savegeom(self):
    try:
      self.asksaveasgeofilename()
      if self.geofilename:
        f=open(self.geofilename,'w')
        for key in self.entries.keys():
          f.write(key + ' = ' + self.entries[key].get() + '\n')
        f.close()
        tkMessageBox.showinfo('M2Spice - Save Geometry - Saved', message='Successfully saved geometry to:\n\n' + self.geofilename)
    except Exception as e:
      tkMessageBox.showerror('M2Spice - Save Geometry - Failed', message='Failed to save geometry.\n\nSystem reported the following errors: \n\n' +e.message + '\n\nPossible reasons: 1. invalid saving address; 2. invalid geometry format.' + '\n\nPlease check the saving address and geometry format.')

  def resetgeom(self):
    cleartag = tkMessageBox.askyesno('M2Spice - Clear Geometry', message='Do you really want to clear the geometry information? All unsaved data will be lost.')
    if cleartag==True:
        for key in self.entries.keys():
            self.entries[key].delete(0,END)

  def loadgeom(self):
    loadvar=""
    try:
      self.askopengeofilename()
      if self.geofilename:
        for key in self.entries.keys(): #clear up
            self.entries[key].delete(0,END)
        f=open(self.geofilename,'r')
        for line in f:
            line_cell=line.split()
            if (len(line_cell)>=3):
                self.entries[line.split()[0]].insert(0,line.split(None,2)[2])
                loadvar = loadvar + line.split()[0] + ', '
        f.close()
        if (len(loadvar.split())==18):
            tkMessageBox.showinfo('M2Spice - Load Geometry - Loaded', message='Successfully loaded all parameters. Please double check the geometry format in the GUI, then click "Check Geometry").')
        else:
            tkMessageBox.showinfo('M2Spice - Load Geometry - Partially Loaded', message='Some parameters are missing. Please double check the geometry format.')
    except Exception as e:
      tkMessageBox.showerror('M2Spice - Load Geometry - Failed', message='Failed to load geometry.\n\nSystem reported the following errors: \n\n' +e.message + '\n\nPossible reasons: 1. invalid loading address; 2.invalid geometry format.' + '\n\nPlease check the loading address and geometry format.')


  def editgeom(self):
    geoinfo=""
    for key in self.entries.keys():
        geoinfo = geoinfo + key + ' = ' + self.entries[key].get() + '\n'
    editor = tk.Toplevel(self, bg='white', width=550,height=500)
    editor.title("M2Spice - Geometry Editor")
    
    #overall frame position
    editorarea = tk.Frame(editor ,height=100,width=50,bg='white',borderwidth=1)
    editorscrollbar=tk.Scrollbar(editorarea)
    
    #size of the scrollbar
    editArea=tk.Text(editorarea, width=70, height=30, wrap="word", yscrollcommand=editorscrollbar.set)
    editorscrollbar.config(command=editArea.yview)
    editorscrollbar.pack(side="right",fill="y")
    editArea.pack(side="left",fill="both",expand=True)
    
    #position of the editorial area
    editorarea.place(x=20,y=40)
    
    sw = editor.winfo_screenwidth()
    sh = editor.winfo_screenheight()
    w = int(sw*0.4)
    h = int(sh*0.6)
    x = 0
    y = 0
    editor.geometry('%dx%d+%d+%d' % (w, h, x, y))

    #Write in the current geometry information
    editArea.insert(tk.INSERT,geoinfo)

    def askopengeofilename():
        self.geofilename=tkFileDialog.askopenfilename(**self.file_opt)
        
    # ask for save geometry file name
    def asksaveasgeofilename():
        self.geofilename=tkFileDialog.asksaveasfilename(**self.file_opt)
    
    def reseteditgeom():
        cleartag = tkMessageBox.askyesno('M2Spice - Clear Geometry', message='Do you really want to clear the geometry information? All unsaved data will be lost.')
        editor.lift()
        if cleartag==True:
            editArea.delete(1.0, END)
            

    def loadeditgeom():
        try:
            askopengeofilename()
            if self.geofilename:
                editArea.delete(1.0, END) #clear up
                f=open(self.geofilename,'r')
                netlist=f.read()
                editArea.insert(tk.INSERT,netlist)
                f.close()
                editor.lift()
        except Exception as e:
                tkMessageBox.showerror('M2Spice - Load Geometry - Failed', message='Failed to load geometry.\n\nSystem reported the following errors: \n\n' +e.message + '\n\nPossible reasons: 1. invalid loading address; 2.invalid geometry format.' + '\n\nPlease check the loading address and geometry format.')

    def saveeditgeom():
        geoinfo=""
        try:
            asksaveasgeofilename()
            if self.geofilename:
                geoinfo = editArea.get(1.0,'end-1c')
                geoinfo = os.linesep.join([s for s in geoinfo.splitlines() if s])
                f=open(self.geofilename,'w')
                f.write(geoinfo)
                f.close()
                tkMessageBox.showinfo('M2Spice - Save Geometry - Saved', message='Successfully saved geometry to:\n\n' + self.geofilename)
                editor.lift()
        except Exception as e:
            tkMessageBox.showerror('M2Spice - Save Geometry - Failed', message='Failed to save geometry.\n\nSystem reported the following errors: \n\n' +e.message + '\n\nPossible reasons: 1. invalid saving address; 2. invalid geometry format.' + '\n\nPlease check the saving address and geometry format.')

    def forwardeditgeom():
        geoinfo=""
        fwdvar="" #forwarded variable
        try:
            for key in self.entries.keys():
                self.entries[key].delete(0,END) #clear up
            geoinfo = editArea.get(1.0,'end-1c')
            geoinfo = os.linesep.join([s for s in geoinfo.splitlines() if s])
            for line in geoinfo.splitlines():
                line_cell=line.split()
                if (len(line_cell)>=3):
                    self.entries[line.split()[0]].insert(0,line.split(None,2)[2])
                    fwdvar = fwdvar + line.split()[0] + ', '
            if (len(fwdvar.split())==17):
                tkMessageBox.showinfo('M2Spice - Forward Geometry - Forwarded', message='Successfully forwarded all parameters to the GUI. Please double check the geometry format in the GUI, then click "Check Geometry".')
                editor.lower()
            else:
                tkMessageBox.showinfo('M2Spice - Forward Geometry - Partially Forwarded', message='Some parameters are missing. Please double check the geometry format.')
        except Exception as e:
            tkMessageBox.showerror('M2Spice - Forward Geometry - Failed', message='Failed to forward geometry.\n\nSystem reported the following errors: \n\n' +e.message + '\n\nPossible reasons: 1. invalid loading address; 2.invalid geometry format.' + '\n\nPlease check the loading address and geometry format.')

    custom = tkFont.Font(family="Helvetica",size=12,weight="bold")
    
    buttonframe=Frame(editor, bg='white', height=3)
    Button(buttonframe, text='Load Geometry', command=loadeditgeom).pack(side=LEFT,padx=5,pady=5)
    Button(buttonframe, text='Save Geometry', command=saveeditgeom).pack(side=LEFT,padx=5,pady=5)
    Button(buttonframe, text='Clear Geometry', command=reseteditgeom).pack(side=LEFT,padx=5,pady=5)
    Button(buttonframe, text='Forward Geometry', command=forwardeditgeom).pack(side=LEFT,padx=5,pady=5)
    buttonframe.grid(row=0, columnspan=1)
               
  def viewnetlist(self):
    try:
      self.askopennetlistfilename()
      if self.netlistfilename:
        f=open(self.netlistfilename,'r')
        netlist=f.read()
        viewer = tk.Toplevel(self, bg='white', width=700,height=500)
        viewer.title("M2Spice - Netlist Viewer")
        viewarea = tk.Frame(viewer,height=100,width=50,bg='white',borderwidth=1)
        viewscrollbar=tk.Scrollbar(viewarea)
        editArea=tk.Text(viewarea,width=100,height=30,wrap="word",yscrollcommand=viewscrollbar.set,borderwidth=0,highlightthickness=0)
        viewscrollbar.config(command=editArea.yview)
        viewscrollbar.pack(side="right",fill="y")
        editArea.pack(side="left",fill="both",expand=True)
        editArea.insert(tk.INSERT,netlist)
        viewarea.place(x=20,y=20)
        sw = viewer.winfo_screenwidth()
        sh = viewer.winfo_screenheight()
        w = int(sw*0.6)
        h = int(sh*0.6)
        x = w/2
        y = h/2
        viewer.geometry('%dx%d+%d+%d' % (w, h, x, y))
    except Exception as e:
      tkMessageBox.showerror('M2Spice - Netlist Viewer - Failed', message='Failed to open netlist.\n\nSystem reported the following errors: \n\n' +e.message + '\n\nPossible reasons: 1. invalid netlist address; 2.invalid netlist file.' + '\n\nPlease check the netlist address and netlist file.')
    
  def checkgeom(self):
    self.errorMsg=''
    self.errorNum=0
    self.errorCheck()


    # error format and value check
  def errorCheck(self):
    try:
      len(literal_eval(self.h.get()))
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid winding thickness (h), please enter a list of float values (please include "[" and "]").'
      self.errorNum=self.errorNum+1
    try:
      len(literal_eval(self.w.get()))
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid winding width (w), please enter a list of float values (please include "[" and "]").'
      self.errorNum=self.errorNum+1
    try:
      len(literal_eval(self.s.get()))
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid winding spacing (s), please enter a list of float values (please include "[" and "]").'
      self.errorNum=self.errorNum+1
    try:
      len(literal_eval(self.mus.get()))
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid spacing permeability (mus), please enter a list of float values (please include "[" and "]").'
      self.errorNum=self.errorNum+1
    try:
      len(literal_eval(self.m.get()))
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid number of turns on each layer (m), please enter a list of integer values (please include "[" and "]").'
      self.errorNum=self.errorNum+1
    try:
      len(literal_eval(self.wstyle.get()))
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid winding style (wstyle), please enter a list of integers (please include "[" and "]").'
      self.errorNum=self.errorNum+1
    try:
      len(literal_eval(self.lindex.get()))
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid layer belongings (lindex), please enter a list of integers (please include "[" and "]").'
      self.errorNum=self.errorNum+1
    try:
      len(literal_eval(self.sigmac.get()))
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid layer conductivity (sigmac), please enter a list of float values (please include "[" and "]").'
      self.errorNum=self.errorNum+1
    try:
      float(self.mur.get())
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid relative permeability (mur), please enter a float value (no "[" or "]").'
      self.errorNum=self.errorNum+1
    try:
      int(self.nlayer.get())
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid total number of layers (nlayer), please enter an integer (no "[" or "]").'
      self.errorNum=self.errorNum+1
    try:
      int(self.nwinding.get())
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid total number of windings (nwinding), please enter an integer (no "[" or "]").'
      self.errorNum=self.errorNum+1
    try:
      float(self.gt.get())
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid top gap length (gt), please enter a float value (no "[" or "]").'
      self.errorNum=self.errorNum+1
    try:
      float(self.gb.get())
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid bottom gap length (gb), please enter a float value (no "[" or "]").'
      self.errorNum=self.errorNum+1
    try:
      float(self.Ac.get())
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid effective core gap area (Ac), please enter a float value (no "[" or "]").'
      self.errorNum=self.errorNum+1
    try:
      float(self.d.get())
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid effective core length (d), please enter a float value (no "[" or "]").'
      self.errorNum=self.errorNum+1
    try:
      float(self.c.get())
    except Exception:
      self.errorMsg=self.errorMsg+'\n -- invalid top and bottom core thickness (c), please enter an integer (no "[" or "]").'
      self.errorNum=self.errorNum+1

        # finished format check, start value check
    if self.errorMsg.strip()=='':
      nwinding=int(self.nwinding.get())
      nlayer=int(self.nlayer.get())
      if nwinding!= max(literal_eval(self.lindex.get())):
        self.errorMsg=self.errorMsg+'\n -- _nwinding_ mismatch with _lindex_, please check if list.length(lindex) equals _nwinding_ ?'
        self.errorNum=self.errorNum+1
      if nwinding!= len(literal_eval(self.wstyle.get())):
        self.errorMsg=self.errorMsg+'\n -- _nwinding_ mismatch with _wstyle_, please check if list.length(wstyle) equals _nwinding_ ?'
        self.errorNum=self.errorNum+1
      if nlayer!=len(literal_eval(self.h.get())):
        self.errorMsg=self.errorMsg+'\n -- _nlayer_ mismatch with _h_, please check if list.length(h) equals _nlayer_ ?'
        self.errorNum=self.errorNum+1
      if nlayer!=len(literal_eval(self.sigmac.get())):
        self.errorMsg=self.errorMsg+'\n -- _nlayer_ mismatch with _sigmac_, please check if list.length(sigmac) equals _nlayer_ ?'
        self.errorNum=self.errorNum+1
      if nlayer!=(len(literal_eval(self.s.get()))-1):
        self.errorMsg=self.errorMsg+'\n -- _nlayer_ mismatch with _s_, please check if list.length(s) equals _nlayer+1_ ? There is always one more spacing than the number of conductive layers.'
        self.errorNum=self.errorNum+1
      if nlayer!=(len(literal_eval(self.mus.get()))-1):
        self.errorMsg=self.errorMsg+'\n -- _nlayer_ mismatch with _mus_, please check if list.length(mus) equals _nlayer+1_ ? There is always one more spacing than the number of conductive layers.'
        self.errorNum=self.errorNum+1
      if nlayer!=len(literal_eval(self.w.get())):
        self.errorMsg=self.errorMsg+'\n -- _nlayer_ mismatch with _w_, please check if list.length(w) equals _nlayer_ ?'
        self.errorNum=self.errorNum+1
      if nlayer!=len(literal_eval(self.lindex.get())):
        self.errorMsg=self.errorMsg+'\n -- _nlayer_ mismatch with _lindex_, please check if list.length(lindex) equals _nlayer_ ?'
        self.errorNum=self.errorNum+1
      if nlayer!=len(literal_eval(self.m.get())):
        self.errorMsg=self.errorMsg+'\n -- _nlayer_ mismatch with _m_, please check if list.length(m) equals _nlayer_ ?'
        self.errorNum=self.errorNum+1
      if self.errorMsg.strip()=='':
        tkMessageBox.showinfo('M2Spice - Check Geometry - Passed', message='Good! Geometry is correct! \n\nNow you can generate the netlist by clicking "Generate Netlist".')
        self.errorNum=self.errorNum+1
      else:
        tkMessageBox.showerror('M2Spice - Check Geometry - Failed', message='Find ' + str(self.errorNum) +' geometry errors:\n' + self.errorMsg)
    else:
      tkMessageBox.showerror('M2Spice - Check Geometry - Failed', message='Find ' + str(self.errorNum) + ' geometry errors:\n'+ self.errorMsg)


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
    Label(self,text='Name of the Component (x)',bg='white').grid(column=0,row=18,sticky=W)
    
    Label(self,text='*'*20,bg='white').grid(column=0,row=19,columnspan=6)
    Label(self,text='S.A. Pavlick, M. Chen, and D.J. Perreault',bg='white').grid(column=0,row=20,columnspan=6)
    Label(self,text='MIT Power Electronics Research Group',bg='white').grid(column=0,row=21,columnspan=6)
    Label(self,text='v1.0, Feb 2015',bg='white').grid(column=0,row=22,columnspan=6)
    Label(self,text='*'*20,bg='white').grid(column=0,row=23,columnspan=6)

    Label(self,text='Unit: Hz',bg='white').grid(column=4,row=1,sticky=W)
    Label(self,text='Unit: 1',bg='white').grid(column=4,row=2,sticky=W)
    Label(self,text='Unit: 1',bg='white').grid(column=4,row=3,sticky=W)
    Label(self,text='Unit: meters',bg='white').grid(column=4,row=4,sticky=W)
    Label(self,text='Unit: S/m',bg='white').grid(column=4,row=5,sticky=W)
    Label(self,text='Unit: meters',bg='white').grid(column=4,row=6,sticky=W)
    Label(self,text='Unit: H/m',bg='white').grid(column=4,row=7,sticky=W)
    Label(self,text='Unit: meters',bg='white').grid(column=4,row=8,sticky=W)
    Label(self,text='Unit: 1',bg='white').grid(column=4,row=9,sticky=W)
    Label(self,text='Unit: 1',bg='white').grid(column=4,row=10,sticky=W)
    Label(self,text='0=series, 1=parallel',bg='white').grid(column=4,row=11,sticky=W)
    Label(self,text='Winding index',bg='white').grid(column=4,row=12,sticky=W)
    Label(self,text='Unit: meters',bg='white').grid(column=4,row=13,sticky=W)
    Label(self,text='Unit: meters',bg='white').grid(column=4,row=14,sticky=W)
    Label(self,text='Unit: meter^2',bg='white').grid(column=4,row=15,sticky=W)
    Label(self,text='Unit: meters',bg='white').grid(column=4,row=16,sticky=W)
    Label(self,text='Unit: meters',bg='white').grid(column=4,row=17,sticky=W)
    Label(self,text='blank, or one letter',bg='white').grid(column=4,row=18,sticky=W)

    Label(self,text='e.g.: 1e6',bg='white').grid(column=5,row=1,sticky=W)
    Label(self,text='e.g.: 1000',bg='white').grid(column=5,row=2,sticky=W)
    Label(self,text='e.g.: 4',bg='white').grid(column=5,row=3,sticky=W)
    Label(self,text='e.g.: [1e-3, 1e-3, 1e-3, 1e-3]',bg='white').grid(column=5,row=4,sticky=W)
    Label(self,text='e.g.: [6e7, 6e7, 6e7, 6e7]',bg='white').grid(column=5,row=5,sticky=W)
    Label(self,text='e.g.: [1e-3, 1e-3, 1e-3, 1e-3, 1e-3]',bg='white').grid(column=5,row=6,sticky=W)
    Label(self,text='e.g.: [1e-6, 1e-6, 1e-6, 1e-6, 1e-6]',bg='white').grid(column=5,row=7,sticky=W)
    Label(self,text='e.g.: [5e-3, 5e-3, 5e-3, 5e-3]',bg='white').grid(column=5,row=8,sticky=W)
    Label(self,text='e.g.: [1, 1, 2, 1]',bg='white').grid(column=5,row=9,sticky=W)
    Label(self,text='e.g.: 2',bg='white').grid(column=5,row=10,sticky=W)
    Label(self,text='e.g.: [0, 1]',bg='white').grid(column=5,row=11,sticky=W)
    Label(self,text='e.g.: [1, 2, 1, 2]',bg='white').grid(column=5,row=12,sticky=W)
    Label(self,text='e.g.: 1e-3',bg='white').grid(column=5,row=13,sticky=W)
    Label(self,text='e.g.: 1e-3',bg='white').grid(column=5,row=14,sticky=W)
    Label(self,text='e.g.: 60e-6',bg='white').grid(column=5,row=15,sticky=W)
    Label(self,text='e.g.: 2e-2',bg='white').grid(column=5,row=16,sticky=W)
    Label(self,text='e.g.: 1e-3',bg='white').grid(column=5,row=17,sticky=W)
    Label(self,text='e.g.: componentname',bg='white').grid(column=5,row=18,sticky=W)



  def createentries(self):
    
    #defining the entries
    self.fentry=Entry(self,textvariable=self.f,bg='yellow',width=50)
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
    self.Acentry=Entry(self,textvariable=self.Ac,bg='yellow')
    self.dentry=Entry(self,textvariable=self.d,bg='yellow')
    self.centry=Entry(self,textvariable=self.c,bg='yellow')
    self.xentry=Entry(self,textvariable=self.x,bg='yellow')

    #positioning the entries
    self.fentry.grid(column=1,row=1,sticky=(W,E),columnspan=2)
    self.murentry.grid(column=1,row=2,sticky=(W,E),columnspan=2)
    self.nlayerentry.grid(column=1,row=3,sticky=(W,E),columnspan=2)
    self.hentry.grid(column=1,row=4,sticky=(W,E),columnspan=2)
    self.sigmacentry.grid(column=1,row=5,sticky=(W,E),columnspan=2)
    self.sentry.grid(column=1,row=6,sticky=(W,E),columnspan=2)
    self.musentry.grid(column=1,row=7,sticky=(W,E),columnspan=2)
    self.wentry.grid(column=1,row=8,sticky=(W,E),columnspan=2)
    self.mentry.grid(column=1,row=9,sticky=(W,E),columnspan=2)
    self.nwindingentry.grid(column=1,row=10,sticky=(W,E),columnspan=2)
    self.wstyleentry.grid(column=1,row=11,sticky=(W,E),columnspan=2)
    self.lindexentry.grid(column=1,row=12,sticky=(W,E),columnspan=2)
    self.gtentry.grid(column=1,row=13,sticky=(W,E),columnspan=2)
    self.gbentry.grid(column=1,row=14,sticky=(W,E),columnspan=2)
    self.Acentry.grid(column=1,row=15,sticky=(W,E),columnspan=2)
    self.dentry.grid(column=1,row=16,sticky=(W,E),columnspan=2)
    self.centry.grid(column=1,row=17,sticky=(W,E),columnspan=2)
    self.xentry.grid(column=1,row=18,sticky=(W,E),columnspan=2)

  def createbuttons(self):
    buttonframe=Frame(self, bg='white', height=3)
    Button(buttonframe, text='Load Geometry', command=self.loadgeom).pack(side=LEFT,padx=5,pady=5)
    Button(buttonframe, text='Save Geometry', command=self.savegeom).pack(side=LEFT,padx=5,pady=5)
    Button(buttonframe, text='Clear Geometry', command=self.resetgeom).pack(side=LEFT,padx=5,pady=5)
    Button(buttonframe, text='Geometry Editor', command=self.editgeom).pack(side=LEFT,padx=5,pady=5)
    Button(buttonframe, text='Check Geometry', command=self.checkgeom).pack(side=LEFT,padx=5,pady=5)
    Button(buttonframe, text='Generate Netlist',command=self.try_generate_netlist).pack(side=LEFT,padx=5,pady=5)
    Button(buttonframe, text='Design Guide',command=self.designref).pack(side=LEFT,padx=5,pady=5)
    Button(buttonframe, text='Netlist Viewer',command=self.viewnetlist).pack(side=LEFT,padx=5,pady=5)
    buttonframe.grid(row=0, columnspan=7)

  def getImpe(self):
 
    d=float(self.d.get())
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
    Ac=float(self.Ac.get())

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
    Xfb=complex(0,1)*(f*2*math.pi)*4*math.pi*1e-7*Ac/(gb+Ac*w[i1]/(mur*c*d))
    Xft=complex(0,1)*(f*2*math.pi)*4*math.pi*1e-7*Ac/(gt+Ac*w[i1]/(mur*c*d))
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
    if self.netlistfilename:

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
        Ac=float(self.Ac.get())
        d=float(self.d.get())
        c=float(self.c.get())
        x=self.x.get()    #x is a string value
        x=x.replace('\n', '').replace('\r', '').replace(' ','') #get rid of all invalid string 
        if x != '':
           x='_'+x

        self.getImpe()


        Serieslayers={}
        #Repeat and summarizing the input information
        f=open(self.netlistfilename,'w')
        
        #Generate netlist identification information
        localtime = time.asctime( time.localtime(time.time()))
        user = getpass.getuser()
        f.write('\n******************************************************************')
        f.write('\n*****        {0} by {1}          *****'.format(localtime,user))
        f.write('\n******************************************************************')
        
        #Start describing the transformer structure
        f.write('\n******************************************************************')
        f.write('\n******* Comprehensive  Summary of the Magnetic Structure  ********')
        f.write('\n******* Please double check the geometry information and  ********')
        f.write('\n**** use the external Port Name to interface with your circuit ***')
        f.write('\n******************************************************************')
        
        f.write('\n\n* The name of the component is: {}. This name can only be used once in a circuit.'.format(x))
        f.write('\n\n* This planar structure has {0} windings and {1} layers'.format(NumofWinding, NumofLayer))

        for index_winding in range(NumofWinding):
            #Parallel Connected
          if WindingStyle[index_winding]==1:
            f.write('\n\n* -> All layers in winding {0} are Parallel Connected; \n* -> Its external Port Name: PortP{0}{1}, PortN{0}{1}'.format(index_winding+1,x))
            totalturn=0
            for index_layer in range(NumofLayer):
              if WindingIndex[index_layer]==index_winding+1:
                f.write('\n* --> Includes Layer {}'.format(index_layer+1))
                f.write('\n* ---> thickness {:4.2f}um, width {:4.2f}mm, turns {}, spacing above {:4.2f}mm, spacing below {:4.2f}mm'.format(h[index_layer]*1e6, w[index_layer]*1e3, m[index_layer], s[index_layer]*1e3, s[index_layer+1]*1e3))
                totalturn=totalturn+m[index_layer]
            f.write('\n* -> Winding {0} has {1} total turns;'.format(index_winding+1, totalturn))

        
            #Series Connected
          if WindingStyle[index_winding]==0:
            f.write('\n\n* -> All layers in winding {0} are Series Connected; \n* -> Its external Port Name: PortP{0}{1}, PortN{0}{1}'.format(index_winding+1,x))
            numSeriesLayers=1
            totalturn=0
            for index_layer in range(NumofLayer):
              if WindingIndex[index_layer]==index_winding+1:
                f.write('\n* --> Includes Layer {}'.format(index_layer+1))
                f.write('\n* ---> thickness {:4.2f}um, width {:4.2f}mm, turns {}, spacing above {:4.2f}mm, spacing below {:4.2f}mm'.format(h[index_layer]*1e6, w[index_layer]*1e3, m[index_layer], s[index_layer]*1e3, s[index_layer+1]*1e3))
                numSeriesLayers+=1
                totalturn=totalturn+m[index_layer]
            f.write('\n* -> Winding {0} has {1} total turns;'.format(index_winding+1, totalturn))

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
          f.write('\nLe{0}{2} N{0}{2} P{0}{2} {1} Rser=1f'.format(index+1,mx**2,x))
          f.write('\nLi{0}{2} G{2} Md{0}{2} {1} Rser=1f'.format(index+1,1,x))
          f.write('\nLg{0}{2} Mg{0}{2} Md{0}{2} {1:14.2f}p Rser=1f'.format(index+1,lb*1e12,x))
          f.write('\nRg{0}{2} Mc{0}{2} Mg{0}{2} {1:14.2f}m'.format(index+1,rb*1e3,x))
          f.write('\nRt{0}{2} Mc{0}{2} Mt{0}{2} {1:14.2f}u'.format(index+1,ra*1e6,x))
          f.write('\nRb{0}{2} Mb{0}{2} Mc{0}{2} {1:14.2f}u'.format(index+1,ra*1e6,x))
          f.write('\nLt{0}{2} T{0}{2} Mt{0}{2} {1:14.2f}p Rser=1f'.format(index+1,la*1e12,x))
          f.write('\nLb{0}{2} Mb{0}{2} B{0}{2} {1:14.2f}p Rser=1f'.format(index+1,la*1e12,x))
          f.write('\nLs{0}{3} B{0}{3} T{1}{3} {2:14.2f}n  Rser=1f'.format(index+1,index+2,ls*1e9,x))
          f.write('\nK{0}{1} Le{0}{1} Li{0}{1} 1'.format(index+1,x))

        #Print the ferrite cores and top spacing
        f.write('\n\n*NetList for Top and Bottom Ferrites, as well as the First Spacing on Top Side')
        f.write('\nLft{1} T0{1} G{1} {0:14.2f}n Rser=1f'.format(self.Lft*1e9,x))
        f.write('\nLfb{2} T{0}{2} G{2} {1:14.2f}n Rser=1f'.format(NumofLayer+1,self.Lfb*1e9,x))
        f.write('\nLs0{1} T1{1} T0{1} {0:14.2f}n Rser=1f'.format(self.Lts*1e9,x))

        #Print the external connections
        f.write('\n\n*NetList for Winding Interconnects')
        f.write('\n*A few 1f ohm resistors are used as short interconnects')

        #Create External Winding Ports
        for index_winding in range(NumofWinding):
          #Parallel Connected
          if WindingStyle[index_winding]==1:
            f.write('\n\n* -> Winding {} is Parallel Connected'.format(index_winding+1))
            for index_layer in range(NumofLayer):
              if WindingIndex[index_layer]==index_winding+1:
                f.write('\n* -->Include layer {}'.format(index_layer+1))
                f.write('\nRexP{0}{2} PortP{1}{2} P{0}{2}    1f'.format(index_layer+1,index_winding+1,x))
                f.write('\nRexN{0}{2} PortN{1}{2} N{0}{2}    1f'.format(index_layer+1,index_winding+1,x))


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
            f.write('\nRexP{0}{2} PortP{1}{2} P{0}{2}    1f'.format(Serieslayers[1],index_winding+1,x))
            f.write('\nRexN{0}{2} PortN{1}{2} N{0}{2}    1f'.format(Serieslayers[numSeriesLayers-1],index_winding+1,x))
            #defining the interconnects among series connected layers
            for index_SeriesLayers in range(numSeriesLayers-2):
              f.write('\nRexM{0}{2} N{0}{2} P{1}{2}      1f'.format(Serieslayers[index_SeriesLayers+1],Serieslayers[index_SeriesLayers+2],x))
        
        f.write('\n\n*One 1G ohm resistor is used to ground the floating domain')
        f.write('\nRgnd{0} G{0} 0  1G\n\n'.format(x))

        #netlist finalized
        f.write('\n******************************************************************')
        f.write('\n*****                   Netlist Ends                      ********')
        f.write('\n******************************************************************')
        f.close()
        
        result=tkMessageBox.askyesno('M2Spice - Conversion Finished!', message='Successfully generated the netlist! The netlist is saved at:\n\n'  + self.netlistfilename +'\n\n Do you want to open the netlist now?')
        if result==True:
            f=open(self.netlistfilename,'r')
            netlist=f.read()
            f.close()
            viewer = tk.Toplevel(self, bg='white', width=700,height=500)
            viewer.title("M2Spice - Netlist Viewer")
            viewarea = tk.Frame(viewer,height=100,width=50,bg='white',borderwidth=1)
            viewscrollbar=tk.Scrollbar(viewarea)
            editArea=tk.Text(viewarea,width=100,height=30,wrap="word",yscrollcommand=viewscrollbar.set,borderwidth=0,highlightthickness=0)
            viewscrollbar.config(command=editArea.yview)
            viewscrollbar.pack(side="right",fill="y")
            editArea.pack(side="left",fill="both",expand=True)
            editArea.insert(tk.INSERT,netlist)
            viewarea.place(x=20,y=20)
        
            sw = viewer.winfo_screenwidth()
            sh = viewer.winfo_screenheight()
            w = int(sw*0.6)
            h = int(sh*0.6)
            x = sw-w
            y = sh-h
            viewer.geometry('%dx%d+%d+%d' % (w, h, x, y))

  def try_generate_netlist(self):
    try:
      self.generate_netlist()
    except Exception as e:
      tkMessageBox.showerror('M2Spice - Conversion Failed', message='Failed to generate the netlist. System reported the following errors: \n\n' +e.message + '\n\nPossible reason: 1. invalid saving address; 2. invalid geometry format'+'\n\nPlease check the saving address and geometry status.')



class ScrollbarFrame(Frame):
  def __init__(self, root):
    Frame.__init__(self, root,height=800,width=900)
    self.canvas = Canvas(root, borderwidth=2, bg='white')
    self.frame = GUI(root)
    self.hsb = Scrollbar(root, orient="horizontal", command=self.canvas.xview)
    self.vsb = Scrollbar(root, orient="vertical", command=self.canvas.yview)
    self.canvas.configure(xscrollcommand=self.hsb.set,yscrollcommand=self.vsb.set)

    self.vsb.pack(side="right", fill="y")
    self.hsb.pack(side="bottom",fill="x")
    self.canvas.pack(side="top", fill="both", expand=TRUE, padx=30,pady=10)
    self.canvas.create_window((4,4),window=self.frame, anchor="nw", tags="self.frame")

    self.frame.bind("<Configure>", self.OnFrameConfigure)
    #self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    

  def OnFrameConfigure(self, event):
    '''Reset the scroll region to encompass the inner frame'''
    self.canvas.configure(scrollregion=self.canvas.bbox("all"))

  def _on_mousewheel(self, event):
    self.canvas.yview_scroll(-1*(event.delta), "units")


if __name__=='__main__':
    
  root=Tk()
  mainframe=ScrollbarFrame(root)
  root.mainloop()
