from Tkinter import *
from ttk import *
from impedance import getImpe

root=Tk()
root.title('Planar Magnetics Analyzing System (PMAS)')

#create frame for the GUI
mainframe=Frame(root,padding='3 3 12 12')
mainframe.grid(column=0,row=0,sticky=(N,W,E,S))
mainframe.columnconfigure(0,weight=1)
mainframe.rowconfigure(0,weight=1)

#set variables
f=StringVar()

#allow users to input data
f_entry=Entry(mainframe,width=7,textvariable=f)
#f_entry.grid(mainframe,column=2,row=1,sticky=W)

#create labels for entries
Label(mainframe,text='Fundamental Frequency (kHz)').grid(column=1,row=1,sticky=W)
Label(mainframe,text='Relative Permeability').grid(column=1,row=2,sticky=W)
Label(mainframe,text='Number of Layers (nlayer)').grid(column=1,row=3,sticky=W)
Label(mainframe,text='Layer Thickness (h)').grid(column=1,row=4,sticky=W)
Label(mainframe,text='Spacing Thickness (s)').grid(column=1,row=5,sticky=W)
Label(mainframe,text='Window Width (w)').grid(column=1,row=6,sticky=W)
Label(mainframe,text='Number of Turns Each Layer (m)').grid(column=1,row=7,sticky=W)
Label(mainframe,text='Number of Windings (nwinding)').grid(column=1,row=8,sticky=W)
Label(mainframe,text='Connection Style of Each Winding (wstyle)').grid(column=1,row=9,sticky=W)
Label(mainframe,text='Belongings of Each Layer to Windings (lindex)').grid(column=1,row=10,sticky=W)
Label(mainframe,text='Core Gap Length (mm)').grid(column=1,row=11,sticky=W)
Label(mainframe,text='Effective Core Area (m^2)').grid(column=1,row=12,sticky=W)
Label(mainframe,text='Effective Length (m)').grid(column=1,row=13,sticky=W)
Label(mainframe,text='Number of Cores').grid(column=1,row=14,sticky=W)
Label(mainframe,text='Thickness of the Top and Bottom Core (m)').grid(column=1,row=15,sticky=W)

#create command button


for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

f_entry.focus()


root.mainloop() #execute at end of code
