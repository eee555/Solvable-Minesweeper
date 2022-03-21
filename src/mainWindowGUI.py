from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
import configparser
# 定义关闭主窗口后的事件
# 重写QMainWindow
class MainWindow(QtWidgets.QMainWindow):
    keyRelease = QtCore.pyqtSignal(str)
    closeEvent_ = QtCore.pyqtSignal()
    def closeEvent(self, event):
        conf = configparser.ConfigParser()
        conf.read("gameSetting.ini")
        conf.set("DEFAULT", "mainWinTop", str(self.x()))
        conf.set("DEFAULT", "mainWinLeft", str(self.y()))
        conf.write(open('gameSetting.ini', "w"))
        self.closeEvent_.emit()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Space and not event.isAutoRepeat():
            self.keyRelease.emit('Space')
            





