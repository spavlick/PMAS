#make sample interface and try adding two functions to button like it says on StackOverflow

import tkinter as tk
import time

class ButtonTimer:
    def __init__(self, root):
        self.master = root
        self.button = tk.Button(self.master, text="press me")  # Notice I haven't assigned the button a command - we're going to bind mouse events instead of using the built in command callback.
        self.button.bind('<ButtonPress>', self.press)       # call 'press' method when the button is pressed
        self.button.configure(command=
        self.button.bind('<ButtonRelease>', self.release)   # call 'release' method when the button is released
        self.label = tk.Label(self.master)
        self.startTime = time.time()
        self.endTime = self.startTime

        self.button.grid(row=1, column=1)
        self.label.grid(row=2, column=1)

    def message(self):
        tk.tkMessageBox(message='HI!!!!')

    def press(self, *args):
        self.startTime = time.time()

    def release(self, *args):
        self.endTime = time.time()
        self.label.config(text="Time pressed: "+str(round(self.endTime - self.startTime, 2))+" seconds")

root = tk.Tk()
b = ButtonTimer(root)
root.mainloop()
