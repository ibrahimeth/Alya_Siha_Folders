from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from main_UI import Ui_MainWindow
from canvas import pusula, Gyro_Cencor
import Map as Map, videodiplay
import sys, os
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class MainWİndow(QMainWindow) :
    def __init__(self):
        super(MainWİndow,self).__init__()
        self.setWindowTitle("ALYA SİHA KONTROL PANELİ")
        self.ui = Ui_MainWindow()
        self.player = QMediaPlayer()
        self.pusula = pusula()
        # self.gyro = Gyro_Cencor()
        self.CAM = videodiplay.App()
        self.Map = Map.MyApp()
        self.initUI()

    def initUI(self):
        self.ui.setupUi(self)
        self.ui.Null1_btn.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.Null_page))
        self.ui.controller_btn.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.controller_page))
    
        # Widgetsler diğer dosyalardan import edilerek layoutlara yerleştiriliyor
        self.ui.Speed_ibre_layout.addWidget(self.pusula.pusula)
        self.ui.CAM_layout.addWidget(self.CAM.image_label)
        self.ui.Map_layout.addWidget(self.Map.webView)
        # self.ui.Gyro_Layout.addWidget(self.gyro.gyro)
    def playVoice(self,name) :
        full_file_path = os.path.join(os.getcwd(), name)
        url = QUrl.fromLocalFile(full_file_path)
        self.content = QMediaContent(url)
        self.player.setMedia(self.content)
        self.player.play()

