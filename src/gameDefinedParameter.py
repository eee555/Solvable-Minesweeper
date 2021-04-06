# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_defined_parameter.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def __init__(self, row, column, num):
        self.row = row
        self.column = column
        self.mineNum = num
        self.maxRow = 100
        self.maxColumn = 100
        self.alter = False
        self.Dialog = QtWidgets.QDialog()
        self.setupUi (self.Dialog)
        self.setParameter()
        self.Dialog.setWindowIcon (QtGui.QIcon ("media/mine.ico"))
        # self.pushButton.clicked.connect (self.processParameter)
        # self.pushButton_2.clicked.connect (self.Dialog.close)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 200)
        Form.setMinimumSize(QtCore.QSize(600, 200))
        Form.setMaximumSize(QtCore.QSize(600, 200))
        Form.setSizeIncrement(QtCore.QSize(0, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/cat.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setWindowOpacity(10.0)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(390, 120, 181, 51))
        self.pushButton_2.setStyleSheet("border-image: url(media/button.png);\n"
"font: 16pt \"黑体\";\n"
"color:white;font: bold;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(390, 40, 181, 51))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.pushButton_3.setStyleSheet("border-image: url(media/button.png);\n"
"font: 16pt \"黑体\";\n"
"color:white;font: bold;")
        self.pushButton_3.setAutoDefault(False)
        self.pushButton_3.setFlat(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(30, 20, 291, 157))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(7)
        self.gridLayout.setVerticalSpacing(23)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.spinBox.setFont(font)
        self.spinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox.setMinimum(6)
        self.spinBox.setMaximum(100)
        self.spinBox.setDisplayIntegerBase(10)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 0, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.spinBox_2 = QtWidgets.QSpinBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.spinBox_2.setFont(font)
        self.spinBox_2.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_2.setMinimum(6)
        self.spinBox_2.setMaximum(100)
        self.spinBox_2.setDisplayIntegerBase(10)
        self.spinBox_2.setObjectName("spinBox_2")
        self.gridLayout.addWidget(self.spinBox_2, 1, 1, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.spinBox_3 = QtWidgets.QSpinBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.spinBox_3.setFont(font)
        self.spinBox_3.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_3.setMinimum(1)
        self.spinBox_3.setMaximum(5000)
        self.spinBox_3.setDisplayIntegerBase(10)
        self.spinBox_3.setObjectName("spinBox_3")
        self.gridLayout.addWidget(self.spinBox_3, 2, 1, 1, 2)

        self.retranslateUi(Form)
        self.pushButton_2.clicked.connect(Form.close)
        self.pushButton_3.clicked.connect(self.processParameter)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "自定义设置"))
        self.pushButton_2.setText(_translate("Form", "取消"))
        self.pushButton_3.setText(_translate("Form", "确定"))
        self.label.setText(_translate("Form", "行数(row)"))
        self.label_2.setText(_translate("Form", "列数(column)"))
        self.label_3.setText(_translate("Form", "雷数(number)"))

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
    demo = Ui_Form(8, 8, 10)
    demo.Dialog.show()
    sys.exit(app.exec_())


