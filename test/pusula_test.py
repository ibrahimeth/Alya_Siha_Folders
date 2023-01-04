from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as img
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
class MplCanvas(FigureCanvas):
    def _init_(self, widht=50, height=40, dpi=100):
        self.fig = Figure(figsize=(widht, height), dpi= dpi)
        self.axes = self.fig.add_subplot(111)
        # super(MplCanvas, self)._init_(self.fig)
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

