# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_about.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def __init__(self):
        self.Dialog = QtWidgets.QDialog()
        self.setupUi(self.Dialog)
        # self.Dialog.setWindowIcon (QtGui.QIcon ("media/cat.ico"))
        self.pushButton.clicked.connect (self.processParameter)
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(613, 377)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(150, 330, 281, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setMouseTracking(False)
        self.pushButton.setStyleSheet("border-image: url(media/button.png);\n"
"font: 16pt \"黑体\";color:white;font: bold;")
        self.pushButton.setAutoDefault(False)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 30, 91, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(160, 20, 301, 81))
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(40, 100, 91, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(160, 95, 371, 61))
        self.label_4.setTextFormat(QtCore.Qt.RichText)
        self.label_4.setOpenExternalLinks(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(40, 180, 531, 151))
        self.label_5.setTextFormat(QtCore.Qt.RichText)
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "确定"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600; color:#000000;\">Github: </span></p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><a href=\"https://github.com/eee555/Solvable-Minesweeper\"><span style=\" font-size:14pt; font-weight:600; color:#0000ff;\">https://github.com/eee555/<br/>Solvable-Minesweeper</span></a></p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">教程：</span></p></body></html>"))
        self.label_4.setText(_translate("Form", "<html><head/><body><p><a href=\"https://mp.weixin.qq.com/s/gh9Oxtv9eHaPTUMTDwX-fg\"><span style=\" font-size:14pt; font-weight:600; text-decoration: underline; color:#0000ff;\">https://mp.weixin.qq.com/<br/>s/gh9Oxtv9eHaPTUMTDwX-fg</span></a></p></body></html>"))
        self.label_5.setText(_translate("Form", "<html><head/><body><p align=\"justify\"><span style=\" font-size:12pt; font-weight:600;\">①软件可以无限制复制、储存、传播。营销号转载请标明<br/>本项目的github地址：<br/>https://github.com/eee555/Solvable-Minesweeper。</span></p><p align=\"justify\"><span style=\" font-size:12pt; font-weight:600;\">②任何人可以在任何一个项目中使用本项目源代码的任何<br/>一个部分。同时欢迎参与黑猫扫雷的合作设计开发。</span></p></body></html>"))

    def processParameter(self):
        self.Dialog.close()





