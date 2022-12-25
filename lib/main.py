from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from main_UI import Ui_MainWindow
import sys

class MainWİndow(QMainWindow) :
    def __init__(self):
        super(MainWİndow,self).__init__()
        self.ui = Ui_MainWindow()
        self.setWindowTitle("ALYA SİHA KONTROL PANELİ")

        self.initUI()

    def initUI(self):
        self.ui.setupUi(self)
        self.ui.Null1_btn.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.Null_page))
        self.ui.controller_btn.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.controller_page))
        

