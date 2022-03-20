from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize
from mineLabel import mineLabel#, mineLabel_new
from uiComponents import StatusLabel
import configparser
from PyQt5.QtGui import QPalette, QPixmap, QFont, QIcon
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtSvg import QSvgWidget

class Ui_MainWindow(object):
    def __init__(self, MainWindow):
        self.mainWindow = MainWindow
        self.mainWindow.setWindowIcon(QIcon("media/cat.ico"))
        self.mainWindow.setFixedSize(self.mainWindow.minimumSize())

        config = configparser.ConfigParser()
        # gameMode = 0，1，2，3，4，5，6，7代表：
        # 标准、win7、竞速无猜、强无猜、弱无猜、准无猜、强可猜、弱可猜
        if config.read('gameSetting.ini'):
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
            with open('gameSetting.ini', 'w') as configfile:
                config.write(configfile)  # 将对象写入文件


        self.setupUi(self.mainWindow)
        self.importLEDPic(self.pixSize) # 导入图片

        # self.mineLabel = []  # 局面
        self.initMineArea()
        self.label_2.leftRelease.connect(self.gameRestart)
        self.MinenumTimeWigdet.mouseReleaseEvent = self.gameRestart

        self.label_2.setPixmap(self.pixmapNum[14])
        self.label_2.setScaledContents(True)
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.black)  # 设置字体颜色
        self.label_31.setPalette(pe)
        self.label_31.setFont(QFont("Arial", 20, QFont.Bold))
        self.label_32.setPalette(pe)
        self.label_32.setFont(QFont("Arial", 20, QFont.Bold))
        self.label_33.setPalette(pe)
        self.label_33.setFont(QFont("Arial", 20, QFont.Bold))
        self.label_11.setPalette(pe)
        self.label_11.setFont(QFont("Arial", 12, QFont.Bold))
        self.label_12.setPalette(pe)
        self.label_12.setFont(QFont("Arial", 12, QFont.Bold))
        self.label_13.setPalette(pe)
        self.label_13.setFont(QFont("Arial", 12, QFont.Bold))
        self.label_info.setPalette(pe)         # 最下面的框
        self.label_info.setFont(QFont("Arial", 20, QFont.Bold))
        self.label_info.setText(str(self.mineNum))


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(973, 217)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setSizeIncrement(QtCore.QSize(0, 0))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 192, 192))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 192, 192))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 192, 192))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(192, 192, 192))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        MainWindow.setPalette(palette)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_1 = QtWidgets.QFrame(self.centralwidget)
        self.frame_1.setEnabled(True)
        self.frame_1.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_1.setLineWidth(6)
        self.frame_1.setMidLineWidth(0)
        self.frame_1.setObjectName("frame_1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_1)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.MinenumTimeWigdet = QtWidgets.QFrame(self.frame_1)
        self.MinenumTimeWigdet.setMinimumSize(QtCore.QSize(0, 0))
        self.MinenumTimeWigdet.setStyleSheet("")
        self.MinenumTimeWigdet.setFrameShape(QtWidgets.QFrame.Panel)
        self.MinenumTimeWigdet.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.MinenumTimeWigdet.setLineWidth(4)
        self.MinenumTimeWigdet.setMidLineWidth(0)
        self.MinenumTimeWigdet.setObjectName("MinenumTimeWigdet")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.MinenumTimeWigdet)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_11 = QtWidgets.QLabel(self.MinenumTimeWigdet)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setMinimumSize(QtCore.QSize(0, 0))
        self.label_11.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_11.setAutoFillBackground(False)
        self.label_11.setText("")
        self.label_11.setPixmap(QtGui.QPixmap("media/test.png"))
        self.label_11.setScaledContents(False)
        self.label_11.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_3.addWidget(self.label_11, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.label_12 = QtWidgets.QLabel(self.MinenumTimeWigdet)
        self.label_12.setMinimumSize(QtCore.QSize(0, 0))
        self.label_12.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_12.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_12.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.label_12.setAcceptDrops(False)
        self.label_12.setText("")
        self.label_12.setPixmap(QtGui.QPixmap("media/test.png"))
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_3.addWidget(self.label_12, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.label_13 = QtWidgets.QLabel(self.MinenumTimeWigdet)
        self.label_13.setText("")
        self.label_13.setPixmap(QtGui.QPixmap("media/test.png"))
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_3.addWidget(self.label_13, 0, QtCore.Qt.AlignVCenter)
        self.horizontalLayout.addLayout(self.horizontalLayout_3)
        spacerItem = QtWidgets.QSpacerItem(40, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.frame = QtWidgets.QFrame(self.centralwidget)#QFrame是基本控件的基类
        # self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        # self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")

        self.label_2 = StatusLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(0, 0))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("media/f0.png"))
        self.label_2.setObjectName("label_2")
        self.label_2.setLineWidth(0)
        self.horizontalLayout.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        spacerItem1 = QtWidgets.QSpacerItem(40, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_31 = QtWidgets.QLabel(self.MinenumTimeWigdet)
        self.label_31.setText("")
        self.label_31.setPixmap(QtGui.QPixmap("media/test.png"))
        self.label_31.setObjectName("label_31")
        self.horizontalLayout_4.addWidget(self.label_31, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.label_32 = QtWidgets.QLabel(self.MinenumTimeWigdet)
        self.label_32.setLineWidth(1)
        self.label_32.setText("")
        self.label_32.setPixmap(QtGui.QPixmap("media/test.png"))
        self.label_32.setObjectName("label_32")
        self.horizontalLayout_4.addWidget(self.label_32, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.label_33 = QtWidgets.QLabel(self.MinenumTimeWigdet)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_33.sizePolicy().hasHeightForWidth())
        self.label_33.setSizePolicy(sizePolicy)
        self.label_33.setMinimumSize(QtCore.QSize(0, 0))
        self.label_33.setText("")
        self.label_33.setPixmap(QtGui.QPixmap("media/test.png"))
        self.label_33.setScaledContents(False)
        self.label_33.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_33.setObjectName("label_33")
        self.horizontalLayout_4.addWidget(self.label_33, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.horizontalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout.addWidget(self.MinenumTimeWigdet)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.centralboard = QtWidgets.QFrame(self.frame_1)
        self.centralboard.setFrameShape(QtWidgets.QFrame.Panel)
        self.centralboard.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.centralboard.setLineWidth(5)
        self.centralboard.setObjectName("centralboard")
        self.gridLayout = QtWidgets.QGridLayout(self.centralboard)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")

        self.horizontalLayout_2.addWidget(self.centralboard)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addWidget(self.frame_1)
        self.label_info = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_info.setFont(font)
        self.label_info.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_info.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_info.setObjectName("label_info")
        self.verticalLayout_2.addWidget(self.label_info)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 973, 33))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.menu.setFont(font)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionnew_game = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.actionnew_game.setFont(font)
        self.actionnew_game.setObjectName("actionnew_game")
        self.actionchu_ji = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.actionchu_ji.setFont(font)
        self.actionchu_ji.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.actionchu_ji.setObjectName("actionchu_ji")
        self.actionzhogn_ji = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.actionzhogn_ji.setFont(font)
        self.actionzhogn_ji.setObjectName("actionzhogn_ji")
        self.actiongao_ji = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.actiongao_ji.setFont(font)
        self.actiongao_ji.setObjectName("actiongao_ji")
        self.actionzi_ding_yi = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.actionzi_ding_yi.setFont(font)
        self.actionzi_ding_yi.setObjectName("actionzi_ding_yi")
        self.actiontui_chu = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.actiontui_chu.setFont(font)
        self.actiontui_chu.setObjectName("actiontui_chu")
        self.actionyouxi_she_zhi = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.actionyouxi_she_zhi.setFont(font)
        self.actionyouxi_she_zhi.setObjectName("actionyouxi_she_zhi")
        self.action_kuaijiejian = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.action_kuaijiejian.setFont(font)
        self.action_kuaijiejian.setObjectName("action_kuaijiejian")
        self.actiongaun_yv = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.actiongaun_yv.setFont(font)
        self.actiongaun_yv.setObjectName("actiongaun_yv")
        self.actionxis = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.actionxis.setFont(font)
        self.actionxis.setObjectName("actionxis")
        self.actionrumjc = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.actionrumjc.setFont(font)
        self.actionrumjc.setObjectName("actionrumjc")
        self.menu.addAction(self.actionnew_game)
        self.menu.addSeparator()
        self.menu.addAction(self.actionchu_ji)
        self.menu.addAction(self.actionzhogn_ji)
        self.menu.addAction(self.actiongao_ji)
        self.menu.addAction(self.actionzi_ding_yi)
        self.menu.addSeparator()
        self.menu.addAction(self.actiontui_chu)
        self.menu_2.addAction(self.actionyouxi_she_zhi)
        self.menu_2.addAction(self.action_kuaijiejian)
        self.menu_3.addAction(self.actionxis)
        self.menu_3.addAction(self.actionrumjc)
        self.menu_3.addAction(self.actiongaun_yv)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

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

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_info.setText(_translate("MainWindow", "预留、备用"))
        self.menu.setTitle(_translate("MainWindow", "游戏"))
        self.menu_2.setTitle(_translate("MainWindow", "设置"))
        self.menu_3.setTitle(_translate("MainWindow", "帮助"))
        self.actionnew_game.setText(_translate("MainWindow", "新游戏"))
        self.actionnew_game.setShortcut(_translate("MainWindow", "N"))
        self.actionchu_ji.setText(_translate("MainWindow", "初级"))
        self.actionchu_ji.setShortcut(_translate("MainWindow", "B"))
        self.actionzhogn_ji.setText(_translate("MainWindow", "中级"))
        self.actionzhogn_ji.setShortcut(_translate("MainWindow", "I"))
        self.actiongao_ji.setText(_translate("MainWindow", "高级"))
        self.actiongao_ji.setShortcut(_translate("MainWindow", "E"))
        self.actionzi_ding_yi.setText(_translate("MainWindow", "自定义"))
        self.actionzi_ding_yi.setShortcut(_translate("MainWindow", "C"))
        self.actiontui_chu.setText(_translate("MainWindow", "退出"))
        self.actiontui_chu.setShortcut(_translate("MainWindow", "X"))
        self.actionyouxi_she_zhi.setText(_translate("MainWindow", "游戏设置"))
        self.actionyouxi_she_zhi.setShortcut(_translate("MainWindow", "S"))
        self.action_kuaijiejian.setText(_translate("MainWindow", "快捷键设置"))
        self.action_kuaijiejian.setShortcut(_translate("MainWindow", "Q"))
        self.actiongaun_yv.setText(_translate("MainWindow", "关于"))
        self.actiongaun_yv.setShortcut(_translate("MainWindow", "A"))
        self.actionxis.setText(_translate("MainWindow", "词典"))
        self.actionxis.setShortcut(_translate("MainWindow", "D"))
        self.actionrumjc.setText(_translate("MainWindow", "入门教程"))
        self.actionrumjc.setShortcut(_translate("MainWindow", "J"))


    def initMineArea(self):
        # self.label就是中间的局面
        for i in range(self.gridLayout.count()):
            w = self.gridLayout.itemAt(i).widget()
            w.setParent(None)

        self.label = mineLabel(self.row, self.column, self.pixSize)
        self.label.setMinimumSize(QSize(self.pixSize*self.column, self.pixSize*self.row))
        self.label.leftPressed.connect(self.mineAreaLeftPressed)
        self.label.leftRelease.connect(self.mineAreaLeftRelease)
        self.label.leftAndRightPressed.connect(self.mineAreaLeftAndRightPressed)
        self.label.leftAndRightRelease.connect(self.mineAreaLeftAndRightRelease)
        self.label.rightPressed.connect(self.mineAreaRightPressed)
        self.label.rightRelease.connect(self.mineAreaRightRelease)
        self.label.mouseMove.connect(self.mineMouseMove)

        self.mainWindow.keyRelease.connect(self.mineKeyReleaseEvent)

        self.label.setObjectName("label")
        self.label.resize(QSize(self.pixSize*self.column, self.pixSize*self.row))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        # self.label = mineLabel_new(self.row, self.column, self.pixSize)
        # self.label.setObjectName("label")
        # self.label.resize(QSize(20, 20))
        # self.svgView = QScrollArea()
        # # self.svgView.setObjectName("svgView")
        # # self.svgView.setBackgroundRole(QPalette.Dark)
        # self.svgView.setWidget(self.label)
        # self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        # self.label = QSvgWidget(r"F:\GitHub\Solvable-Minesweeper\src\media\github.svg")
        # # self.label.resize(QSize(200, 20))
        # self.label.setGeometry(0,0,100,150)
        # self.gridLayout.addWidget(self.label, 0, 0, 1, 1)



    def importLEDPic(self, pixSize):
        # 导入资源，并缩放到希望的尺寸、比例
        pixmap14 = QPixmap("media/smileface.svg")
        pixmap15 = QPixmap("media/clickface.svg")
        pixmap16 = QPixmap("media/lostface.svg")
        pixmap17 = QPixmap("media/winface.svg")
        pixmap18 = QPixmap("media/smilefacedown.svg")
        pixmap14 = pixmap14.scaled(pixSize * 1.5, pixSize * 1.5)
        pixmap15 = pixmap15.scaled(pixSize * 1.5, pixSize * 1.5)
        pixmap16 = pixmap16.scaled(pixSize * 1.5, pixSize * 1.5)
        pixmap17 = pixmap17.scaled(pixSize * 1.5, pixSize * 1.5)
        pixmap18 = pixmap18.scaled(pixSize * 1.5, pixSize * 1.5)
        self.pixmapNum = {14: pixmap14, 15: pixmap15, 16: pixmap16, 17: pixmap17, 18: pixmap18}
        # 以上是读取数字的图片，局面中的数字；一下是上方LED数字的图片
        pixLEDmap0 = QPixmap("media/LED0.png")
        pixLEDmap1 = QPixmap("media/LED1.png")
        pixLEDmap2 = QPixmap("media/LED2.png")
        pixLEDmap3 = QPixmap("media/LED3.png")
        pixLEDmap4 = QPixmap("media/LED4.png")
        pixLEDmap5 = QPixmap("media/LED5.png")
        pixLEDmap6 = QPixmap("media/LED6.png")
        pixLEDmap7 = QPixmap("media/LED7.png")
        pixLEDmap8 = QPixmap("media/LED8.png")
        pixLEDmap9 = QPixmap("media/LED9.png")
        pixLEDmap0 = pixLEDmap0.scaled(pixSize, pixSize * 1.75)
        pixLEDmap1 = pixLEDmap1.scaled(pixSize, pixSize * 1.75)
        pixLEDmap2 = pixLEDmap2.scaled(pixSize, pixSize * 1.75)
        pixLEDmap3 = pixLEDmap3.scaled(pixSize, pixSize * 1.75)
        pixLEDmap4 = pixLEDmap4.scaled(pixSize, pixSize * 1.75)
        pixLEDmap5 = pixLEDmap5.scaled(pixSize, pixSize * 1.75)
        pixLEDmap6 = pixLEDmap6.scaled(pixSize, pixSize * 1.75)
        pixLEDmap7 = pixLEDmap7.scaled(pixSize, pixSize * 1.75)
        pixLEDmap8 = pixLEDmap8.scaled(pixSize, pixSize * 1.75)
        pixLEDmap9 = pixLEDmap9.scaled(pixSize, pixSize * 1.75)
        self.pixmapLEDNum = {0: pixLEDmap0, 1: pixLEDmap1, 2: pixLEDmap2, 3: pixLEDmap3,
                        4: pixLEDmap4, 5: pixLEDmap5, 6: pixLEDmap6, 7: pixLEDmap7,
                        8: pixLEDmap8, 9: pixLEDmap9}


    def readPredefinedBoard(self):
        # modTable = [0,1,2,3,4,5,6,7]
        self.predefinedBoardPara = {}
        config = configparser.ConfigParser()
        config.read('gameSetting.ini')
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

        # self.key_6_gameMode = modTable[config.getint('CUSTOM_PRESET_6','gameMode')]
        # self.key_6_max3BV = config.getint('CUSTOM_PRESET_6','max3BV')
        # self.key_6_min3BV = config.getint('CUSTOM_PRESET_6','min3BV')
        # self.key_6_row = config.getint('CUSTOM_PRESET_6','row')
        # self.key_6_column = config.getint('CUSTOM_PRESET_6','column')
        # self.key_6_pixSize = config.getint('CUSTOM_PRESET_6','pixSize')
        # self.key_6_timesLimit = config.getint('CUSTOM_PRESET_6','timesLimit')
        # self.key_6_enuLimit = config.getint('CUSTOM_PRESET_6','enuLimit')
        # self.key_6_mineNum = config.getint('CUSTOM_PRESET_6','mineNum')

