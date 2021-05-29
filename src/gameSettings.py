# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_gs.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import configparser
from ui.ui_gs import Ui_Form

class ui_Form(Ui_Form):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('gameSetting.ini')
        self.timesLimit = config.getint('DEFAULT','timesLimit')
        self.enuLimit = config.getint('DEFAULT','enuLimit')
        self.gameMode = config.getint('DEFAULT','gameMode')
        self.transparency = config.getint('DEFAULT','transparency')
        self.pixSize = config.getint('DEFAULT','pixSize')
        self.row = config.getint("DEFAULT", "row")
        self.column = config.getint("DEFAULT", "column")
        self.mineNum = config.getint("DEFAULT", "mineNum")
        self.auto_replay = config.getint("DEFAULT", "auto_replay") # 完成度低于该百分比炸雷自动重开
        self.auto_show_score = config.getint("DEFAULT", "auto_show_score") # 自动弹成绩
        self.gameover_flag = config.getint("DEFAULT", "gameover_flag") # 游戏结束后自动标雷
        if (self.row, self.column, self.mineNum) == (8, 8, 10):
            self.min3BV = config.getint('BEGINNER', 'min3BV')
            self.max3BV = config.getint('BEGINNER', 'max3BV')
        elif (self.row, self.column, self.mineNum) == (16, 16, 40):
            self.min3BV = config.getint('INTERMEDIATE', 'min3BV')
            self.max3BV = config.getint('INTERMEDIATE', 'max3BV')
        elif (self.row, self.column, self.mineNum) == (16, 30, 99):
            self.min3BV = config.getint('EXPERT', 'min3BV')
            self.max3BV = config.getint('EXPERT', 'max3BV')
        else:
            self.min3BV = config.getint('CUSTOM', 'min3BV')
            self.max3BV = config.getint('CUSTOM', 'max3BV')
        self.alter = False
        self.Dialog = QtWidgets.QDialog ()
        self.setupUi (self.Dialog)
        self.setParameter ()
        self.Dialog.setWindowIcon (QtGui.QIcon ("media/cat.ico"))
        self.pushButton.clicked.connect (self.processParameter)
        self.pushButton_2.clicked.connect (self.Dialog.close)

    def setParameter(self):
        self.spinBox_6.setValue (self.min3BV)
        self.spinBox_7.setValue (self.max3BV)
        self.spinBox_8.setValue (self.timesLimit)
        self.spinBox_9.setValue (self.enuLimit)
        self.spinBox_10.setValue (self.pixSize)
        self.spinBox_11.setValue (self.auto_replay)
        self.spinBox_12.setValue (self.auto_show_score)
        self.checkBox.setChecked(True if self.gameover_flag else False)
        self.horizontalSlider.setValue (self.transparency)
        self.label_7.setText(str(self.transparency))
        # gameMode = 0，1，2，3，4，5，6，7代表：
        # 标准、win7、竞速无猜、强无猜、弱无猜、准无猜、强可猜、弱可猜
        if self.gameMode == 0:
            self.radioButton.setChecked(True)
        elif self.gameMode == 1:
            self.radioButton_2.setChecked(True)
        elif self.gameMode == 2:
            self.radioButton_5.setChecked(True)
        elif self.gameMode == 3:
            self.radioButton_3.setChecked(True)
        elif self.gameMode == 4:
            self.radioButton_4.setChecked(True)
        elif self.gameMode == 5:
            self.radioButton_6.setChecked(True)
        elif self.gameMode == 6:
            self.radioButton_7.setChecked(True)
        else:
            self.radioButton_8.setChecked(True)


    def processParameter(self):
        #只有点确定才能进来

        self.alter = True
        self.min3BV = self.spinBox_6.value()  # 改到这里还没改完
        self.max3BV = int(self.lineEdit_2.text())
        self.timesLimit = int(self.lineEdit_3.text())
        self.enuLimit = int(self.lineEdit_4.text())
        self.transparency = self.horizontalSlider.value()
        self.pixSize = int(self.lineEdit_5.text())
        # gameMode = 0，1，2，3，4，5，6，7代表：
        # 标准、win7、竞速无猜、强无猜、弱无猜、准无猜、强可猜、弱可猜
        if self.radioButton.isChecked() == True:
            self.gameMode = 0
        elif self.radioButton_2.isChecked() == True:
            self.gameMode = 1
        elif self.radioButton_3.isChecked() == True:
            self.gameMode = 3
        elif self.radioButton_4.isChecked() == True:
            self.gameMode = 4
        elif self.radioButton_5.isChecked() == True:
            self.gameMode = 2
        elif self.radioButton_6.isChecked() == True:
            self.gameMode = 5
        elif self.radioButton_7.isChecked() == True:
            self.gameMode = 6
        elif self.radioButton_8.isChecked() == True:
            self.gameMode = 7

        conf = configparser.ConfigParser()
        conf.read("gameSetting.ini")
        # conf.set("DEFAULT", "min3BV", str(self.min3BV))
        # conf.set("DEFAULT", "max3BV", str(self.max3BV))
        conf.set("DEFAULT", "timesLimit", str(self.timesLimit))
        conf.set("DEFAULT", "enuLimit", str(self.enuLimit))
        conf.set("DEFAULT", "gameMode", str(self.gameMode))
        conf.set("DEFAULT", "transparency", str(self.transparency))
        conf.set("DEFAULT", "pixSize", str(self.pixSize))
        conf.write(open('gameSetting.ini', "w"))
        if (self.row, self.column, self.mineNum) == (8, 8, 10):
            conf.set("BEGINNER", "min3BV", str(self.min3BV))
            conf.set("BEGINNER", "max3BV", str(self.max3BV))
        elif (self.row, self.column, self.mineNum) == (16, 16, 40):
            conf.set("INTERMEDIATE", "min3BV", str(self.min3BV))
            conf.set("INTERMEDIATE", "max3BV", str(self.max3BV))
        elif (self.row, self.column, self.mineNum) == (16, 30, 99):
            conf.set("EXPERT", "min3BV", str(self.min3BV))
            conf.set("EXPERT", "max3BV", str(self.max3BV))
        else:
            conf.set("CUSTOM", "min3BV", str(self.min3BV))
            conf.set("CUSTOM", "max3BV", str(self.max3BV))
        conf.write(open('gameSetting.ini', "w"))

        self.Dialog.close ()

















