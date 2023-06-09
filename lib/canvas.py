# contributions by ibrahimeth
#Alya_Siha_System
# gerekli kütüphanelerimmizi import ediyoruz
import matplotlib.image as mpimg
import math
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import matplotlib.image as img
from multiprocessing import Process
from threading import Thread
# kendimzice bir figure sahip olan bir sınıf oluşturduk böylece her gösterge aynı cinsten olacak
class MplCanvas(FigureCanvasQTAgg):
        # initilation veya constructer kısmında figur ve axes taımladık
    def __init__(self, parent=None, width=1, height=1, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor="black")
        self.axes = self.fig.add_subplot(1,1,1)
        super(MplCanvas, self).__init__(self.fig)

class pusula():
    def __init__(self, hiz) -> None:
        self.cx = 600                                        #resimin 600. x kordinatında pikselde nokta oluşturduk
        self.cy = 600                                        #resimin 600. x kordinatında pikselde nokta oluşturduk
        self.r = 400                                         #0 ile 360 arasında değer alan aci değeri istedik
        self.aci = 90 - (hiz * 4.5)
        self.pusula = MplCanvas(self, width= 4, height= 4, dpi=100)        #Pusula adında bir canvas oluşturduk
        self.main()

    def main(self) :
        # QtGui.QPixmap(u":/other/images/ibre.png")
        self.ibre = img.imread("ibre.png") 
        self.y = [600,1000]
        self.x = [600,1000]
        self.pusula.axes.set_ylim([0,1200])                                           # y ekseninni düzenledik
        self.pusula.axes.imshow(self.ibre)
        self.ln = self.pusula.axes.plot(self.x, self.y,  linewidth=3, marker = "o")
        self.pusula.axes.axis("off")
        self.update()
        # self.animation = FuncAnimation(self.pusula.fig, self.update, interval = 1400,  init_func= self.artist)         #Animasyonu başlattık

    def artist(self):
        return self.ln

    def update(self):
        hours_dx = self.cx + int(math.cos(math.radians(-self.aci))*self.r*.75)
        hours_dy = self.cy - int(math.sin(math.radians(-self.aci))*self.r*.75)
        self.y = [600,hours_dy ]
        self.x = [600,hours_dx]
        self.pusula.axes.clear()
        self.pusula.axes.imshow(self.ibre)
        self.pusula.axes.set_ylim([0, 1200])
        self.pusula.axes.plot(self.x, self.y, linewidth = 5, marker = "o")
        # self.pusula.axes.set_visible(True)
        self.pusula.axes.axis("off")      

class Gyro_Cencor():
    def __init__(self) -> None:
        self.ox = 1500
        self.oy = 1500
        self.gyro = MplCanvas(self, width= 4, height= 4, dpi=100)
        self.rotate = 0
        self.main()
    def main(self):
        self.x = [1500 , 1900]
        self.y = [1900, 1900]
        self.image = img.imread("gyro_img.png")
        self.gyro.axes.imshow(self.image)
        self.lnn = self.gyro.axes.plot(self.x, self.y)
        self.update()
        # self.animationn = FuncAnimation(self.gyro.fig, self.update, interval = 90, init_func= self.artist)         #Animasyonu başlattık
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

class altimetre():
    def __init__(self, irtifa_value) -> None:
        self.cx = 600
        self.cy = 600
        self.r = 400
        self.aci = 90 - (irtifa_value * 3.6)
        self.altimetre = MplCanvas(self, width= 4 ,height= 4, dpi=100 )
        self.main()
    def main(self):
        self.ibre = img.imread("Altimetreimg.png")
        self.x = [600,1200]
        self.y = [600,1200]
        self.altimetre.axes.set_ylim([0,1200])
        
        self.altimetre.axes.imshow(self.ibre)

        self.ln = self.altimetre.axes.plot(self.x, self.y, linewidth = 3, color = "white", marker = "o")
        self.altimetre.axes.axis("off")
        self.update()
        # self.animation = FuncAnimation(self.altimetre.fig, self.update, interval = 1400, init_func=self.artist)

    def artist(self):
        return self.ln
    
    def update(self):
        hours_dx = self.cx + int(math.cos(math.radians(-self.aci))*self.r*.75)
        hours_dy = self.cy - int(math.sin(math.radians(-self.aci))*self.r*.75)
        self.y = [600,hours_dy ]
        self.x = [600,hours_dx]
        self.altimetre.axes.clear()
        self.altimetre.axes.imshow(self.ibre)
        self.altimetre.axes.set_ylim([0, 1200])
        self.altimetre.axes.plot(self.x, self.y, linewidth = 5, color = "white", marker = "o")
        self.altimetre.axes.axis("off")      

