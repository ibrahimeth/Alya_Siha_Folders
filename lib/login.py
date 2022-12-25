from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from playsound import playsound
from login_ui import Ui_MainWindow
from main import MainWİndow
class MainnWindow(QMainWindow):
    def __init__(self):
        super(MainnWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.main = MainWİndow()
        self.ui.setupUi(self)
        self.initUi()
    def initUi(self):
        self.show()
        self.setWindowTitle("Alya Siha LOGİN")
        self.ui.password_lineEdit.setText("admin")
        # playsound("vikings.mp3")
        self.ui.send_btn.clicked.connect(self.sorgula)

    def sorgula(self) :
        if(self.ui.password_lineEdit.text() == "admin"):
            self.close()
            self.main.showMaximized()
        else:
            self.ui.message_box_label.setText("Incorrect Password\nError Code :x3400")
            
def mainLOOP():
    fas = QApplication(sys.argv)
    win = MainnWindow()
    sys.exit(fas.exec_())

mainLOOP()

