from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2, time
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from main_UI import Ui_MainWindow
import numpy as np
import threading

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    def __init__(self) -> None:
        super(VideoThread, self).__init__()
    def run(self):
        # capture from web cam
        # self.cap = cv2.VideoCapture(self.a)
        self.cap = cv2.VideoCapture(0)
        while True:
            ret, cv_img = self.cap.read()
            cv2.waitKey(1)   #sıkıntı çıkarsa kapat
            if ret:
                self.change_pixmap_signal.emit(cv_img)
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 800
        self.display_height = 550
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # metin labeli oluşturdum
        self.textLabel = QLabel('Webcam')

        # video cAPturu oluşturuldu
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

        

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
