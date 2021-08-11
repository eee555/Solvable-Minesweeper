# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_gs.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.NonModal)
        Form.resize(783, 360)
        Form.setMinimumSize(QtCore.QSize(783, 360))
        Form.setMaximumSize(QtCore.QSize(783, 360))
        Form.setMouseTracking(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/cat.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(650, 90, 111, 51))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.pushButton.setStyleSheet("border-image: url(media/button.png);\n"
"font: 16pt \"黑体\";\n"
"color:white;font: bold;")
        self.pushButton.setAutoDefault(False)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(650, 220, 111, 51))
        self.pushButton_2.setStyleSheet("border-image: url(media/button.png);\n"
"font: 16pt \"黑体\";\n"
"color:white;font: bold;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(620, 10, 20, 341))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setGeometry(QtCore.QRect(20, 230, 581, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 250, 571, 91))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.radioButton = QtWidgets.QRadioButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.radioButton.setFont(font)
        self.radioButton.setStyleSheet("QRadioButton::indicator {\n"
"    height: 14px;\n"
"    width: 14px;\n"
"    border-style:solid;\n"
"    border-radius:7px;\n"
"    border-width: 1px;\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    border-color: #48a5fd;\n"
"    background-color: qradialgradient(cx:0.5, cy:0.5, radius:0.4,fx:0.5, fy:0.5, stop:0 #ffffff, stop:0.5 #ffffff, stop:0.6 #48a5fd, stop:1 #48a5fd);\n"
"}\n"
"QRadioButton::indicator:!checked {\n"
"    border-color: #a9b7c6;\n"
"    background-color: #fbfdfa;\n"
"}")
        self.radioButton.setObjectName("radioButton")
        self.gridLayout.addWidget(self.radioButton, 0, 0, 1, 1)
        self.radioButton_7 = QtWidgets.QRadioButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.radioButton_7.setFont(font)
        self.radioButton_7.setStyleSheet("QRadioButton::indicator {\n"
"    height: 14px;\n"
"    width: 14px;\n"
"    border-style:solid;\n"
"    border-radius:7px;\n"
"    border-width: 1px;\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    border-color: #48a5fd;\n"
"    background-color: qradialgradient(cx:0.5, cy:0.5, radius:0.4,fx:0.5, fy:0.5, stop:0 #ffffff, stop:0.5 #ffffff, stop:0.6 #48a5fd, stop:1 #48a5fd);\n"
"}\n"
"QRadioButton::indicator:!checked {\n"
"    border-color: #a9b7c6;\n"
"    background-color: #fbfdfa;\n"
"}")
        self.radioButton_7.setObjectName("radioButton_7")
        self.gridLayout.addWidget(self.radioButton_7, 0, 3, 1, 1)
        self.radioButton_4 = QtWidgets.QRadioButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.radioButton_4.setFont(font)
        self.radioButton_4.setStyleSheet("QRadioButton::indicator {\n"
"    height: 14px;\n"
"    width: 14px;\n"
"    border-style:solid;\n"
"    border-radius:7px;\n"
"    border-width: 1px;\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    border-color: #48a5fd;\n"
"    background-color: qradialgradient(cx:0.5, cy:0.5, radius:0.4,fx:0.5, fy:0.5, stop:0 #ffffff, stop:0.5 #ffffff, stop:0.6 #48a5fd, stop:1 #48a5fd);\n"
"}\n"
"QRadioButton::indicator:!checked {\n"
"    border-color: #a9b7c6;\n"
"    background-color: #fbfdfa;\n"
"}")
        self.radioButton_4.setObjectName("radioButton_4")
        self.gridLayout.addWidget(self.radioButton_4, 1, 1, 1, 1)
        self.radioButton_5 = QtWidgets.QRadioButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.radioButton_5.setFont(font)
        self.radioButton_5.setStyleSheet("QRadioButton::indicator {\n"
"    height: 14px;\n"
"    width: 14px;\n"
"    border-style:solid;\n"
"    border-radius:7px;\n"
"    border-width: 1px;\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    border-color: #48a5fd;\n"
"    background-color: qradialgradient(cx:0.5, cy:0.5, radius:0.4,fx:0.5, fy:0.5, stop:0 #ffffff, stop:0.5 #ffffff, stop:0.6 #48a5fd, stop:1 #48a5fd);\n"
"}\n"
"QRadioButton::indicator:!checked {\n"
"    border-color: #a9b7c6;\n"
"    background-color: #fbfdfa;\n"
"}")
        self.radioButton_5.setObjectName("radioButton_5")
        self.gridLayout.addWidget(self.radioButton_5, 0, 2, 1, 1)
        self.radioButton_8 = QtWidgets.QRadioButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.radioButton_8.setFont(font)
        self.radioButton_8.setStyleSheet("QRadioButton::indicator {\n"
"    height: 14px;\n"
"    width: 14px;\n"
"    border-style:solid;\n"
"    border-radius:7px;\n"
"    border-width: 1px;\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    border-color: #48a5fd;\n"
"    background-color: qradialgradient(cx:0.5, cy:0.5, radius:0.4,fx:0.5, fy:0.5, stop:0 #ffffff, stop:0.5 #ffffff, stop:0.6 #48a5fd, stop:1 #48a5fd);\n"
"}\n"
"QRadioButton::indicator:!checked {\n"
"    border-color: #a9b7c6;\n"
"    background-color: #fbfdfa;\n"
"}")
        self.radioButton_8.setObjectName("radioButton_8")
        self.gridLayout.addWidget(self.radioButton_8, 1, 3, 1, 1)
        self.radioButton_2 = QtWidgets.QRadioButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setStyleSheet("QRadioButton::indicator {\n"
"    height: 14px;\n"
"    width: 14px;\n"
"    border-style:solid;\n"
"    border-radius:7px;\n"
"    border-width: 1px;\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    border-color: #48a5fd;\n"
"    background-color: qradialgradient(cx:0.5, cy:0.5, radius:0.4,fx:0.5, fy:0.5, stop:0 #ffffff, stop:0.5 #ffffff, stop:0.6 #48a5fd, stop:1 #48a5fd);\n"
"}\n"
"QRadioButton::indicator:!checked {\n"
"    border-color: #a9b7c6;\n"
"    background-color: #fbfdfa;\n"
"}")
        self.radioButton_2.setObjectName("radioButton_2")
        self.gridLayout.addWidget(self.radioButton_2, 1, 0, 1, 1)
        self.radioButton_3 = QtWidgets.QRadioButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.radioButton_3.setFont(font)
        self.radioButton_3.setStyleSheet("QRadioButton::indicator {\n"
"    height: 14px;\n"
"    width: 14px;\n"
"    border-style:solid;\n"
"    border-radius:7px;\n"
"    border-width: 1px;\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    border-color: #48a5fd;\n"
"    background-color: qradialgradient(cx:0.5, cy:0.5, radius:0.4,fx:0.5, fy:0.5, stop:0 #ffffff, stop:0.5 #ffffff, stop:0.6 #48a5fd, stop:1 #48a5fd);\n"
"}\n"
"QRadioButton::indicator:!checked {\n"
"    border-color: #a9b7c6;\n"
"    background-color: #fbfdfa;\n"
"}")
        self.radioButton_3.setObjectName("radioButton_3")
        self.gridLayout.addWidget(self.radioButton_3, 0, 1, 1, 1)
        self.radioButton_6 = QtWidgets.QRadioButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.radioButton_6.setFont(font)
        self.radioButton_6.setStyleSheet("QRadioButton::indicator {\n"
"    height: 14px;\n"
"    width: 14px;\n"
"    border-style:solid;\n"
"    border-radius:7px;\n"
"    border-width: 1px;\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    border-color: #48a5fd;\n"
"    background-color: qradialgradient(cx:0.5, cy:0.5, radius:0.4,fx:0.5, fy:0.5, stop:0 #ffffff, stop:0.5 #ffffff, stop:0.6 #48a5fd, stop:1 #48a5fd);\n"
"}\n"
"QRadioButton::indicator:!checked {\n"
"    border-color: #a9b7c6;\n"
"    background-color: #fbfdfa;\n"
"}")
        self.radioButton_6.setObjectName("radioButton_6")
        self.gridLayout.addWidget(self.radioButton_6, 1, 2, 1, 1)
        self.horizontalSlider = QtWidgets.QSlider(Form)
        self.horizontalSlider.setGeometry(QtCore.QRect(390, 195, 160, 22))
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(320, 190, 71, 31))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setScaledContents(False)
        self.label_5.setWordWrap(False)
        self.label_5.setObjectName("label_5")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(545, 190, 41, 31))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_7.setText("")
        self.label_7.setScaledContents(False)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setWordWrap(False)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(590, 190, 21, 31))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setScaledContents(False)
        self.label_8.setWordWrap(False)
        self.label_8.setObjectName("label_8")
        self.layoutWidget1 = QtWidgets.QWidget(Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(30, 30, 253, 155))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.spinBox_6 = QtWidgets.QSpinBox(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_6.sizePolicy().hasHeightForWidth())
        self.spinBox_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.spinBox_6.setFont(font)
        self.spinBox_6.setStyleSheet("border-width: 2px;\n"
"border-radius: 8px;\n"
"border-style: solid;\n"
"border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"border-right-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"border-left-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"background-color: #f4f4f4;\n"
"color: #3d3d3d;")
        self.spinBox_6.setFrame(True)
        self.spinBox_6.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_6.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_6.setKeyboardTracking(True)
        self.spinBox_6.setProperty("showGroupSeparator", False)
        self.spinBox_6.setMinimum(0)
        self.spinBox_6.setMaximum(9999)
        self.spinBox_6.setProperty("value", 0)
        self.spinBox_6.setObjectName("spinBox_6")
        self.gridLayout_2.addWidget(self.spinBox_6, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setScaledContents(False)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.spinBox_7 = QtWidgets.QSpinBox(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_7.sizePolicy().hasHeightForWidth())
        self.spinBox_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.spinBox_7.setFont(font)
        self.spinBox_7.setStyleSheet("border-width: 2px;\n"
"border-radius: 8px;\n"
"border-style: solid;\n"
"border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"border-right-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"border-left-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"background-color: #f4f4f4;\n"
"color: #3d3d3d;")
        self.spinBox_7.setFrame(True)
        self.spinBox_7.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_7.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_7.setKeyboardTracking(True)
        self.spinBox_7.setProperty("showGroupSeparator", False)
        self.spinBox_7.setMinimum(0)
        self.spinBox_7.setMaximum(9999)
        self.spinBox_7.setProperty("value", 9999)
        self.spinBox_7.setObjectName("spinBox_7")
        self.gridLayout_2.addWidget(self.spinBox_7, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setScaledContents(False)
        self.label_3.setWordWrap(False)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.spinBox_8 = QtWidgets.QSpinBox(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_8.sizePolicy().hasHeightForWidth())
        self.spinBox_8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.spinBox_8.setFont(font)
        self.spinBox_8.setStyleSheet("border-width: 2px;\n"
"border-radius: 8px;\n"
"border-style: solid;\n"
"border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"border-right-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"border-left-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"background-color: #f4f4f4;\n"
"color: #3d3d3d;")
        self.spinBox_8.setFrame(True)
        self.spinBox_8.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_8.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_8.setKeyboardTracking(True)
        self.spinBox_8.setProperty("showGroupSeparator", False)
        self.spinBox_8.setMinimum(0)
        self.spinBox_8.setMaximum(99999999)
        self.spinBox_8.setProperty("value", 50000)
        self.spinBox_8.setObjectName("spinBox_8")
        self.gridLayout_2.addWidget(self.spinBox_8, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setToolTipDuration(0)
        self.label_4.setScaledContents(False)
        self.label_4.setWordWrap(False)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)
        self.spinBox_9 = QtWidgets.QSpinBox(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_9.sizePolicy().hasHeightForWidth())
        self.spinBox_9.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.spinBox_9.setFont(font)
        self.spinBox_9.setStyleSheet("border-width: 2px;\n"
"border-radius: 8px;\n"
"border-style: solid;\n"
"border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"border-right-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"border-left-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"background-color: #f4f4f4;\n"
"color: #3d3d3d;")
        self.spinBox_9.setFrame(True)
        self.spinBox_9.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_9.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_9.setKeyboardTracking(True)
        self.spinBox_9.setProperty("showGroupSeparator", False)
        self.spinBox_9.setMinimum(0)
        self.spinBox_9.setMaximum(200)
        self.spinBox_9.setProperty("value", 30)
        self.spinBox_9.setObjectName("spinBox_9")
        self.gridLayout_2.addWidget(self.spinBox_9, 3, 1, 1, 1)
        self.layoutWidget2 = QtWidgets.QWidget(Form)
        self.layoutWidget2.setGeometry(QtCore.QRect(340, 30, 241, 115))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_6.setMinimumSize(QtCore.QSize(100, 0))
        self.label_6.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setScaledContents(False)
        self.label_6.setWordWrap(False)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 1)
        self.spinBox_10 = QtWidgets.QSpinBox(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_10.sizePolicy().hasHeightForWidth())
        self.spinBox_10.setSizePolicy(sizePolicy)
        self.spinBox_10.setMinimumSize(QtCore.QSize(124, 0))
        self.spinBox_10.setMaximumSize(QtCore.QSize(124, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.spinBox_10.setFont(font)
        self.spinBox_10.setStyleSheet("border-width: 2px;\n"
"border-radius: 8px;\n"
"border-style: solid;\n"
"border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"border-right-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"border-left-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"background-color: #f4f4f4;\n"
"color: #3d3d3d;")
        self.spinBox_10.setFrame(True)
        self.spinBox_10.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_10.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_10.setKeyboardTracking(True)
        self.spinBox_10.setProperty("showGroupSeparator", False)
        self.spinBox_10.setMinimum(1)
        self.spinBox_10.setMaximum(200)
        self.spinBox_10.setProperty("value", 20)
        self.spinBox_10.setObjectName("spinBox_10")
        self.gridLayout_3.addWidget(self.spinBox_10, 0, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setToolTipDuration(0)
        self.label_9.setScaledContents(False)
        self.label_9.setWordWrap(False)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 1, 0, 1, 1)
        self.spinBox_11 = QtWidgets.QSpinBox(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_11.sizePolicy().hasHeightForWidth())
        self.spinBox_11.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.spinBox_11.setFont(font)
        self.spinBox_11.setStyleSheet("border-width: 2px;\n"
"border-radius: 8px;\n"
"border-style: solid;\n"
"border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"border-right-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"border-left-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"background-color: #f4f4f4;\n"
"color: #3d3d3d;")
        self.spinBox_11.setFrame(True)
        self.spinBox_11.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_11.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_11.setKeyboardTracking(True)
        self.spinBox_11.setProperty("showGroupSeparator", False)
        self.spinBox_11.setMinimum(-1)
        self.spinBox_11.setMaximum(100)
        self.spinBox_11.setProperty("value", 30)
        self.spinBox_11.setObjectName("spinBox_11")
        self.gridLayout_3.addWidget(self.spinBox_11, 1, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.label_10.setFont(font)
        self.label_10.setToolTipDuration(0)
        self.label_10.setScaledContents(False)
        self.label_10.setWordWrap(False)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 2, 0, 1, 1)
        self.spinBox_12 = QtWidgets.QSpinBox(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_12.sizePolicy().hasHeightForWidth())
        self.spinBox_12.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.spinBox_12.setFont(font)
        self.spinBox_12.setStyleSheet("border-width: 2px;\n"
"border-radius: 8px;\n"
"border-style: solid;\n"
"border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"border-right-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"border-left-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"background-color: #f4f4f4;\n"
"color: #3d3d3d;")
        self.spinBox_12.setFrame(True)
        self.spinBox_12.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_12.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_12.setKeyboardTracking(True)
        self.spinBox_12.setProperty("showGroupSeparator", False)
        self.spinBox_12.setMinimum(0)
        self.spinBox_12.setMaximum(101)
        self.spinBox_12.setProperty("value", 101)
        self.spinBox_12.setObjectName("spinBox_12")
        self.gridLayout_3.addWidget(self.spinBox_12, 2, 1, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setGeometry(QtCore.QRect(350, 160, 151, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.checkBox.setFont(font)
        self.checkBox.setStyleSheet("")
        self.checkBox.setObjectName("checkBox")

        self.retranslateUi(Form)
        self.horizontalSlider.valueChanged['int'].connect(self.label_7.setNum)
        self.pushButton_2.clicked.connect(Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "游戏设置"))
        self.pushButton.setText(_translate("Form", "确定"))
        self.pushButton_2.setText(_translate("Form", "取消"))
        self.radioButton.setText(_translate("Form", "标准"))
        self.radioButton_7.setText(_translate("Form", "强可猜"))
        self.radioButton_4.setText(_translate("Form", "弱无猜"))
        self.radioButton_5.setText(_translate("Form", "竞速无猜"))
        self.radioButton_8.setText(_translate("Form", "弱可猜"))
        self.radioButton_2.setText(_translate("Form", "Win7"))
        self.radioButton_3.setText(_translate("Form", "强无猜"))
        self.radioButton_6.setText(_translate("Form", "准无猜"))
        self.label_5.setText(_translate("Form", "透明度"))
        self.label_8.setText(_translate("Form", "%"))
        self.label_2.setText(_translate("Form", "3BV最小值"))
        self.label.setText(_translate("Form", "3BV最大值"))
        self.label_3.setText(_translate("Form", "最大尝试次数"))
        self.label_4.setToolTip(_translate("Form", "<html><head/><body><p>仅对于强无猜、竞速无猜、强可猜，本参数生效。众所周知，判<span style=\" font-family:\'-apple-system\',\'SF UI Text\',\'Arial\',\'PingFang SC\',\'Hiragino Sans GB\',\'Microsoft YaHei\',\'WenQuanYi Micro Hei\',\'sans-serif\'; font-size:14px; color:#222226; background-color:#ffffff;\">\\r\\n</span>雷是NP难题，即一种不可简化的、在有限长时间内无法计算出的<span style=\" font-family:\'-apple-system\',\'SF UI Text\',\'Arial\',\'PingFang SC\',\'Hiragino Sans GB\',\'Microsoft YaHei\',\'WenQuanYi Micro Hei\',\'sans-serif\'; font-size:14px; color:#222226; background-color:#ffffff;\">\\r\\n</span>问题。这就意味着，有时即使局面的确存在解，也不存在任何算<span style=\" font-family:\'-apple-system\',\'SF UI Text\',\'Arial\',\'PingFang SC\',\'Hiragino Sans GB\',\'Microsoft YaHei\',\'WenQuanYi Micro Hei\',\'sans-serif\'; font-size:14px; color:#222226; background-color:#ffffff;\">\\r\\n</span>法可以计算出。软件内部集成了三大判雷引擎，采用了高效的判<span style=\" font-family:\'-apple-system\',\'SF UI Text\',\'Arial\',\'PingFang SC\',\'Hiragino Sans GB\',\'Microsoft YaHei\',\'WenQuanYi Micro Hei\',\'sans-serif\'; font-size:14px; color:#222226; background-color:#ffffff;\">\\r\\n</span>雷算法，但即使如此，如果有太多个方格相邻，其数量超过最大<span style=\" font-family:\'-apple-system\',\'SF UI Text\',\'Arial\',\'PingFang SC\',\'Hiragino Sans GB\',\'Microsoft YaHei\',\'WenQuanYi Micro Hei\',\'sans-serif\'; font-size:14px; color:#222226; background-color:#ffffff;\">\\r\\n</span>枚举长度，且不能分割，算法便会放弃枚举。这个数值的推荐值<span style=\" font-family:\'-apple-system\',\'SF UI Text\',\'Arial\',\'PingFang SC\',\'Hiragino Sans GB\',\'Microsoft YaHei\',\'WenQuanYi Micro Hei\',\'sans-serif\'; font-size:14px; color:#222226; background-color:#ffffff;\">\\r\\n</span>为20~35</p></body></html>"))
        self.label_4.setText(_translate("Form", "最大枚举长度"))
        self.label_6.setText(_translate("Form", "方格边长"))
        self.label_9.setToolTip(_translate("Form", "完成度小于等于此百分比局面自动重开"))
        self.label_9.setText(_translate("Form", "自动重开"))
        self.label_10.setToolTip(_translate("Form", "完成度大于等于此百分比的局面自动弹窗"))
        self.label_10.setText(_translate("Form", "自动弹窗"))
        self.checkBox.setText(_translate("Form", "结束后标雷"))