class battery():                   
    def __init__(self, battery_value) -> None:
        self.cx = 600
        self.cy = 600
        self.r = 400
        self.aci = 17.5 + 1.45 * (100 - battery_value) #17,5 - 162,5
        self.battery_indicator = MplCanvas(self, width= 4 ,height= 4 , dpi=100 )
        self.main()
    def main(self):
        self.ibre = img.imread("batteryimg.png")
        self.x = [600,1200]
        self.y = [600,1200]
        self.battery_indicator.axes.set_ylim([0,1200])
        self.battery_indicator.axes.imshow(self.ibre)

        self.ln = self.battery_indicator.axes.plot(self.x, self.y, linewidth = 3, color = "white", marker = "o")
        self.battery_indicator.axes.axis("off")
        self.update()
        # self.animation = FuncAnimation(self.battery_indicator.fig, self.update, interval = 1400, init_func=self.artist)

    def artist(self):
        return self.ln
    
    def update(self):                             # 3 de başla 32 de bitir  15 derece Full, 160 derece son

        hours_dx = self.cx + int(math.cos(math.radians(-self.aci))*self.r*.75)
        hours_dy = self.cy - int(math.sin(math.radians(-self.aci))*self.r*.75)
        self.y = [600,hours_dy ]
        self.x = [600,hours_dx]
        self.battery_indicator.axes.clear()
        self.battery_indicator.axes.imshow(self.ibre)
        self.battery_indicator.axes.set_ylim([0, 1200])
        self.battery_indicator.axes.plot(self.x, self.y, linewidth = 5, color = "white", marker = "o")
        self.battery_indicator.axes.axis("off")      

class compass():
    def __init__(self) -> None:
        self.cx = 600
        self.cy = 600
        self.r = 400
        self.aci = 0
        self.compass_indicator = MplCanvas(self, width= 4,height= 4, dpi=100 )
        self.main()
    def main(self):
        self.ibre = img.imread("compassimg.png")
        self.x = [600,1200]
        self.y = [600,1200]
        self.compass_indicator.axes.set_ylim([0,1200])
        
        self.compass_indicator.axes.imshow(self.ibre)

        self.ln = self.compass_indicator.axes.plot(self.x, self.y, linewidth = 3, color = "white", marker = "o")
        self.compass_indicator.axes.axis("off")
        self.update()
        # self.animation = FuncAnimation(self.compass_indicator.fig, self.update, interval = 1400, init_func=self.artist)

    def artist(self):
        return self.ln
    
    def update(self):
        self.aci += 5
        hours_dx = self.cx + int(math.cos(math.radians(-self.aci))*self.r*.75)
        hours_dy = self.cy - int(math.sin(math.radians(-self.aci))*self.r*.75)
        self.y = [600,hours_dy ]
        self.x = [600,hours_dx]
        self.compass_indicator.axes.clear()
        self.compass_indicator.axes.imshow(self.ibre)
        self.compass_indicator.axes.set_ylim([0, 1200])
        self.compass_indicator.axes.plot(self.x, self.y, linewidth = 5, color = "white", marker = "o")
        self.compass_indicator.axes.axis("off")      

class indicator_type2():
    def __init__(self) -> None:
        self.x = 100
        self.y = 5 
        self.main()
    def main(self):
        self.indicator = MplCanvas(self,width=4,height=1,dpi=100)
        # self.indicator.axes.set_ylim =([0,100])
        x = np.array([10])
        y = np.linspace(0,100,100)
        self.ln = self.indicator.axes.barh(x, y, color = "pink")
