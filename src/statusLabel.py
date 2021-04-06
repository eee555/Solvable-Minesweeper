from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
import configparser

class StatusLabel (QtWidgets.QLabel):
    leftRelease = QtCore.pyqtSignal ()  # 定义信号

    def __init__(self, parent=None):
        super (StatusLabel, self).__init__ (parent)
        config = configparser.ConfigParser()
        config.read('gameSetting.ini')
        self.pixSize = config.getint('DEFAULT','pixSize')

        self.setFrameShape (QtWidgets.QFrame.Panel)
        self.setFrameShadow (QtWidgets.QFrame.Raised)
        self.setLineWidth(1)
        self.setAlignment (QtCore.Qt.AlignCenter)
        self.pixmap1 = QPixmap("media/f4.png")
        self.pixmap2 = QPixmap("media/f0.png")
        self.reloadFace(self.pixSize)

    def reloadFace(self, pixSize):
        self.pixSize = pixSize
        self.pixmap1 = self.pixmap1.scaled(self.pixSize * 1.5, self.pixSize * 1.5)
        self.pixmap2 = self.pixmap2.scaled(self.pixSize * 1.5, self.pixSize * 1.5)

    def mousePressEvent(self, e):  ##重载一下鼠标点击事件
        if e.button () == QtCore.Qt.LeftButton:
            self.setPixmap(self.pixmap1)

    def mouseReleaseEvent(self, e):
        if e.button () == QtCore.Qt.LeftButton:
            self.setPixmap(self.pixmap2)
            if self.pixSize * 1.5 >= e.localPos().x() >= 0 and 0 <= e.localPos().y() <= self.pixSize*1.5:
                self.leftRelease.emit()
    
