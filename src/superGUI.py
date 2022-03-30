from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize, QTimer
# from mineLabel import mineLabel#, mineLabel_new
# from uiComponents import StatusLabel
import configparser
from PyQt5.QtGui import QPalette, QPixmap, QFont, QIcon
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtSvg import QSvgWidget
from ui.ui_main_board import Ui_MainWindow
from pathlib import Path

class Ui_MainWindow(Ui_MainWindow):
    minimum_counter = 0 # 最小化展示窗口有关
    # windowSizeState = 'loose'  # loose or tight
    def __init__(self, MainWindow, args):
        self.mainWindow = MainWindow
        # 设置全局路径
        r_path = Path(args[0])
        self.game_setting_path = str(r_path.with_name('gameSetting.ini'))
        self.ico_path = str(r_path.with_name('media').joinpath('cat.ico'))
        self.smileface_path = str(r_path.with_name('media').joinpath('smileface.svg'))
        self.clickface_path = str(r_path.with_name('media').joinpath('clickface.svg'))
        self.lostface_path = str(r_path.with_name('media').joinpath('lostface.svg'))
        self.winface_path = str(r_path.with_name('media').joinpath('winface.svg'))
        self.smilefacedown_path = str(r_path.with_name('media').joinpath('smilefacedown.svg'))
        self.LED0_path = str(r_path.with_name('media').joinpath('LED0.png'))
        self.LED1_path = str(r_path.with_name('media').joinpath('LED1.png'))
        self.LED2_path = str(r_path.with_name('media').joinpath('LED2.png'))
        self.LED3_path = str(r_path.with_name('media').joinpath('LED3.png'))
        self.LED4_path = str(r_path.with_name('media').joinpath('LED4.png'))
        self.LED5_path = str(r_path.with_name('media').joinpath('LED5.png'))
        self.LED6_path = str(r_path.with_name('media').joinpath('LED6.png'))
        self.LED7_path = str(r_path.with_name('media').joinpath('LED7.png'))
        self.LED8_path = str(r_path.with_name('media').joinpath('LED8.png'))
        self.LED9_path = str(r_path.with_name('media').joinpath('LED9.png'))
        
        
        self.mainWindow.setWindowIcon(QIcon(self.ico_path))
        
        config = configparser.ConfigParser()
        # gameMode = 0，1，2，3，4，5，6，7代表：
        # 标准、win7、竞速无猜、强无猜、弱无猜、准无猜、强可猜、弱可猜
        if config.read(self.game_setting_path):
            self.timesLimit = config.getint('DEFAULT', 'timesLimit')
            self.enuLimit = config.getint('DEFAULT', 'enuLimit')
            self.gameMode = config.getint('DEFAULT', 'gameMode')
            self.mainWindow.setWindowOpacity((config.getint('DEFAULT', 'transparency') + 1) / 100)
            self.pixSize = config.getint('DEFAULT', 'pixSize')
            self.mainWindow.move(config.getint('DEFAULT', 'mainWinTop'), config.getint('DEFAULT', 'mainWinLeft'))
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
            self.readPredefinedBoard()
        else:
            # 找不到配置文件就初始化
            self.min3BV = 100
            self.max3BV = 381
            self.timesLimit = 1000
            self.enuLimit = 30
            self.gameMode = 0
            self.mainWindow.setWindowOpacity(1)
            self.pixSize = 20
            self.mainWindow.move(100, 200)
            self.row = 16
            self.column = 30
            self.mineNum = 99
            self.auto_replay = -1
            self.auto_show_score = 101
            self.gameover_flag = 1
            config["DEFAULT"] = {'timesLimit': 1000,
                                 'enuLimit': 30,
                                 'gameMode': 0,
                                 'transparency': 100,
                                 'pixSize': 20,
                                 'mainWinTop': 100,
                                 'mainWinLeft': 200,
                                 'row': 16,
                                 'column': 30,
                                 'mineNum': 99,
                                 "auto_replay": -1,
                                 "auto_show_score": 101,
                                 "gameover_flag": 1,
                                 }
            config["BEGINNER"] = {'min3BV': 2,
                                 'max3BV': 54,
                                 }
            config["INTERMEDIATE"] = {'min3BV': 30,
                                 'max3BV': 216,
                                 }
            config["EXPERT"] = {'min3BV': 100,
                                 'max3BV': 381,
                                 }
            config["CUSTOM"] = {'min3BV': 1,
                                'max3BV': 9999,
                                 }
            config["CUSTOM_PRESET_4"] = {'row': 16,
                                         'column': 16,
                                         'mineNum': 72,
                                         'gameMode': 2,
                                         'pixSize': 20,
                                         'timesLimit': 100000,
                                         'enuLimit': 30,
                                         'min3BV': 0,
                                         'max3BV': 9999,
                                         }
            config["CUSTOM_PRESET_5"] = {'row': 16,
                                         'column': 30,
                                         'mineNum': 120,
                                         'gameMode': 2,
                                         'pixSize': 20,
                                         'timesLimit': 100000,
                                         'enuLimit': 30,
                                         'min3BV': 0,
                                         'max3BV': 9999,
                                         }
            config["CUSTOM_PRESET_6"] = {'row': 24,
                                         'column': 36,
                                         'mineNum': 200,
                                         'gameMode': 2,
                                         'pixSize': 20,
                                         'timesLimit': 100000,
                                         'enuLimit': 30,
                                         'min3BV': 0,
                                         'max3BV': 9999,
                                         }
            with open(self.game_setting_path, 'w') as configfile:
                config.write(configfile)  # 将对象写入文件


        self.setupUi(self.mainWindow)
        self.retranslateUi(MainWindow)
        
        self.importLEDPic(self.pixSize) # 导入图片

        self.initMineArea()
        
        self.label_2.setPath(r_path)
        self.label_2.leftRelease.connect(self.gameRestart)
        self.MinenumTimeWigdet.mouseReleaseEvent = self.gameRestart

        self.label_2.setPixmap(self.pixmapNum[14])
        self.label_2.setScaledContents(True)
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.black)  # 设置字体颜色
        self.label_info.setPalette(pe)         # 最下面的框
        self.label_info.setFont(QFont("Arial", 20, QFont.Bold))
        self.label_info.setText(str(self.mineNum))

        self.frameShortcut1 = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_1), MainWindow)
        self.frameShortcut2 = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_2), MainWindow)
        self.frameShortcut3 = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_3), MainWindow)
        self.frameShortcut5 = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_4), MainWindow)
        self.frameShortcut6 = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_5), MainWindow)
        self.frameShortcut7 = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_6), MainWindow)
        self.frameShortcut4 = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F2), MainWindow)
        self.frameShortcut8 = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Space), MainWindow)
        self.frameShortcut8.setAutoRepeat(False)
        self.frameShortcut9 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Space"), MainWindow)

        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.minimumWindow()

    def initMineArea(self):

        self.label.set_rcp(self.row, self.column, self.pixSize)
        self.label.setMinimumSize(QSize(self.pixSize*self.column + 8, self.pixSize*self.row + 8))
        self.label.leftPressed.connect(self.mineAreaLeftPressed)
        self.label.leftRelease.connect(self.mineAreaLeftRelease)
        self.label.leftAndRightPressed.connect(self.mineAreaLeftAndRightPressed)
        self.label.leftAndRightRelease.connect(self.mineAreaLeftAndRightRelease)
        self.label.rightPressed.connect(self.mineAreaRightPressed)
        self.label.rightRelease.connect(self.mineAreaRightRelease)
        self.label.mouseMove.connect(self.mineMouseMove)
        self.label.mousewheelEvent.connect(self.resizeWheel)
        self.label_11.mousewheelEvent.connect(self.mineNumWheel)
        self.label_12.mousewheelEvent.connect(self.mineNumWheel)
        self.label_13.mousewheelEvent.connect(self.mineNumWheel)

        self.mainWindow.keyRelease.connect(self.mineKeyReleaseEvent)

        self.label.setObjectName("label")



    def importLEDPic(self, pixSize):
        # 导入资源，并缩放到希望的尺寸、比例
        pixmap14 = QPixmap(self.smileface_path)
        pixmap15 = QPixmap(self.clickface_path)
        pixmap16 = QPixmap(self.lostface_path)
        pixmap17 = QPixmap(self.winface_path)
        pixmap18 = QPixmap(self.smilefacedown_path)
        self.pixmapNumPix = {14: pixmap14, 15: pixmap15, 16: pixmap16, 17: pixmap17, 18: pixmap18}
        pixmap14_ = pixmap14.scaled(pixSize * 1.5, pixSize * 1.5)
        pixmap15_ = pixmap15.scaled(pixSize * 1.5, pixSize * 1.5)
        pixmap16_ = pixmap16.scaled(pixSize * 1.5, pixSize * 1.5)
        pixmap17_ = pixmap17.scaled(pixSize * 1.5, pixSize * 1.5)
        pixmap18_ = pixmap18.scaled(pixSize * 1.5, pixSize * 1.5)
        self.pixmapNum = {14: pixmap14_, 15: pixmap15_, 16: pixmap16_, 17: pixmap17_, 18: pixmap18_}
        # 以上是读取数字的图片，局面中的数字；一下是上方LED数字的图片
        pixLEDmap0 = QPixmap(self.LED0_path)
        pixLEDmap1 = QPixmap(self.LED1_path)
        pixLEDmap2 = QPixmap(self.LED2_path)
        pixLEDmap3 = QPixmap(self.LED3_path)
        pixLEDmap4 = QPixmap(self.LED4_path)
        pixLEDmap5 = QPixmap(self.LED5_path)
        pixLEDmap6 = QPixmap(self.LED6_path)
        pixLEDmap7 = QPixmap(self.LED7_path)
        pixLEDmap8 = QPixmap(self.LED8_path)
        pixLEDmap9 = QPixmap(self.LED9_path)
        self.pixmapLEDNumPix = {0: pixLEDmap0, 1: pixLEDmap1, 2: pixLEDmap2, 3: pixLEDmap3,
                        4: pixLEDmap4, 5: pixLEDmap5, 6: pixLEDmap6, 7: pixLEDmap7,
                        8: pixLEDmap8, 9: pixLEDmap9}
        pixLEDmap0_ = pixLEDmap0.copy().scaled(pixSize, pixSize * 1.75)
        pixLEDmap1_ = pixLEDmap1.copy().scaled(pixSize, pixSize * 1.75)
        pixLEDmap2_ = pixLEDmap2.copy().scaled(pixSize, pixSize * 1.75)
        pixLEDmap3_ = pixLEDmap3.copy().scaled(pixSize, pixSize * 1.75)
        pixLEDmap4_ = pixLEDmap4.copy().scaled(pixSize, pixSize * 1.75)
        pixLEDmap5_ = pixLEDmap5.copy().scaled(pixSize, pixSize * 1.75)
        pixLEDmap6_ = pixLEDmap6.copy().scaled(pixSize, pixSize * 1.75)
        pixLEDmap7_ = pixLEDmap7.copy().scaled(pixSize, pixSize * 1.75)
        pixLEDmap8_ = pixLEDmap8.copy().scaled(pixSize, pixSize * 1.75)
        pixLEDmap9_ = pixLEDmap9.copy().scaled(pixSize, pixSize * 1.75)
        self.pixmapLEDNum = {0: pixLEDmap0_, 1: pixLEDmap1_, 2: pixLEDmap2_, 3: pixLEDmap3_,
                        4: pixLEDmap4_, 5: pixLEDmap5_, 6: pixLEDmap6_, 7: pixLEDmap7_,
                        8: pixLEDmap8_, 9: pixLEDmap9_}

    def reimportLEDPic(self, pixSize):
        # 导重新入资源，并缩放到希望的尺寸、比例
        self.pixmapNum = {key:value.copy().scaled(pixSize * 1.5, pixSize * 1.5) for key,value in self.pixmapNumPix.items()}
        self.pixmapLEDNum = {key:value.copy().scaled(pixSize, pixSize * 1.75) for key,value in self.pixmapLEDNumPix.items()}


    def readPredefinedBoard(self):
        # modTable = [0,1,2,3,4,5,6,7]
        self.predefinedBoardPara = {}
        config = configparser.ConfigParser()
        config.read(self.game_setting_path)
        self.predefinedBoardPara[4] = [
            config.getint('CUSTOM_PRESET_4','gameMode'),
            config.getint('CUSTOM_PRESET_4','max3BV'),
            config.getint('CUSTOM_PRESET_4','min3BV'),
            config.getint('CUSTOM_PRESET_4','row'),
            config.getint('CUSTOM_PRESET_4','column'),
            config.getint('CUSTOM_PRESET_4','pixSize'),
            config.getint('CUSTOM_PRESET_4','timesLimit'),
            config.getint('CUSTOM_PRESET_4','enuLimit'),
            config.getint('CUSTOM_PRESET_4','mineNum'),
            ]

        self.predefinedBoardPara[5] = [
            config.getint('CUSTOM_PRESET_5','gameMode'),
            config.getint('CUSTOM_PRESET_5','max3BV'),
            config.getint('CUSTOM_PRESET_5','min3BV'),
            config.getint('CUSTOM_PRESET_5','row'),
            config.getint('CUSTOM_PRESET_5','column'),
            config.getint('CUSTOM_PRESET_5','pixSize'),
            config.getint('CUSTOM_PRESET_5','timesLimit'),
            config.getint('CUSTOM_PRESET_5','enuLimit'),
            config.getint('CUSTOM_PRESET_5','mineNum')]

        self.predefinedBoardPara[6] = [
            config.getint('CUSTOM_PRESET_6','gameMode'),
            config.getint('CUSTOM_PRESET_6','max3BV'),
            config.getint('CUSTOM_PRESET_6','min3BV'),
            config.getint('CUSTOM_PRESET_6','row'),
            config.getint('CUSTOM_PRESET_6','column'),
            config.getint('CUSTOM_PRESET_6','pixSize'),
            config.getint('CUSTOM_PRESET_6','timesLimit'),
            config.getint('CUSTOM_PRESET_6','enuLimit'),
            config.getint('CUSTOM_PRESET_6','mineNum')]
        
    def minimumWindow(self):
        # 最小化展示窗口，并固定尺寸
        # if self.windowSizeState == 'loose':
        self.label.setFixedSize(QtCore.QSize(self.pixSize*self.column + 8, self.pixSize*self.row + 8))
            # self.label.setMinimumSize(QtCore.QSize(self.pixSize*self.column + 8, self.pixSize*self.row + 8))
        self.windowSizeState = 'tight'
        self.timer_ = QTimer()
        self.timer_.timeout.connect(self.__minimumWindow)
        self.timer_.start(1)

    def __minimumWindow(self):
        self.mainWindow.setFixedSize(self.mainWindow.minimumSize())
        self.minimum_counter += 1
        if self.minimum_counter >= 100:
            self.minimum_counter = 0
            self.timer_.stop()
            

        
        
        


