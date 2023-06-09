import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from main_UI import Ui_MainWindow
from canvas import pusula, Gyro_Cencor, altimetre, battery, compass, indicator_type2
import Map, serial, serial.tools.list_ports
import videodisplay
import sys, os
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import threading
from multiprocessing import Process

class SerialThreadClass(QThread):
    Mesaj = pyqtSignal(str)

    def __init__(self) -> None:
        super(SerialThreadClass, self).__init__()
        self.seriport = serial.Serial()

class MainWİndow(QMainWindow) :
    def __init__(self):
        super(MainWİndow,self).__init__()
        self.ui = Ui_MainWindow()
        self.Myserial = SerialThreadClass()
        self.player = QMediaPlayer()
        self.pusula_indicator = pusula(31)
        self.altimetre_indicator = altimetre(31)
        self.compass_indicator = compass()
        self.battery_indicator = battery(31)
        self.CAM = videodisplay.App()
        self.Map = Map.MyApp()
        self.initUI()

    def initUI(self):
        self.ui.setupUi(self)   
        self.setWindowTitle("ALYA SİHA KONTROL PANELİ")
        self.setWindowIcon(QIcon("planeLogo.ico"))
        self.ui.videomodecombobox.addItem("0")
        self.ui.videomodecombobox.addItem("1")
        self.ui.videomodecombobox.currentTextChanged.connect(self.esitle)
        self.ui.video_control_btn.clicked.connect(lambda :videodisplay.App)
        #port işlemleri yapıyoruz.
        self.cheatbox = []
        self.portkume = []
        self.ports = serial.tools.list_ports.comports()
        for i in self.ports:
            self.portkume.append(str(i))
        self.ui.Port_combox.addItems(self.portkume)  
        #Connection pencesesi widgets
        self.ui.connect_btn.clicked.connect(self.connect)
        self.ui.disconnect_btn.clicked.connect(self.disconnect)
        self.ui.serial_control_port.clicked.connect(self.status)
        # kontrol panel button fonksiyonları eklenmektedir
        self.ui.stackedWidget.setCurrentWidget(self.ui.telemeri_page)
        self.ui.kara_kutu_btn.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.kara_kutu_page))
        self.ui.controller_btn.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.telemeri_page))
        self.ui.Baglanti_page_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Baglanti_page))
        self.ui.Kara_kutu_settings_temizle_btn.clicked.connect(lambda : self.LOG.clear() and self.ui.Kara_kutu_text_label.setText(self.LOG))
        # Widgetsler diğer dosyalardan import edilerek layoutlara yerleştiriliyor
        self.ui.right_indicator.addWidget(self.pusula_indicator.pusula)
        self.ui.left_indicator.addWidget(self.altimetre_indicator.altimetre)
        self.ui.left_indicator.addWidget(self.battery_indicator.battery_indicator)
        self.ui.right_indicator.addWidget(self.compass_indicator.compass_indicator)
        self.ui.Map_layout.addWidget(self.Map.webView)
        self.ui.CAM_layout.addWidget(self.CAM.image_label)
        self.ui.Kara_kutu_settings_Log_kaydet_btn.clicked.connect(lambda : self.Log_kayıt())
    def esitle(self):
        videodisplay.VideoThread.a = self.ui.videomodecombobox.currentText
    def port_listele(self) :
        self.portkume = []
        self.ports = serial.tools.list_ports.comports()
        for i in self.ports:
            self.portkume.append(str(i))
        self.ui.Port_combox.addItems(self.portkume)  

    def playVoice(self,name) :
        full_file_path = os.path.join(os.getcwd(), name)
        url = QUrl.fromLocalFile(full_file_path)
        self.content = QMediaContent(url)
        self.player.setMedia(self.content)
        self.player.play()

    def Log_kayit(self) :
        self.LOG =[
            "[16:24]Log Kayit Acildi. \n",
            "[16:24]Hava Araci tüm sistemler calisti\n",
            "[16:27]Hava Araci Seyir Modu Aktif edildi\n",
            "[16:28]Rakip iha Kilit atildi 16:35:02\n",
            "[16:35]Rakip iha Killit Devre dişi 16:35:022\n",
            "[16:36]Hava araci Landing\n"
            ] 
        self.ui.Kara_kutu_text_label.setText(self.LOG)

    def initmessage(self):
        self.incomingMessage = str(self.Myserial.data.decode("UTF-8"))
        self.cheatbox.append(self.incomingMessage)

    def connect(self):
        self.selectbaudrate = self.ui.baudrate_combox.currentText()
        self.selectport = self.ui.Port_combox.currentText().split()
        self.Myserial.seriport.baudrate = self.selectbaudrate
        self.Myserial.seriport.port = self.selectport[0]
        try :
            self.Myserial.seriport.open()
            self.ui.communicate_status_bar.setStyleSheet("color : rgb(22, 148, 26);")
            self.ui.communicate_status_bar.setText("Bağlanti Gerçekleşti")
            self.Myserial.seriport.write("r".encode("UTF-8"))
            p1 = threading.Thread(target=self.listen).start()
        except:
            self.ui.communicate_status_bar.setStyleSheet("color :rgb(255, 3, 28);")
            self.ui.communicate_status_bar.setText("""Baglanti Başarisiz.\n\n
            Portunuzun takili olduğundan emin olunuz\n Gerekirse uygulamayi yeniden baslatin.\n
            şuanda sistem portunuzu okuyamiyor.
            """)

    def disconnect(self):
        if(self.Myserial.seriport.is_open):
            self.ui.communicate_status_bar.setStyleSheet("color :rgb(255, 3, 28);")
            self.ui.communicate_status_bar.setText("Baglanti Kesildi.")
            self.Myserial.seriport.write("q".encode("UTF-8"))
            self.Myserial.seriport.close()
        else:
            self.ui.communicate_status_bar.setStyleSheet("color: rgb(252, 255, 28);")
            self.ui.communicate_status_bar.setText("Bağlanti Zaten Yok.")
    
    def listen(self) :
        self.box = []
        mdata = ""
        while True :
            try:
                self.data =self.Myserial.seriport.readline.decode("UTF-8")
                self.Myserial.seriport
                mdata = mdata + "|" + self.data
                print("Gelen Veri >>{0}".format(mdata))
                print(self.data)
                if self.data == "q" :
                    m = mdata.split("|")
                    self.box.append(m)
                    self.ui.chat_seri_box_label.setText("asddsadsa")
                    print(self.box)
                    break
            except :
                self.Myserial.seriport.write("q".encode("UTF-8"))
                self.data = "q"
                self.box.append(self.data)
    def send(self,veri) :
        try :
            self.Myserial.seriport.write(veri.encode("UTF-8"))
            print("bir şeyler gönderdik bakalim")
        except:
            self.ui.communicate_status_bar.setText("veri gönderilemedi..")
    def status(self):
        if(self.Myserial.seriport.is_open):
            self.ui.communicate_status_bar.setText("Şuanda Bagliyiz\nKontrol biti gönderildi")
            self.Myserial.seriport.write("z".encode("UTF-8"))
        else:
            self.ui.communicate_status_bar.setText("Bağlanti maalesef ki yok tekrar deneyiniz.")