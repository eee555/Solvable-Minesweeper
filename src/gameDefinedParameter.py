# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_defined_parameter.ui'
# 自定义

from PyQt5 import QtGui
from ui.ui_defined_parameter import Ui_Form
from ui.uiComponents import RoundQDialog

class ui_Form(Ui_Form):
    def __init__(self, r_path, row, column, num, parent):
        self.row = row
        self.column = column
        self.mineNum = num
        # self.maxRow = 1e6
        # self.maxColumn = 1e6
        self.alter = False
        self.Dialog = RoundQDialog(parent)
        self.setupUi (self.Dialog)
        self.setParameter()
        self.Dialog.setWindowIcon (QtGui.QIcon (str(r_path.with_name('media').joinpath('cat.ico')).replace("\\", "/")))
        self.pushButton_3.clicked.connect (self.processParameter)
        self.pushButton_2.clicked.connect (self.Dialog.close)
        
        self.pushButton_2.setStyleSheet("border-image: url(" + str(r_path.with_name('media').joinpath('button.png')).replace("\\", "/") + ");\n"
"font: 16pt \"黑体\";\n"
"color:white;font: bold;")
        self.pushButton_3.setStyleSheet("border-image: url(" + str(r_path.with_name('media').joinpath('button.png')).replace("\\", "/") + ");\n"
"font: 16pt \"黑体\";\n"
"color:white;font: bold;")
        
        
    def setParameter(self):
        self.spinBox.setValue (self.row)
        self.spinBox_2.setValue (self.column)
        self.spinBox_3.setValue (self.mineNum)
        self.change_minenum_limit()
        self.spinBox.valueChanged.connect(self.change_minenum_limit)
        self.spinBox_2.valueChanged.connect(self.change_minenum_limit)
        
    def change_minenum_limit(self):
        minenum_limit = self.spinBox.value () * self.spinBox_2.value () - 1
        self.spinBox_3.setValue (min(self.spinBox_3.value (), minenum_limit))
        self.spinBox_3.setMaximum(minenum_limit)

    def processParameter(self):
        r = self.spinBox.value ()
        c = self.spinBox_2.value ()
        n = self.spinBox_3.value ()
        if r != self.row or c != self.column or n != self.mineNum:
            self.alter = True
            self.row = r
            self.column = c
            self.mineNum = min (max (n, 1), r * c - 1)
        self.Dialog.close ()


if __name__ == '__main__':
    # from PyQt5.QtWidgets import QApplication
    # import sys
    # app = QApplication(sys.argv)
    # demo = ui_Form(8, 8, 10)
    # demo.Dialog.show()
    # sys.exit(app.exec_())
    ...


