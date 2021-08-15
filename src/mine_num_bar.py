# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 00:34:24 2021

@author: jia32
"""

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_gs.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from uiComponents import RoundQWidget
from ui.ui_mine_num_bar import Ui_Form
from uiComponents import RoundQDialog

class ui_Form(Ui_Form):
    # barSetMineNum = QtCore.pyqtSignal(int)
    # barSetMineNumCalPoss = QtCore.pyqtSignal(int)
    def __init__(self, mine_num, size):
        self.QWidget = RoundQWidget()
        self.setupUi(self.QWidget)
        # self.setParameter ()
        
        _translate = QtCore.QCoreApplication.translate
        self.label_4.setText(_translate("Form", str(mine_num[0])))
        self.label_5.setText(_translate("Form", str(mine_num[2])))
        self.verticalSlider.setMinimum(mine_num[0])
        self.verticalSlider.setMaximum(mine_num[2])
        self.verticalSlider.setValue(mine_num[1])
        # setSingleStep
        
        # 重新设置尺寸
        self.QWidget.resize(80, size)
        self.QWidget.setMinimumSize(QtCore.QSize(80, size))
        self.QWidget.setMaximumSize(QtCore.QSize(80, size))
        self.verticalSlider.setGeometry(QtCore.QRect(30, min(size * 0.2, 35), 22, max(size * 0.6, size - 70)))
        self.label_4.setGeometry(QtCore.QRect(10, max(size * 0.9, size - 35), 51, 31))
        self.label_5.setGeometry(QtCore.QRect(10, min(size * 0.1, 3), 51, 31))

        # self.verticalSlider.valueChanged['int'].connect(self.QWidget.barSetMineNum.emit())
        # self.verticalSlider.sliderReleased['int'].connect(self.QWidget.barSetMineNumCalPoss.emit())
        

    def setSignal(self):
        # self.verticalSlider.valueChanged = self.QWidget.barSetMineNum.emit
        # self.verticalSlider.sliderReleased = self.QWidget.barSetMineNumCalPoss.emit
        self.verticalSlider.valueChanged['int'].connect(self.QWidget.barSetMineNum.emit)
        self.verticalSlider.sliderReleased.connect(self.QWidget.barSetMineNumCalPoss.emit)

    def setParameter(self):
        ...

    def processParameter(self):
        ...
        
        
        
        
        
        
        
        
        
        
        
        
        