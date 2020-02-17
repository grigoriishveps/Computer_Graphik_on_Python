# encoding: utf8
import numpy as np
from tkinter import *
a = np.array([[5, 3, -7], [-1, 6, -3], [2, -4, 1]], int)
b = np.array([[4, -1, 3], [4, -2, -6], [2, 0, 3]], int)

root = Tk()

graphWindow = Canvas(root, width = 800, height = 400, bg = 'white')
graphWindow.pack()
#graphWindow.create_window()
graphWindow.create_line(10, 10, 50, 60)

root.mainloop()
print(a*b)
print(np.dot(a,b))