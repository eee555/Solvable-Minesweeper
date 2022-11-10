# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_gs.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import configparser
from ui.ui_gameSettings import Ui_Form
from ui.uiComponents import RoundQDialog
# from PyQt5.QtWidgets import  QWidget, QDialog

class ui_Form(Ui_Form):
    def __init__(self, game_setting_path):
        self.game_setting_path = game_setting_path
        config = configparser.ConfigParser()
        config.read(game_setting_path)
        self.gameMode = config.getint('DEFAULT','gameMode')
        self.transparency = config.getint('DEFAULT','transparency')
        self.pixSize = config.getint('DEFAULT','pixSize')
        self.row = config.getint("DEFAULT", "row")
        self.column = config.getint("DEFAULT", "column")
        self.mineNum = config.getint("DEFAULT", "mineNum")
        
        self.auto_replay = config.getint("DEFAULT", "auto_replay")
        self.allow_auto_replay = config.getboolean("DEFAULT", "allow_auto_replay")
        self.auto_notification = config.getboolean("DEFAULT", "auto_notification")
        self.allow_min3BV = config.getboolean("DEFAULT", "allow_min3BV")
        self.allow_max3BV = config.getboolean("DEFAULT", "allow_max3BV")
        
        self.label = config["DEFAULT"]["label"]
        self.race_label = config["DEFAULT"]["race_label"]
        self.country = config["DEFAULT"]["country"]
        self.autosave_video = config.getboolean("DEFAULT", "autosave_video")
        self.filter_forever = config.getboolean("DEFAULT", "filter_forever")
        # self.auto_show_score = config.getint("DEFAULT", "auto_show_score") # 自动弹成绩
        self.end_then_flag = config.getboolean("DEFAULT", "end_then_flag") # 游戏结束后自动标雷
        
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
        self.Dialog = RoundQDialog()
        # self.Dialog = QDialog()
        self.setupUi (self.Dialog)
        self.setParameter ()
        self.Dialog.setWindowIcon (QtGui.QIcon ("media/cat.ico"))
        self.pushButton_yes.clicked.connect (self.processParameter)
        self.pushButton_no.clicked.connect (self.Dialog.close)

    def setParameter(self):
        self.spinBox_min_bbbv.setValue (self.min3BV)
        self.spinBox_max_bbbv.setValue (self.max3BV)
        self.spinBox_pixsize.setValue (self.pixSize)
        self.spinBox_auto_replay.setValue (self.auto_replay)
        self.checkBox_auto_replay.setChecked(self.allow_auto_replay)
        self.checkBox_auto_notification.setChecked(self.auto_notification)
        self.checkBox_allow_min3BV.setChecked(self.allow_min3BV)
        self.checkBox_allow_max3BV.setChecked(self.allow_max3BV)
        self.checkBox_autosave_video.setChecked(self.autosave_video)
        self.checkBox_filter_forever.setChecked(self.filter_forever)
        self.lineEdit_label.setText(self.label)
        self.lineEdit_race_label.setText(self.race_label)
        self.lineEdit_country.setText(self.country)
        self.checkBox_end_then_flag.setChecked(self.end_then_flag)
        self.horizontalSlider_transparency.setValue (self.transparency)
        self.label_transparency_percent_value.setText(str(self.transparency))
        # gameMode = 0，1，2，3，4，5，6，7代表：
        # 标准、win7、竞速无猜、强无猜、弱无猜、准无猜、强可猜、弱可猜
        self.comboBox_gamemode.setCurrentIndex([0, 1, 4, 3, 2, 5, 6, 7][self.gameMode])
        
    def processParameter(self):
        #只有点确定才能进来

        self.alter = True
        self.min3BV = self.spinBox_min_bbbv.value()
        self.max3BV = self.spinBox_max_bbbv.value()
        self.transparency = self.horizontalSlider_transparency.value()
        self.pixSize = self.spinBox_pixsize.value()
        
        self.auto_replay = self.spinBox_auto_replay.value()
        self.allow_auto_replay = self.checkBox_auto_replay.isChecked()
        self.auto_notification = self.checkBox_auto_notification.isChecked()
        self.allow_min3BV = self.checkBox_allow_min3BV.isChecked()
        self.allow_max3BV = self.checkBox_allow_max3BV.isChecked()
        
        self.label = self.lineEdit_label.text()
        self.race_label = self.lineEdit_race_label.text()
        self.country = self.lineEdit_country.text()
        self.autosave_video = self.checkBox_autosave_video.isChecked()
        self.filter_forever = self.checkBox_filter_forever.isChecked()
        # self.auto_show_score = config.getint("DEFAULT", "auto_show_score") # 自动弹成绩
        self.end_then_flag = self.checkBox_end_then_flag.isChecked() # 游戏结束后自动标雷
        self.gameMode = [0, 1, 4, 3, 2, 5, 6, 7][self.comboBox_gamemode.currentIndex()]
        # 标准、win7、竞速无猜、强无猜、弱无猜、准无猜、强可猜、弱可猜
        
        conf = configparser.ConfigParser()
        conf.read(self.game_setting_path)
        # conf.set("DEFAULT", "min3BV", str(self.min3BV))
        # conf.set("DEFAULT", "max3BV", str(self.max3BV))
        # conf.set("DEFAULT", "timesLimit", str(self.timesLimit))
        # conf.set("DEFAULT", "enuLimit", str(self.enuLimit))
        conf.set("DEFAULT", "gameMode", str(self.gameMode))
        conf.set("DEFAULT", "transparency", str(self.transparency))
        conf.set("DEFAULT", "pixSize", str(self.pixSize))
        
        
        
        
        
        conf.set("DEFAULT", "auto_replay", str(self.auto_replay))
        conf.set("DEFAULT", "allow_auto_replay", str(self.allow_auto_replay))
        conf.set("DEFAULT", "auto_show_score", str(self.auto_show_score))
        conf.set("DEFAULT", "auto_notification", str(self.auto_notification))
        conf.set("DEFAULT", "allow_min3BV", str(self.allow_min3BV))
        conf.set("DEFAULT", "allow_max3BV", str(self.allow_max3BV))
        
        self.label = self.lineEdit_label.text()
        self.race_label = self.lineEdit_race_label.text()
        self.country = self.lineEdit_country.text()
        self.autosave_video = self.checkBox_autosave_video.isChecked()
        self.filter_forever = self.checkBox_filter_forever.isChecked()
        # self.auto_show_score = config.getint("DEFAULT", "auto_show_score") # 自动弹成绩
        self.end_then_flag = self.checkBox_end_then_flag.isChecked()
        
        
        
        
        conf.set("DEFAULT", "gameover_flag", str(self.gameover_flag))
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
        conf.write(open(self.game_setting_path, "w"))

        self.Dialog.close ()

















