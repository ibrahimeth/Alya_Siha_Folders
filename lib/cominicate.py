import serial, time
import serial.tools.list_ports
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
class SerialThreadClass(QThread):
    Mesaj = pyqtSignal(str)

    def __init__(self) -> None:
        super(SerialThreadClass, self).__init__()
        self.seriport = serial.Serial()

class Communication():
    def __init__(self) -> None:
        self.Myserial = SerialThreadClass()