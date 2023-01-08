# contributions by ibrahimeth
# gerekli kütüphanelerimmizi iöport ediyoruz
import matplotlib.image as mpimg
import sys, math
import matplotlib as mpl
from PyQt5 import QtCore, QtWidgets,QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import matplotlib. image as img
import matplotlib.pyplot as plt

# kendimzice bir figure sahip olan bir sınıf oluşturduk böylece her gösterge aynı cinsten olacak
class MplCanvas(FigureCanvasQTAgg):
        # initilation veya constructer kısmında figur ve axes taımladık
    def __init__(self, parent=None, width=1, height=1, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor="black")
        self.axes = self.fig.add_subplot(1,1,1)
        super(MplCanvas, self).__init__(self.fig)

class pusula():
    def __init__(self) -> None:
        self.cx = 600                                        #resimin 600. x kordinatında pikselde nokta oluşturduk
        self.cy = 600                                        #resimin 600. x kordinatında pikselde nokta oluşturduk
        self.r = 400                                         #0 ile 360 arasında değer alan aci değeri istedik
        self.aci = 0
        self.pusula = MplCanvas(self, width= 3, height= 4, dpi=100)        #Pusula adında bir canvas oluşturduk
        self.main()

    def main(self) :
        # QtGui.QPixmap(u":/other/images/ibre.png")
        self.ibre = img.imread("ibre.png") 
        self.y = [600,1000]
        self.x = [600,1000]
        self.pusula.axes.set_ylim([0,1200])                                           # y ekseninni düzenledik
        self.pusula.axes.imshow(self.ibre)
        self.ln = self.pusula.axes.plot(self.x, self.y,  linewidth=3)
        self.pusula.axes.axis("off")
        self.animation = FuncAnimation(self.pusula.fig, self.update, interval = 700,  init_func= self.artist)         #Animasyonu başlattık

    def artist(self):
        return self.ln

    def update(self, frame):
        self.aci += 5
        hours_dx = self.cx + int(math.cos(math.radians(-self.aci))*self.r*.75)
        hours_dy = self.cy - int(math.sin(math.radians(-self.aci))*self.r*.75)
        self.y = [600,hours_dy ]
        self.x = [600,hours_dx]
        self.pusula.axes.clear()
        self.pusula.axes.imshow(self.ibre)
        self.pusula.axes.set_ylim([0, 1200])
        self.pusula.axes.plot(self.x, self.y, linewidth = 5)
        # self.pusula.axes.set_visible(True)
        self.pusula.axes.axis("off")
        

class Gyro_Cencor():
    def __init__(self) -> None:
        self.ox = 1500
        self.oy = 1500
        self.gyro = MplCanvas(self, width= 3, height= 4, dpi=100)
        self.rotate = 0
        self.main()
    def main(self):
        self.x = [1500 , 1900]
        self.y = [1900, 1900]
        self.image = img.imread("gyro_img.png")
        self.gyro.axes.imshow(self.image)
        self.lnn = self.gyro.axes.plot(self.x, self.y)
        self.animationn = FuncAnimation(self.gyro.fig, self.update, interval = 90, init_func= self.artist)         #Animasyonu başlattık
    def artist(self):
        return self.lnn
    def update(self,frame):
        self.ly = self.ox + 100
        self.x = [self.ox , self.ly]
        self.y = [self.ox, self.ly]
        self.gyro.axes.clear()
        self.gyro.axes.imshow(self.image)
        self.gyro.axes.axis("off")
        self.gyro.axes.plot(self.x, self.y)