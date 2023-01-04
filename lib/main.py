from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from main_UI import Ui_MainWindow
from canvas import pusula
import sys
import os
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class MainWİndow(QMainWindow) :
    def __init__(self):
        super(MainWİndow,self).__init__()
        self.ui = Ui_MainWindow()
        self.setWindowTitle("ALYA SİHA KONTROL PANELİ")
        self.player = QMediaPlayer()
        self.pusula = pusula()
        self.initUI()

    def initUI(self):
        self.ui.setupUi(self)
        self.ui.Null1_btn.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.Null_page))
        self.ui.controller_btn.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.controller_page))
        self.ui.verticalLayout_8.addWidget(self.pusula.pusula)
        
    def playVoice(self,name) :
        full_file_path = os.path.join(os.getcwd(), name)
        url = QUrl.fromLocalFile(full_file_path)
        self.content = QMediaContent(url)
        self.player.setMedia(self.content)
        self.player.play()



