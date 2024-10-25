from ui.ui_gameSettingShortcuts import Ui_Form
import configparser
from PyQt5 import QtGui
from ui.uiComponents import RoundQDialog

# 继承自ui文件生成的原始的.py
# 减少ui文件生成的原始的.py的改动

class myGameSettingShortcuts(Ui_Form):
    def __init__(self, game_setting_path, ico_path, r_path, parent):
        self.game_setting_path = game_setting_path
        self.r_path = r_path
        self.Dialog = RoundQDialog(parent)
        self.setupUi(self.Dialog)
        self.setParameter()
        self.Dialog.setWindowIcon(QtGui.QIcon (ico_path))
        self.pushButton.clicked.connect(self.processParameter)
        self.pushButton_2.clicked.connect(self.Dialog.close)
        self.alter = False

    def setParameter(self):
        config = configparser.ConfigParser()
        config.read(self.game_setting_path, encoding='utf-8')

        # modTable = [0,1,4,2,3,5,6,7]
        modTable = [0,0,0,0,1,4,2,3,5,6,7]
        self.comboBox_gamemode4.setCurrentIndex(modTable[config.getint('CUSTOM_PRESET_4','gameMode')])
        self.spinBox_height4.setProperty("value", config.getint('CUSTOM_PRESET_4','row'))
        self.spinBox_width4.setProperty("value", config.getint('CUSTOM_PRESET_4','column'))
        self.spinBox_pixsize4.setProperty("value", config.getint('CUSTOM_PRESET_4','pixSize'))
        self.spinBox_attempt_times_limit4.setProperty("value", config.getint('CUSTOM_PRESET_4','attempt_times_limit'))
        self.spinBox_minenum4.setProperty("value", config.getint('CUSTOM_PRESET_4','mineNum'))
        self.lineEdit_constraint4.setProperty("value", config["CUSTOM_PRESET_4"]["board_constraint"])

        self.comboBox_gamemode5.setCurrentIndex(modTable[config.getint('CUSTOM_PRESET_5','gameMode')])
        self.spinBox_height5.setProperty("value", config.getint('CUSTOM_PRESET_5','row'))
        self.spinBox_width5.setProperty("value", config.getint('CUSTOM_PRESET_5','column'))
        self.spinBox_pixsize5.setProperty("value", config.getint('CUSTOM_PRESET_5','pixSize'))
        self.spinBox_attempt_times_limit5.setProperty("value", config.getint('CUSTOM_PRESET_5','attempt_times_limit'))
        self.spinBox_minenum5.setProperty("value", config.getint('CUSTOM_PRESET_5','mineNum'))
        self.lineEdit_constraint5.setProperty("value", config["CUSTOM_PRESET_5"]["board_constraint"])

        self.comboBox_gamemode6.setCurrentIndex(modTable[config.getint('CUSTOM_PRESET_6','gameMode')])
        self.spinBox_height6.setProperty("value", config.getint('CUSTOM_PRESET_6','row'))
        self.spinBox_width6.setProperty("value", config.getint('CUSTOM_PRESET_6','column'))
        self.spinBox_pixsize6.setProperty("value", config.getint('CUSTOM_PRESET_6','pixSize'))
        self.spinBox_attempt_times_limit6.setProperty("value", config.getint('CUSTOM_PRESET_6','attempt_times_limit'))
        self.spinBox_minenum6.setProperty("value", config.getint('CUSTOM_PRESET_6','mineNum'))
        self.lineEdit_constraint6.setProperty("value", config["CUSTOM_PRESET_6"]["board_constraint"])
        
        self.pushButton.setStyleSheet("border-image: url(" + str(self.r_path.with_name('media').joinpath('button.png')).replace("\\", "/") + ");\n"
"font: 16pt \"黑体\";\n"
"color:white;font: bold;")
        self.pushButton_2.setStyleSheet("border-image: url(" + str(self.r_path.with_name('media').joinpath('button.png')).replace("\\", "/") + ");\n"
"font: 16pt \"黑体\";\n"
"color:white;font: bold;")
        
    def processParameter(self):
        #只有点确定才能进来
        self.alter = True

        # modTable = [0,1,3,4,2,5,6,7]
        modTable = [0,4,6,7,5,8,9,10]
        conf = configparser.ConfigParser()
        conf.read(self.game_setting_path, encoding='utf-8')
        conf.set("CUSTOM_PRESET_4", "gameMode", str(modTable[self.comboBox_gamemode4.currentIndex()]))
        conf.set("CUSTOM_PRESET_4", "row", str(self.spinBox_height4.value()))
        conf.set("CUSTOM_PRESET_4", "column", str(self.spinBox_width4.value()))
        conf.set("CUSTOM_PRESET_4", "pixSize", str(self.spinBox_pixsize4.value()))
        conf.set("CUSTOM_PRESET_4", "attempt_times_limit", str(self.spinBox_attempt_times_limit4.value()))
        conf.set("CUSTOM_PRESET_4", "mineNum", str(self.spinBox_minenum4.value()))
        conf.set("CUSTOM_PRESET_4", "board_constraint", self.lineEdit_constraint4.text())

        conf.set("CUSTOM_PRESET_5", "gameMode", str(modTable[self.comboBox_gamemode5.currentIndex()]))
        conf.set("CUSTOM_PRESET_5", "row", str(self.spinBox_height5.value()))
        conf.set("CUSTOM_PRESET_5", "column", str(self.spinBox_width5.value()))
        conf.set("CUSTOM_PRESET_5", "pixSize", str(self.spinBox_pixsize5.value()))
        conf.set("CUSTOM_PRESET_5", "attempt_times_limit", str(self.spinBox_attempt_times_limit5.value()))
        conf.set("CUSTOM_PRESET_5", "mineNum", str(self.spinBox_minenum5.value()))
        conf.set("CUSTOM_PRESET_5", "board_constraint", self.lineEdit_constraint5.text())

        conf.set("CUSTOM_PRESET_6", "gameMode", str(modTable[self.comboBox_gamemode6.currentIndex()]))
        conf.set("CUSTOM_PRESET_6", "row", str(self.spinBox_height6.value()))
        conf.set("CUSTOM_PRESET_6", "column", str(self.spinBox_width6.value()))
        conf.set("CUSTOM_PRESET_6", "pixSize", str(self.spinBox_pixsize6.value()))
        conf.set("CUSTOM_PRESET_6", "attempt_times_limit", str(self.spinBox_attempt_times_limit6.value()))
        conf.set("CUSTOM_PRESET_6", "mineNum", str(self.spinBox_minenum6.value()))
        conf.set("CUSTOM_PRESET_6", "board_constraint", self.lineEdit_constraint6.text())
        conf.write(open(self.game_setting_path, "w", encoding='utf-8'))

        self.Dialog.close ()








