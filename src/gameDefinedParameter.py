# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_defined_parameter.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtGui
from ui.ui_defined_parameter import Ui_Form
from ui.uiComponents import RoundQDialog

class ui_Form(Ui_Form):
    def __init__(self, row, column, num):
        self.row = row
        self.column = column
        self.mineNum = num
        # self.maxRow = 1e6
        # self.maxColumn = 1e6
        self.alter = False
        self.Dialog = RoundQDialog()
        self.setupUi (self.Dialog)
        self.setParameter()
        self.Dialog.setWindowIcon (QtGui.QIcon ("media/mine.ico"))
        self.pushButton_3.clicked.connect (self.processParameter)
        self.pushButton_2.clicked.connect (self.Dialog.close)
        
    def setParameter(self):
        self.spinBox.setValue (self.row)
        self.spinBox_2.setValue (self.column)
        self.spinBox_3.setValue (self.mineNum)

    def processParameter(self):
        r = self.spinBox.value ()
        c = self.spinBox_2.value ()
        n = self.spinBox_3.value ()
        if r != self.row or c != self.column or n != self.mineNum:
            self.alter = True
            self.row = r
            self.column = c
            self.mineNum = min (max (n, 2), r * c - 1)
        self.Dialog.close ()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    demo = ui_Form(8, 8, 10)
    demo.Dialog.show()
    sys.exit(app.exec_())


