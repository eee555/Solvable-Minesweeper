from ui.ui_gameSettingShortcuts import Ui_Form
import configparser
from PyQt5 import QtGui, QtWidgets
from uiComponents import RoundQDialog

# 继承自ui文件生成的原始的.py
# 减少ui文件生成的原始的.py的改动

class myGameSettingShortcuts(Ui_Form):
    def __init__(self):
        self.Dialog = RoundQDialog()
        self.setupUi(self.Dialog)
        self.setParameter()
        self.Dialog.setWindowIcon(QtGui.QIcon ("media/cat.ico"))
        self.pushButton.clicked.connect(self.processParameter)
        self.pushButton_2.clicked.connect(self.Dialog.close)
        self.alter = False

    def setParameter(self):
        config = configparser.ConfigParser()
        config.read('gameSetting.ini')

        modTable = [0,1,4,2,3,5,6,7]
        self.comboBox.setCurrentIndex(modTable[config.getint('CUSTOM_PRESET_4','gameMode')])
        self.spinBox.setProperty("value", config.getint('CUSTOM_PRESET_4','max3BV'))
        self.spinBox_2.setProperty("value", config.getint('CUSTOM_PRESET_4','min3BV'))
        self.spinBox_3.setProperty("value", config.getint('CUSTOM_PRESET_4','row'))
        self.spinBox_4.setProperty("value", config.getint('CUSTOM_PRESET_4','column'))
        self.spinBox_6.setProperty("value", config.getint('CUSTOM_PRESET_4','pixSize'))
        self.spinBox_7.setProperty("value", config.getint('CUSTOM_PRESET_4','timesLimit'))
        self.spinBox_8.setProperty("value", config.getint('CUSTOM_PRESET_4','enuLimit'))
        self.spinBox_5.setProperty("value", config.getint('CUSTOM_PRESET_4','mineNum'))

        self.comboBox_2.setCurrentIndex(modTable[config.getint('CUSTOM_PRESET_5','gameMode')])
        self.spinBox_13.setProperty("value", config.getint('CUSTOM_PRESET_5','max3BV'))
        self.spinBox_14.setProperty("value", config.getint('CUSTOM_PRESET_5','min3BV'))
        self.spinBox_15.setProperty("value", config.getint('CUSTOM_PRESET_5','row'))
        self.spinBox_16.setProperty("value", config.getint('CUSTOM_PRESET_5','column'))
        self.spinBox_9.setProperty("value", config.getint('CUSTOM_PRESET_5','pixSize'))
        self.spinBox_10.setProperty("value", config.getint('CUSTOM_PRESET_5','timesLimit'))
        self.spinBox_11.setProperty("value", config.getint('CUSTOM_PRESET_5','enuLimit'))
        self.spinBox_12.setProperty("value", config.getint('CUSTOM_PRESET_5','mineNum'))

        self.comboBox_3.setCurrentIndex(modTable[config.getint('CUSTOM_PRESET_6','gameMode')])
        self.spinBox_21.setProperty("value", config.getint('CUSTOM_PRESET_6','max3BV'))
        self.spinBox_22.setProperty("value", config.getint('CUSTOM_PRESET_6','min3BV'))
        self.spinBox_23.setProperty("value", config.getint('CUSTOM_PRESET_6','row'))
        self.spinBox_24.setProperty("value", config.getint('CUSTOM_PRESET_6','column'))
        self.spinBox_17.setProperty("value", config.getint('CUSTOM_PRESET_6','pixSize'))
        self.spinBox_18.setProperty("value", config.getint('CUSTOM_PRESET_6','timesLimit'))
        self.spinBox_19.setProperty("value", config.getint('CUSTOM_PRESET_6','enuLimit'))
        self.spinBox_20.setProperty("value", config.getint('CUSTOM_PRESET_6','mineNum'))

    def processParameter(self):
        #只有点确定才能进来
        self.alter = True

        modTable = [0,1,3,4,2,5,6,7]
        conf = configparser.ConfigParser()
        conf.read("gameSetting.ini")
        conf.set("CUSTOM_PRESET_4", "gameMode", str(modTable[self.comboBox.currentIndex()]))
        conf.set("CUSTOM_PRESET_4", "max3BV", str(self.spinBox.value()))
        conf.set("CUSTOM_PRESET_4", "min3BV", str(self.spinBox_2.value()))
        conf.set("CUSTOM_PRESET_4", "row", str(self.spinBox_3.value()))
        conf.set("CUSTOM_PRESET_4", "column", str(self.spinBox_4.value()))
        conf.set("CUSTOM_PRESET_4", "pixSize", str(self.spinBox_6.value()))
        conf.set("CUSTOM_PRESET_4", "timesLimit", str(self.spinBox_7.value()))
        conf.set("CUSTOM_PRESET_4", "enuLimit", str(self.spinBox_8.value()))
        conf.set("CUSTOM_PRESET_4", "mineNum", str(self.spinBox_5.value()))

        conf.set("CUSTOM_PRESET_5", "gameMode", str(modTable[self.comboBox_2.currentIndex()]))
        conf.set("CUSTOM_PRESET_5", "max3BV", str(self.spinBox_13.value()))
        conf.set("CUSTOM_PRESET_5", "min3BV", str(self.spinBox_14.value()))
        conf.set("CUSTOM_PRESET_5", "row", str(self.spinBox_15.value()))
        conf.set("CUSTOM_PRESET_5", "column", str(self.spinBox_16.value()))
        conf.set("CUSTOM_PRESET_5", "pixSize", str(self.spinBox_9.value()))
        conf.set("CUSTOM_PRESET_5", "timesLimit", str(self.spinBox_10.value()))
        conf.set("CUSTOM_PRESET_5", "enuLimit", str(self.spinBox_11.value()))
        conf.set("CUSTOM_PRESET_5", "mineNum", str(self.spinBox_12.value()))

        conf.set("CUSTOM_PRESET_6", "gameMode", str(modTable[self.comboBox_3.currentIndex()]))
        conf.set("CUSTOM_PRESET_6", "max3BV", str(self.spinBox_21.value()))
        conf.set("CUSTOM_PRESET_6", "min3BV", str(self.spinBox_22.value()))
        conf.set("CUSTOM_PRESET_6", "row", str(self.spinBox_23.value()))
        conf.set("CUSTOM_PRESET_6", "column", str(self.spinBox_24.value()))
        conf.set("CUSTOM_PRESET_6", "pixSize", str(self.spinBox_17.value()))
        conf.set("CUSTOM_PRESET_6", "timesLimit", str(self.spinBox_18.value()))
        conf.set("CUSTOM_PRESET_6", "enuLimit", str(self.spinBox_19.value()))
        conf.set("CUSTOM_PRESET_6", "mineNum", str(self.spinBox_20.value()))
        conf.write(open('gameSetting.ini', "w"))

        self.Dialog.close ()








