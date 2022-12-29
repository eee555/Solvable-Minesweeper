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
from gameScoreBoard import gameScoreBoardManager
import minesweeper_master as mm

class Ui_MainWindow(Ui_MainWindow):
    minimum_counter = 0 # 最小化展示窗口有关
    # windowSizeState = 'loose'  # loose or tight
    def __init__(self, MainWindow, args):
        self.mainWindow = MainWindow
        # 设置全局路径
        r_path = Path(args[0])
        # 录像保存位置
        self.replay_path = str(r_path.with_name('replay'))
        # 记录了全局游戏设置
        self.game_setting_path = str(r_path.with_name('gameSetting.ini'))
        # 记录了计数器的配置，显示哪些指标等等
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

        self.predefinedBoardPara = [{}] * 7
        # 缓存了6套游戏模式的配置，以减少快捷键切换模式时的io
        config = configparser.ConfigParser()
        # gameMode = 0，1，2，3，4，5，6，7代表：
        # 标准、win7、竞速无猜、强无猜、弱无猜、准无猜、强可猜、弱可猜
        
    
        
        
        
        
        if config.read(self.game_setting_path):
            self.gameMode = config.getint('DEFAULT', 'gameMode')
            self.mainWindow.setWindowOpacity((config.getint('DEFAULT', 'transparency') + 1) / 100)
            self.pixSize = config.getint('DEFAULT', 'pixSize')
            self.mainWindow.move(config.getint('DEFAULT', 'mainWinTop'), config.getint('DEFAULT', 'mainWinLeft'))
            # self.score_board_manager.ui.QWidget.move(config.getint('DEFAULT', 'scoreBoardTop'),
            #                                          config.getint('DEFAULT', 'scoreBoardLeft'))
            _scoreBoardTop = config.getint('DEFAULT', 'scoreBoardTop')
            _scoreBoardLeft = config.getint('DEFAULT', 'scoreBoardLeft')
            self.row = config.getint("DEFAULT", "row")
            self.column = config.getint("DEFAULT", "column")
            self.mineNum = config.getint("DEFAULT", "mineNum")
            # 完成度低于该百分比炸雷自动重开
            if config.getboolean("DEFAULT", "allow_auto_replay"):
                self.auto_replay = config.getint("DEFAULT", "auto_replay")
            else:
                self.auto_replay = -1
            self.auto_notification = config.getboolean("DEFAULT", "auto_notification")
            
            self.player_designator = config["DEFAULT"]["player_designator"]
            self.race_designator = config["DEFAULT"]["race_designator"]
            self.country = config["DEFAULT"]["country"]
            self.autosave_video = config.getboolean("DEFAULT", "autosave_video")
            self.filter_forever = config.getboolean("DEFAULT", "filter_forever")
            # self.auto_show_score = config.getint("DEFAULT", "auto_show_score") # 自动弹成绩
            self.end_then_flag = config.getboolean("DEFAULT", "end_then_flag") # 游戏结束后自动标雷
            
            if (self.row, self.column, self.mineNum) == (8, 8, 10):
                self.board_constraint = config["BEGINNER"]["board_constraint"]
                self.attempt_times_limit = config.getint('BEGINNER', 'attempt_times_limit')
            elif (self.row, self.column, self.mineNum) == (16, 16, 40):
                self.board_constraint = config["INTERMEDIATE"]["board_constraint"]
                self.attempt_times_limit = config.getint('INTERMEDIATE', 'attempt_times_limit')
            elif (self.row, self.column, self.mineNum) == (16, 30, 99):
                self.board_constraint = config["EXPERT"]["board_constraint"]
                self.attempt_times_limit = config.getint('EXPERT', 'attempt_times_limit')
            else:
                self.board_constraint = config["CUSTOM"]["board_constraint"]
                self.attempt_times_limit = config.getint('CUSTOM', 'attempt_times_limit')
        else:
            # 找不到配置文件就初始化
            self.min3BV = 100
            self.max3BV = 381
            self.gameMode = 0
            self.mainWindow.setWindowOpacity(1)
            self.pixSize = 20
            self.mainWindow.move(100, 200)
            self.row = 16
            self.column = 30
            self.mineNum = 99
            self.auto_replay = 30
            self.allow_auto_replay = False
            self.auto_notification = True
            self.allow_min3BV = False
            self.allow_max3BV = False
            self.player_designator = "匿名玩家(anonymous player)"
            self.race_designator = ""
            self.country = "未知(unknow)"
            self.autosave_video = True
            self.filter_forever = False
            self.end_then_flag = True
            config["DEFAULT"] = {'gameMode': 0,
                                 'transparency': 100,
                                 'pixSize': 20,
                                 'mainWinTop': 100,
                                 'mainWinLeft': 200,
                                 'scoreBoardTop': 100,
                                 'scoreBoardLeft': 100,
                                 'row': 16,
                                 'column': 30,
                                 'mineNum': 99,
                                 "auto_replay": 30,
                                 "allow_auto_replay": False,
                                 "auto_notification": True,
                                 # "board_constraint": "",
                                 # "attempt_times_limit": 0,
                                 "player_designator": "匿名玩家(anonymous player)",
                                 "race_designator": "",
                                 "country": "未知(unknow)",
                                 "autosave_video": True,
                                 "filter_forever": False,
                                 "end_then_flag": True,
                                 }
            config["BEGINNER"] = {"board_constraint": "",
                                  "attempt_times_limit": 100000,
                                  }
            config["INTERMEDIATE"] = {"board_constraint": "",
                                      "attempt_times_limit": 100000,
                                      }
            config["EXPERT"] = {"board_constraint": "",
                                "attempt_times_limit": 100000,
                                }
            config["CUSTOM"] = {"board_constraint": "",
                                "attempt_times_limit": 100000,
                                 }
            config["CUSTOM_PRESET_4"] = {'row': 16,
                                         'column': 16,
                                         'minenum': 72,
                                         'gameMode': 5,
                                         'pixSize': 20,
                                         "board_constraint": "",
                                         "attempt_times_limit": 100000,
                                         }
            config["CUSTOM_PRESET_5"] = {'row': 16,
                                         'column': 30,
                                         'minenum': 120,
                                         'gamemode': 5,
                                         'pixsize': 20,
                                         "board_constraint": "",
                                         "attempt_times_limit": 100000,
                                         }
            config["CUSTOM_PRESET_6"] = {'row': 24,
                                         'column': 36,
                                         'minenum': 200,
                                         'gamemode': 5,
                                         'pixsize': 20,
                                         "board_constraint": "",
                                         "attempt_times_limit": 100000,
                                         }
            with open(self.game_setting_path, 'w') as configfile:
                config.write(configfile)  # 将对象写入文件
              
        
        self.readPredefinedBoardPara()
        self.setupUi(self.mainWindow)
        self.retranslateUi(MainWindow)
                
        score_board_path = str(r_path.with_name('scoreBoardSetting.ini'))
        self.score_board_manager = gameScoreBoardManager(score_board_path,
                                                         self.game_setting_path, 
                                                         self.pixSize)
        self.score_board_manager.ui.QWidget.move(_scoreBoardTop, _scoreBoardLeft)
        
                
        self.score_board_manager.with_namespace({
            "race_designator": self.race_designator,
            "mode": mm.trans_game_mode(self.gameMode),
            })
        
        self.importLEDPic(self.pixSize) # 导入图片
        self.label.setPath(r_path)
        self.initMineArea()


        self.label_2.setPath(r_path)
        self.label_2.leftRelease.connect(self.gameRestart)
        self.MinenumTimeWigdet.mouseReleaseEvent = self.gameRestart

        self.label_2.setPixmap(self.pixmapNum[14])
        self.label_2.setScaledContents(True)
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.black)  # 设置字体颜色
        self.label_info.setPalette(pe)         # 最下面的框
        # self.label_info.setFont(QFont("Arial", 20, QFont.Bold))
        # self.label_info.setText(str(self.mineNum))
        
        self.label_info.setText(self.player_designator)

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
        self.shortcut_hidden_score_board = QtWidgets.QShortcut(
            QtGui.QKeySequence(QtCore.Qt.Key_Slash), MainWindow) # /键隐藏计数器

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
        pixmap14_ = pixmap14.scaled(int(pixSize * 1.5), int(pixSize * 1.5))
        pixmap15_ = pixmap15.scaled(int(pixSize * 1.5), int(pixSize * 1.5))
        pixmap16_ = pixmap16.scaled(int(pixSize * 1.5), int(pixSize * 1.5))
        pixmap17_ = pixmap17.scaled(int(pixSize * 1.5), int(pixSize * 1.5))
        pixmap18_ = pixmap18.scaled(int(pixSize * 1.5), int(pixSize * 1.5))
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
        pixLEDmap0_ = pixLEDmap0.copy().scaled(pixSize, int(pixSize * 1.75))
        pixLEDmap1_ = pixLEDmap1.copy().scaled(pixSize, int(pixSize * 1.75))
        pixLEDmap2_ = pixLEDmap2.copy().scaled(pixSize, int(pixSize * 1.75))
        pixLEDmap3_ = pixLEDmap3.copy().scaled(pixSize, int(pixSize * 1.75))
        pixLEDmap4_ = pixLEDmap4.copy().scaled(pixSize, int(pixSize * 1.75))
        pixLEDmap5_ = pixLEDmap5.copy().scaled(pixSize, int(pixSize * 1.75))
        pixLEDmap6_ = pixLEDmap6.copy().scaled(pixSize, int(pixSize * 1.75))
        pixLEDmap7_ = pixLEDmap7.copy().scaled(pixSize, int(pixSize * 1.75))
        pixLEDmap8_ = pixLEDmap8.copy().scaled(pixSize, int(pixSize * 1.75))
        pixLEDmap9_ = pixLEDmap9.copy().scaled(pixSize, int(pixSize * 1.75))
        self.pixmapLEDNum = {0: pixLEDmap0_, 1: pixLEDmap1_, 2: pixLEDmap2_, 3: pixLEDmap3_,
                        4: pixLEDmap4_, 5: pixLEDmap5_, 6: pixLEDmap6_, 7: pixLEDmap7_,
                        8: pixLEDmap8_, 9: pixLEDmap9_}

    def reimportLEDPic(self, pixSize):
        # 导重新入资源，并缩放到希望的尺寸、比例
        self.pixmapNum = {key:value.copy().scaled(int(pixSize * 1.5), int(pixSize * 1.5)) for key,value in self.pixmapNumPix.items()}
        self.pixmapLEDNum = {key:value.copy().scaled(pixSize, int(pixSize * 1.75)) for key,value in self.pixmapLEDNumPix.items()}


    def readPredefinedBoardPara(self):
        # 从配置中更新出快捷键1, 2, 3, 4、5、6的定义(0是自定义)
        config = configparser.ConfigParser()
        config.read(self.game_setting_path)
        self.predefinedBoardPara[0] = {
            "game_mode": config.getint('DEFAULT','gamemode'),
            "row": 8,
            "column": 8,
            "pix_size": config.getint('DEFAULT','pixsize'),
            "mine_num": 10,
            "board_constraint": config["CUSTOM"]["board_constraint"],
            "attempt_times_limit": config.getint('CUSTOM','attempt_times_limit'),
            }
        self.predefinedBoardPara[1] = {
            "game_mode": config.getint('DEFAULT','gamemode'),
            "row": 8,
            "column": 8,
            "pix_size": config.getint('DEFAULT','pixsize'),
            "mine_num": 10,
            "board_constraint": config["BEGINNER"]["board_constraint"],
            "attempt_times_limit": config.getint('BEGINNER','attempt_times_limit'),
            }
        self.predefinedBoardPara[2] = {
            "game_mode": config.getint('DEFAULT','gamemode'),
            "row": 16,
            "column": 16,
            "pix_size": config.getint('DEFAULT','pixsize'),
            "mine_num": 40,
            "board_constraint": config["INTERMEDIATE"]["board_constraint"],
            "attempt_times_limit": config.getint('INTERMEDIATE','attempt_times_limit'),
            }
        self.predefinedBoardPara[3] = {
            "game_mode": config.getint('DEFAULT','gamemode'),
            "row": 16,
            "column": 30,
            "pix_size": config.getint('DEFAULT','pixsize'),
            "mine_num": 99,
            "board_constraint": config["EXPERT"]["board_constraint"],
            "attempt_times_limit": config.getint('EXPERT','attempt_times_limit'),
            }
        self.predefinedBoardPara[4] = {
            "game_mode": config.getint('CUSTOM_PRESET_4','gameMode'),
            "row": config.getint('CUSTOM_PRESET_4','row'),
            "column": config.getint('CUSTOM_PRESET_4','column'),
            "pix_size": config.getint('CUSTOM_PRESET_4','pixSize'),
            "mine_num": config.getint('CUSTOM_PRESET_4','mineNum'),
            "board_constraint": config["CUSTOM_PRESET_4"]["board_constraint"],
            "attempt_times_limit": config.getint('CUSTOM_PRESET_4','attempt_times_limit'),
            }

        self.predefinedBoardPara[5] = {
            "game_mode": config.getint('CUSTOM_PRESET_5','gameMode'),
            "row": config.getint('CUSTOM_PRESET_5','row'),
            "column": config.getint('CUSTOM_PRESET_5','column'),
            "pix_size": config.getint('CUSTOM_PRESET_5','pixSize'),
            "mine_num": config.getint('CUSTOM_PRESET_5','mineNum'),
            "board_constraint": config["CUSTOM_PRESET_5"]["board_constraint"],
            "attempt_times_limit": config.getint('CUSTOM_PRESET_5','attempt_times_limit'),
            }
        
        self.predefinedBoardPara[6] = {
            "game_mode": config.getint('CUSTOM_PRESET_6','gameMode'),
            "row": config.getint('CUSTOM_PRESET_6','row'),
            "column": config.getint('CUSTOM_PRESET_6','column'),
            "pix_size": config.getint('CUSTOM_PRESET_6','pixSize'),
            "mine_num": config.getint('CUSTOM_PRESET_6','mineNum'),
            "board_constraint": config["CUSTOM_PRESET_6"]["board_constraint"],
            "attempt_times_limit": config.getint('CUSTOM_PRESET_6','attempt_times_limit'),
            }

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







