from Tkinter import *
from ttk import *

class Box():
  def __init__(self):
    self.f=None
  def createGUI(self):
    root=Tk()
    root.title('testing')
    mainframe=Frame(root)
    mainframe.grid(column=0,row=0,sticky=(N,W,E,S))
    mainframe.columnconfigure(0,weight=1)
    mainframe.rowconfigure(0,weight=1)

    self.f=StringVar()
    Entry(mainframe,width=15,textvariable=self.f).grid(column=1,row=1,sticky=(W,E),columnspan=2)

    Button(mainframe,text='print f',command=self.printf).grid(column=1,row=2)
    
  
    root.mainloop()

  def printf(self):
    print self.f.get()

bbb=Box()
bbb.createGUI()
