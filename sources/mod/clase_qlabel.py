from App_Essen import *
from PyQt5.QtCore import signal
class QlabelClickeable(QLabel):
    #clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super(QlabelClickeable, self).__init__(parent)
    
    def mousePressEvent(self, event):
        self.ultimo = "Clic"
    
    def mouseReleaseEvent(self, ev: PySide2.QtGui.QMouseEvent):
        print(str(super().mouseReleaseEvent(ev)))
        return super().mouseReleaseEvent(ev)
    
    def mouseMoveEvent(self, ev: PySide2.QtGui.QMouseEvent):
        return super().mouseMoveEvent(ev)