import sys
import os
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtWidgets import QApplication, QWidget , QLabel, QMessageBox,QAction, QPushButton, QGraphicsRectItem, QMainWindow
from PyQt5.QtGui import QIcon, QPainter, QPixmap, QKeySequence, QFont, QFontMetrics, QMovie
from PyQt5 import QtGui


class UIWindow(QWidget):
    def __init__(self, parent=None):
        super(UIWindow, self).__init__(parent)
        self.resize(QSize(400, 450))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), QPixmap("Images\Image.png"))
        # painter.move(0,0)
        # painter.resize(950,270)




class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(490, 200, 950, 620)
        self.setFixedSize(950, 620)
        self.startUIWindow()
        self.setWindowIcon(QtGui.QIcon('Images\Logo.png'))

    def startUIWindow(self):
        self.Window = UIWindow(self)
        self.setWindowTitle("pythonw")
        self.setCentralWidget(self.Window)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())