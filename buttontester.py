from Tkinter import *
from ttk import *
import tkMessageBox

def func1():
  tkMessageBox.showinfo(message='message 1')
def func2():
  tkMessageBox.showinfo(message='message 2')

root=Tk()
frame=Frame(root)
button=Button(frame,command=func1,text='hi')

button.configure(command=func2)
button.pack()
frame.pack()
root.mainloop()
