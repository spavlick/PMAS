from gui import GUI
from Tkinter import *
from ttk import *

class ScrollCanvas(Canvas):
  def __init__(self,root):
    self.root=root
    Canvas.__init__(self,self.root,width=300,height=300,scrollregion=(0,0,500,500))

    self.xscrollbar=Scrollbar(self,orient=HORIZONTAL)
    self.xscrollbar.pack(side=BOTTOM,fill=X)
    self.xscrollbar.config(command=self.canvas.xview)
    self.yscrollbar=Scrollbar(self,orient=VERTICAL)
    self.yscrollbar.pack(side=RIGHT,fill=Y)
    self.yscrollbar.config(command=self.canvas.yview)
    self.canvas.config(width=300,height=300)
    self.canvas.config(xscrollcommand=self.xscrollbar.set,yscrollcommand=self.yscrollbar.set)
    self.canvas.pack(side=LEFT,expand=TRUE,fill=BOTH)
