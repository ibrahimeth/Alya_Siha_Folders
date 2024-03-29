from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys
import os
from  login_ui import Ui_MainWindow
from main import MainWİndow

class Login_Window(QMainWindow):
    def __init__(self):
        super(Login_Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.window_fix()
        self.player = QMediaPlayer()
        self.initUi()
        
    def initUi(self):
        self.show()
        self.setWindowTitle("Alya Siha LOGİN")
        self.ui.password_lineEdit.setText("admin")
        self.ui.send_btn.clicked.connect(self.sorgula)
        self.ui.alt_btn.clicked.connect(lambda : self.showMinimized())
        self.ui.x_btn.clicked.connect(lambda : self.close())
        self.playVoice("vikings.wav")

    def sorgula(self) :
        if(self.ui.password_lineEdit.text() == "admin"):
            self.player.stop()
            self.close()
            self.main = MainWİndow()
            self.main.showMaximized()
            # self.playVoice("/sound/hoşgeldiniz.wav")
        elif(self.ui.password_lineEdit.text() == "") :
            self.ui.message_box_label.setText("you have to entry \na password.")
        else:
            self.ui.message_box_label.setText("Incorrect Password\nError Code :x3400")

    def mausePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mauseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def window_fix(self) :
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
        self.ui.right_top_frame.mauseMoveEvent = self.mauseMoveEvent

    def playVoice(self,name) :
        full_file_path = os.path.join(os.getcwd(), name)
        url = QUrl.fromLocalFile(full_file_path)
        self.content = QMediaContent(url) 
        self.player.setMedia(self.content)
        self.player.play()

    def mute(self):
        self.player.setMuted(not self.player.isMuted())

def mainLOOP():
    fas = QApplication(sys.argv)
    win = Login_Window()
    sys.exit(fas.exec_())

mainLOOP()