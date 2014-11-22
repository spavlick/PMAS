from Tkinter import *
from ttk import *
import tkMessageBox

def func1():
  tkMessageBox.showmessage('message 1')
def func2():
  tkMessageBox.showmessage('message 2')

root=Tk()
frame=Frame(root)
button=Button(frame,command=func1)
button.configure(command=func2)
frame.pack()
root.mainloop()
