# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_gs.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def __init__(self, min3BV, max3BV, timesLimit, enuLimit):
        self.min3BV = min3BV
        self.max3BV = max3BV
        self.timesLimit = timesLimit
        self.enuLimit = enuLimit
        self.alter = False
        self.Dialog = QtWidgets.QDialog ()
        self.setupUi ()
        self.setParameter ()
        self.Dialog.setWindowIcon (QtGui.QIcon ("media/cat.ico"))
        self.pushButton.clicked.connect (self.processParameter)
        self.pushButton_2.clicked.connect (self.Dialog.close)
    def setupUi(self):
        self.Dialog.setObjectName("Form")
        self.Dialog.resize(693, 405)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/cat.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Dialog.setWindowIcon(icon)
        self.label = QtWidgets.QLabel(self.Dialog)
        self.label.setGeometry(QtCore.QRect(280, 50, 81, 31))
        self.label.setScaledContents(False)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 72, 15))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 140, 101, 31))
        self.label_3.setScaledContents(False)
        self.label_3.setWordWrap(False)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 230, 91, 31))
        self.label_4.setScaledContents(False)
        self.label_4.setWordWrap(False)
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(self.Dialog)
        self.pushButton.setGeometry(QtCore.QRect(540, 110, 101, 51))
        self.pushButton.setStyleSheet("font: 14pt \"楷体\";border-radius:7px;border:2px groove gray;\n"
"background-color: rgb(180, 180, 180);")
        self.pushButton.setAutoDefault(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(540, 210, 101, 51))
        self.pushButton_2.setStyleSheet("font: 14pt \"楷体\";border-radius:7px;border:2px groove gray;\n"
"background-color: rgb(180, 180, 180);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit = QtWidgets.QLineEdit(self.Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(120, 60, 113, 21))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(360, 60, 113, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(120, 140, 113, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.Dialog)
        self.lineEdit_4.setGeometry(QtCore.QRect(120, 230, 113, 21))
        self.lineEdit_4.setObjectName("lineEdit_4")

        self.retranslateUi(self.Dialog)
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)

    def setParameter(self):
        self.lineEdit.setText (str(self.min3BV))
        self.lineEdit_2.setText (str(self.max3BV))
        self.lineEdit_3.setText (str(self.timesLimit))
        self.lineEdit_4.setText (str(self.enuLimit))
        
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "游戏设置"))
        self.label.setText(_translate("Form", "3BV最大值"))
        self.label_2.setText(_translate("Form", "3BV最小值"))
        self.label_3.setText(_translate("Form", "最大尝试次数"))
        self.label_4.setText(_translate("Form", "最大枚举长度"))
        self.pushButton.setText(_translate("Form", "确定"))
        self.pushButton_2.setText(_translate("Form", "取消"))
    def processParameter(self):
        a = int(self.lineEdit.text())
        b = int(self.lineEdit_2.text())
        c = int(self.lineEdit_3.text())
        d = int(self.lineEdit_4.text())
        if a != self.min3BV or b != self.max3BV or c != self.timesLimit or d!= self.enuLimit:
            self.alter = True
            self.min3BV = a
            self.max3BV = b
            self.timesLimit = c
            self.enuLimit = d
        self.Dialog.close ()

