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
        self.pusula_indicator = pusula()
        self.altimetre_indicator = altimetre()
        self.compass_indicator = compass()
        self.battery_indicator = battery()
        self.CAM = videodisplay.App()
        self.Map = Map.MyApp()
        self.initUI()

    def initUI(self):
        self.ui.setupUi(self)
        self.setWindowTitle("ALYA SİHA KONTROL PANELİ")
        self.setWindowIcon(QIcon("plane_icon.ico"))
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
        self.ui.Speed_ibre_layout.addWidget(self.pusula_indicator.pusula)
        self.ui.plane_indicator_left_top_layout.addWidget(self.altimetre_indicator.altimetre)
        self.ui.plane_indicator_left_bot_layout.addWidget(self.battery_indicator.battery_indicator)
        self.ui.compass_layout.addWidget(self.compass_indicator.compass_indicator)
        self.ui.Map_layout.addWidget(self.Map.webView)
        self.ui.CAM_layout.addWidget(self.CAM.image_label)
        # self.ui.Kara_kutu_settings_Log_kaydet_btn.clicked.connect(lambda : self.Log_kayıt())
        # self.ui.Gyro_Layout.addWidget(self.gyro.gyro)

        self.ui.progressBar_2.setValue(50)

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
    def Log_kayıt(self) :
        self.LOG =[
            "[16:24]Log Kayıt Acildi. \n",
            "[16:24]Hava Aracı tüm sistemler calıştı\n",
            "[16:27]Hava Aracı Seyir Modu Aktif edildi\n",
            "[16:28]Rakip iha Kilit atıldı 16:35:02\n",
            "[16:35]Rakip iha Killit Devre dışı 16:35:022\n",
            "[16:36]Hava aracı Landing\n"
            ] 
        # self.ui.Kara_kutu_text_label.setText(self.LOG)
    def initmessage(self):
        self.incomingMessage = str(self.Myserial.data.decode("utf-8"))
        self.cheatbox.append(self.incomingMessage)
    def connect(self):
        self.selectbaudrate = self.ui.baudrate_combox.currentText()
        self.selectport = self.ui.Port_combox.currentText().split()
        self.Myserial.seriport.baudrate = self.selectbaudrate
        self.Myserial.seriport.port = self.selectport[0]
        try :
            self.Myserial.seriport.open()
            self.ui.communicate_status_bar.setStyleSheet("color : rgb(22, 148, 26);")
            self.ui.communicate_status_bar.setText("Bağlantı Gerçekleşti")
            self.Myserial.seriport.write("r".encode("utf-8"))
            p1 = threading.Thread(target=self.listen).start()
        except:
            self.ui.communicate_status_bar.setStyleSheet("color :rgb(255, 3, 28);")
            self.ui.communicate_status_bar.setText("""Bağlantı Başarısız.\n\n
            Portunuzun takılı olduğundan emin olunuz\n Gerekirse uygulamayı yeniden başlatın.\n
            şuanda sistem portunuzu okuyamıyor.
            """)

    def disconnect(self):
        if(self.Myserial.seriport.is_open):
            self.ui.communicate_status_bar.setStyleSheet("color :rgb(255, 3, 28);")
            self.ui.communicate_status_bar.setText("Bağlantı Kesildi.")
            self.Myserial.seriport.write("q".encode("utf-8"))
            self.Myserial.seriport.close()
        else:
            self.ui.communicate_status_bar.setStyleSheet("color: rgb(252, 255, 28);")
            self.ui.communicate_status_bar.setText("Bağlantı Zaten Yok.")
    
    def listen(self) :
        self.box = []
        mdata = ""
        while True :
            try:
                self.data =self.Myserial.seriport.read().decode("utf-8")
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
                self.Myserial.seriport.write("q".encode("utf-8"))
                self.data = "q"
                self.box.append(self.data)
    def send(self,veri) :
        try :
            self.Myserial.seriport.write(veri.encode("utf-8"))
            print("bir şeyler gönderdik bakalım")
        except:
            self.ui.communicate_status_bar.setText("veri gönderilemedi..")
    def status(self):
        if(self.Myserial.seriport.is_open):
            self.ui.communicate_status_bar.setText("Şuanda Bağlıyız\nKontrol biti gönderildi")
            self.Myserial.seriport.write("z".encode("utf-8"))
        else:
            self.ui.communicate_status_bar.setText("Bağlantı maalesef ki yok tekrar deneyiniz.")