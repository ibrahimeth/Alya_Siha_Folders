from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys
import os
from login_ui import Ui_MainWindow
from main import MainWİndow
class MainnWindow(QMainWindow):
    def __init__(self):
        super(MainnWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.main = MainWİndow()
        self.ui.setupUi(self)
        self.window_fix()
        self.player = QMediaPlayer()
        self.initUi()
    def initUi(self):
        self.show()
        self.setWindowTitle("Alya Siha LOGİN")
        self.ui.password_lineEdit.setText("admin")
        self.ui.send_btn.clicked.connect(self.sorgula)
        self.playVoice("vikings.wav")
    def sorgula(self) :
        if(self.ui.password_lineEdit.text() == "admin"):
            self.player.stop()
            self.close()
            self.main.showMaximized()
            self.playVoice("../sound/hoşgeldiniz.wav")
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
        # if self.player.stateChanged():
            # self.playVoice()
    def mute(self):
        self.player.setMuted(not self.player.isMuted())
def mainLOOP():
    fas = QApplication(sys.argv)
    win = MainnWindow()
    sys.exit(fas.exec_())

mainLOOP()