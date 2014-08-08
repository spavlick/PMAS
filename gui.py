from Tkinter import *
from ttk import *
from impedance import getImpe

root=Tk()
root.title('Planar Magnetics Analyzing System (PMAS)')

#create frame for the GUI
mainframe=Frame(root)
mainframe.grid(column=0,row=0,sticky=(N,W,E,S))
mainframe.columnconfigure(0,weight=1)
mainframe.rowconfigure(0,weight=1)

#set variables
f=StringVar() #switching frequency
mur=StringVar() #relative permeability
nlayer=StringVar() #number of layers
h=StringVar() #layer thickness
s=StringVar() #Spacing thickness
w=StringVar() #window width
m=StringVar() #turns per layer
nwinding=StringVar() #number of windings
wstyle=StringVar() #connection style of each winding
lindex=StringVar() #layer indices
g=StringVar() #core gap length
Ae=StringVar() #effective gap area
le=StringVar() #effective length
nc=StringVar() #number of cores
c=StringVar() #thickness of top and bottom ferrite



#allow users to input data
Entry(mainframe,width=30,textvariable=f).grid(column=1,row=1,sticky=(W,E),columnspan=2)
Entry(mainframe,width=15,textvariable=mur).grid(column=1,row=2,sticky=W)
Entry(mainframe,width=15,textvariable=nlayer).grid(column=1,row=3,sticky=W)
Entry(mainframe,width=15,textvariable=h).grid(column=1,row=4,sticky=W)
Entry(mainframe,width=15,textvariable=s).grid(column=1,row=5,sticky=W)
Entry(mainframe,width=15,textvariable=w).grid(column=1,row=6,sticky=W)
Entry(mainframe,width=15,textvariable=m).grid(column=1,row=7,sticky=W)
Entry(mainframe,width=15,textvariable=nwinding).grid(column=1,row=8,sticky=W)
Entry(mainframe,width=15,textvariable=wstyle).grid(column=1,row=9,sticky=W)
Entry(mainframe,width=15,textvariable=lindex).grid(column=1,row=10,sticky=W)
Entry(mainframe,width=15,textvariable=g).grid(column=1,row=11,sticky=W)
Entry(mainframe,width=15,textvariable=Ae).grid(column=1,row=12,sticky=W)
Entry(mainframe,width=15,textvariable=le).grid(column=1,row=13,sticky=W)
Entry(mainframe,width=15,textvariable=nc).grid(column=1,row=14,sticky=W)
Entry(mainframe,width=15,textvariable=c).grid(column=1,row=15,sticky=W)


#create labels for entries
Label(mainframe,text='Fundamental Frequency (kHz)').grid(column=0,row=1,sticky=W)
Label(mainframe,text='Relative Permeability').grid(column=0,row=2,sticky=W)
Label(mainframe,text='Number of Layers (nlayer)').grid(column=0,row=3,sticky=W)
Label(mainframe,text='Layer Thickness (h)').grid(column=0,row=4,sticky=W)
Label(mainframe,text='Spacing Thickness (s)').grid(column=0,row=5,sticky=W)
Label(mainframe,text='Window Width (w)').grid(column=0,row=6,sticky=W)
Label(mainframe,text='Number of Turns Each Layer (m)').grid(column=0,row=7,sticky=W)
Label(mainframe,text='Number of Windings (nwinding)').grid(column=0,row=8,sticky=W)
Label(mainframe,text='Connection Style of Each Winding (wstyle)').grid(column=0,row=9,sticky=W)
Label(mainframe,text='Belongings of Each Layer to Windings (lindex)').grid(column=0,row=10,sticky=W)
Label(mainframe,text='Core Gap Length (mm)').grid(column=0,row=11,sticky=W)
Label(mainframe,text='Effective Core Area (m^2)').grid(column=0,row=12,sticky=W)
Label(mainframe,text='Effective Length (m)').grid(column=0,row=13,sticky=W)
Label(mainframe,text='Number of Cores').grid(column=0,row=14,sticky=W)
Label(mainframe,text='Thickness of the Top and Bottom Core (m)').grid(column=0,row=15,sticky=W)

#create command button
Button(mainframe,text='Load Geometry').grid(row=0,column=0)
Button(mainframe,text='Save Geometry').grid(row=0,column=1)
Button(mainframe,text='Reset Geometry').grid(row=0,column=2)
Button(mainframe,text='Check Geometry Status').grid(row=16,columnspan=3)
Button(mainframe,text='Generate Netlist').grid(row=18,columnspan=3)


for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)



root.mainloop() #execute at end of code
