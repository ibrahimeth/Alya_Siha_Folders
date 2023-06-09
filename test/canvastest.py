import matplotlib.image as mpimg
import math
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.image as img

class MplCanvas(FigureCanvasQTAgg):
        # initilation veya constructer kısmında figur ve axes taımladık
    def __init__(self, parent=None, width=1, height=1, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor="black")
        self.axes = self.fig.add_subplot(2,2,1)
        super(MplCanvas, self).__init__(self.fig)

class indicators():
    def __init__(self, hiz) -> None:
        self.cx = 600                                        #resimin 600. x kordinatında pikselde nokta oluşturduk
        self.cy = 600                                        #resimin 600. x kordinatında pikselde nokta oluşturduk
        self.r = 400                                         #0 ile 360 arasında değer alan aci değeri istedik
        self.aci = 90 - (hiz * 4.5)
        self.pusula = MplCanvas(self, width= 4, height= 4, dpi=100)      #Pusula adında bir canvas oluşturduk
        self.main()

    def main(self) :
        # QtGui.QPixmap(u":/other/images/ibre.png")
        self.ibre = img.imread("ibre.png") 
        hours_dx = self.cx + int(math.cos(math.radians(-self.aci))*self.r*.75)
        hours_dy = self.cy - int(math.sin(math.radians(-self.aci))*self.r*.75)
        self.y = [600,hours_dy ]
        self.x = [600,hours_dx]
        self.pusula.axes.clear()
        self.pusula.axes.imshow(self.ibre)
        self.pusula.axes.set_ylim([0, 1200])
        self.pusula.axes.plot(self.x, self.y, linewidth = 5, marker = "o")
        self.pusula.axes.axis("off")
        self.pusula.fig.subplots(ncols=1,nrows=1)
        
        # self.animation = FuncAnimation(self.pusula.fig, self.update, interval = 1400,  init_func= self.artist)         #Animasyonu başlattık
