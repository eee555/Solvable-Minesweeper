from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

# 重写QMainWindow
class MainWindow(QtWidgets.QMainWindow):
    keyRelease = QtCore.pyqtSignal(str)
    closeEvent_ = QtCore.pyqtSignal()
    flag_drag_border = False
    minimum_counter = 0

    def closeEvent(self, event):
        self.closeEvent_.emit()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Space and not event.isAutoRepeat():
            self.keyRelease.emit('Space')
            
    def resizeEvent(self,event):
        # 拖拽边框后resize尺寸
        if QApplication.mouseButtons() & Qt.LeftButton:
            self.flag_drag_border = True
            self.timer_ = QTimer()
            self.timer_.timeout.connect(self.__minimumWindowRelease)
            self.timer_.start(100)

    def __minimumWindowRelease(self):
        if not (QApplication.mouseButtons() & Qt.LeftButton):
            self.flag_drag_border = False
        if not self.flag_drag_border:
            self.resize(self.minimumSize())
            self.minimum_counter += 1
            if self.minimum_counter >= 10:
                self.minimum_counter = 0
                self.timer_.stop()


