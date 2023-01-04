import matplotlib.pyplot as plt
import matplotlib.image as img
from matplotlib.animation import FuncAnimation
import numpy as np
import math
import time

# ibre = img.imread('pusula.png')
# aci = int(input("ACI :"))
# if (aci >= 45 and aci < 90):
#     def f(x, aci) :
#         return (x - 600) * math.tan(math.radians(aci))  + 600 - math.tan(math.radians(aci-45)) * (x - 600)
#     y = [600,f(800,aci)]
#     x = [600,800]
# y = [600,f(800,aci) ]
# x = [600,800]   
# ibre_uzunluk = math.sqrt((x[1] - x[0]) ** 2 + (y[0] - y[1]) ** 2)
# print(ibre_uzunluk)
# plt.ylim([0,1200])
# plt.imshow(ibre)
# plt.plot(x, y,  linewidth=4)
# plt.show()
# while(True):
#     figure = plt.figure(figsize=(5, 3))
#     axes = figure.add_axes([0.1,0.1,0.9,0.9])
#     aci = int(input("ACI :"))
#     x = (0,1)
#     y = (0, f(1, aci))
#     axes.plot(x, y)
#     plt.imshow(ibre)

# figure = plt.figure(figsize=(5, 5))
# ax = figure.add_axes([0.1, 0.1, 0.9, 0.9])
# cx = 600
# cy = 600
# r = 400
# global aci

# hours_dx = cx + int(math.cos(math.radians(-self.aci))*r*.75)
# hours_dy = cy - int(math.sin(math.radians(-aci))*r*.75)
# ibre = img.imread('pusula.png')

# y = [600,hours_dy ]
# x = [600,hours_dx]  
# ax.set_ylim([0,1200])
# ax.imshow(ibre)
# ln = ax.plot(x, y,  linewidth=5) 
# def artist():
#     return ln
# def update(frame):
#     ax.clear()
#     aci += 1
#     hours_dx = cx + int(math.cos(math.radians(-aci))*r*.75)
#     hours_dy = cy - int(math.sin(math.radians(-aci))*r*.75)
#     y = [600,hours_dy ]
#     x = [600,hours_dx] 
#     ax.plot(x, y)
# animation = FuncAnimation(figure, update, interval = 1000, init_func= artist)
# plt.show()

class pusula():
    def __init__(self) -> None:
        self.figure = plt.figure(figsize=(5, 5))
        self.ax = self.figure.add_axes([0.1, 0.1, 0.9, 0.9])
        self.cx = 600
        self.cy = 600
        self.r = 400
        self.aci = 0
        self.main()
    def main(self) :
        hours_dx = self.cx + int(math.cos(math.radians(-self.aci))*self.r*.75)
        hours_dy = self.cy - int(math.sin(math.radians(-self.aci))*self.r*.75)
        self.ibre = img.imread('pusula.png')
        self.y = [600,hours_dy ]
        self.x = [600,hours_dx] 
        self.ax.set_ylim([0,1200])
        self.ax.imshow(self.ibre)
        self.ln = self.ax.plot(self.x, self.y,  linewidth=5)
        self.ax.axis("off")
        self.animation = FuncAnimation(self.figure, self.update, interval = 50, init_func= self.artist)
        plt.show()
    def artist(self):
        return self.ln
    def update(self, frame):
        self.aci += 2
        hours_dx = self.cx + int(math.cos(math.radians(-self.aci))*self.r*.75)
        hours_dy = self.cy - int(math.sin(math.radians(-self.aci))*self.r*.75)
        self.ibre = img.imread('pusula.png')
        self.y = [600,hours_dy ]
        self.x = [600,hours_dx] 
        self.ax.clear()
        self.ax.imshow(self.ibre)
        self.ax.set_ylim([0, 1200])
        self.ax.plot(self.x, self.y, linewidth = 5)
        self.ax.set_visible(True)
        self.ax.axis("off")
a = pusula()