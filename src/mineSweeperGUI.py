# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QCoreApplication
from PyQt5.QtGui import QPixmap
# from PyQt5.QtWidgets import QLineEdit, QInputDialog, QShortcut
import gameDefinedParameter
import superGUI, gameAbout, gameSettings, gameHelp, gameTerms, gameScores,\
    gameSettingShortcuts, captureScreen, mine_num_bar
import minesweeper_master as mm
import ms_toollib as ms
import configparser
import time
# import sys
# from PyQt5.QtWidgets import QApplication

class MineSweeperGUI(superGUI.Ui_MainWindow):
    def __init__(self, MainWindow):
        self.mainWindow = MainWindow
        super(MineSweeperGUI, self).__init__(MainWindow)
        # MineSweeperGUI父类的init中读.ini、读图片、设置字体、局面初始化等
        
        self.finish = False
        self.gamestart = False

        self.operationStream = []
        self.gameWinFlag = False
        self.showShot = False # 展示OBR功能的状态
        
        self.enuLimitAI = 30  # AI采用的最大枚举长度限制
        self.board = [[0] * self.column for _ in range(self.row)]


        self.time = 0
        self.showTime(self.time)
        self.timer = QTimer()
        self.timer.setInterval(1000)  # 一千毫秒回调一次的定时器
        self.timer.timeout.connect(self.timeCount)
        # text4 = '1'
        # self.label_info.setText(text4)
        self.mineUnFlagedNum = self.mineNum  # 没有标出的雷，显示在左上角
        self.showMineNum(self.mineUnFlagedNum)    # 在左上角画雷数

        # 绑定菜单栏事件
        self.actionnew_game.triggered.connect(self.gameRestart)
        self.actionchu_ji.triggered.connect(self.action_BEvent)
        self.actionzhogn_ji.triggered.connect(self.action_IEvent)
        self.actiongao_ji.triggered.connect(self.action_Event)
        self.actionzi_ding_yi.triggered.connect(self.action_CEvent)
        self.actiontui_chu.triggered.connect(QCoreApplication.instance().quit)
        self.actionyouxi_she_zhi.triggered.connect(self.action_NEvent)
        self.action_kuaijiejian.triggered.connect(self.action_QEvent)
        self.actionxis.triggered.connect(self.action_HEvent)
        self.actiongaun_yv.triggered.connect(self.action_AEvent)
        self.actionrumjc.triggered.connect(self.action_JEvent)

        config = configparser.ConfigParser()
        config.read('gameSetting.ini')
        if (self.row, self.column, self.mineNum) == (8, 8, 10):
            self.actionChecked('B')
        elif (self.row, self.column, self.mineNum) == (16, 16, 40):
            self.actionChecked('I')
        elif (self.row, self.column, self.mineNum) == (16, 30, 99):
            self.actionChecked('E')
        else:
            self.actionChecked('C')

        self.frameShortcut1.activated.connect(self.action_BEvent)
        self.frameShortcut2.activated.connect(self.action_IEvent)
        self.frameShortcut3.activated.connect(self.action_Event)
        self.frameShortcut4.activated.connect(self.gameRestart)
        self.frameShortcut5.activated.connect(lambda: self.predefined_Board(4))
        self.frameShortcut6.activated.connect(lambda: self.predefined_Board(5))
        self.frameShortcut7.activated.connect(lambda: self.predefined_Board(6))
        self.frameShortcut8.activated.connect(self.showScores)
        self.frameShortcut9.activated.connect(self.screenShot)

        self.game_state = 'ready'
        # 用状态机控制局面状态。
        # 约定：'ready'：预备状态。表示局面完全没有左键点过，可能被右键标雷；刚打开或点脸时进入这种状态。
        #               此时可以改雷数、改格子大小（ctrl+滚轮）、行数、列数（拖拉边框）。
        #      'study':研究状态。截图后进入。应该设计第二种方式进入研究状态，没想好。
        #      'modify':调整状态。'ready'下，拖拉边框时进入，拖拉结束后自动转为'ready'。
        #      'playing':正在游戏状态、标准模式、不筛选3BV、且没有看概率计算结果，游戏结果是official的。
        #      'joking':正在游戏状态，游戏中看过概率计算结果，游戏结果不是official的。
        #      'fail':游戏失败，踩雷了。
        #      'win':游戏成功。

    def outOfBorder(self, i, j):
        if i < 0 or i >= self.row or j < 0 or j >= self.column:
            return True
        return False

    def layMine(self, i, j):
        xx = self.row
        yy = self.column
        num = self.mineNum
        if self.gameMode == 2 or self.gameMode == 3 or self.gameMode == 6:
            # 根据模式生成局面
            Board, Parameters = mm.laymine_solvable(self.min3BV, self.max3BV,
                                                    self.timesLimit, (xx, yy, num, i, j))
        elif self.gameMode == 0 or self.gameMode == 4 or self.gameMode == 5 or self.gameMode == 7:
            Board, Parameters = mm.laymine(self.min3BV, self.max3BV,
                                           self.timesLimit, (xx, yy, num, i, j))
        elif self.gameMode == 1:
            Board, Parameters = mm.laymine_op(self.min3BV, self.max3BV,
                                              self.timesLimit, (xx, yy, num, i, j))
        if Parameters:
            # text4 = 'Sucess! 3BV=%d\n尝试次数为%d'%(Parameters[1],Parameters[2])
            # text4 = 'ttt'
            text4 = 'Success!'
            self.label_info.setText(text4)
        else:
            # text4 = 'Failure! 3BV=%d\n尝试次数为%d'%(Parameters[1],Parameters[2])
            # text4 = 'iii'
            text4 = 'Failure!'
            self.label_info.setText(text4)

        self.label.ms_board.board = Board

    def timeCount(self):  # 定时器改时间
        self.time += 1
        self.showTime(self.time)

    def ai(self, i, j):
        # 0，1，2，3，4，5，6，7代表：标准、win7、
        # 竞速无猜、强无猜、弱无猜、准无猜、强可猜、弱可猜
        # 根据模式处理一次点击的全部流程
        # 返回的最后一个值是一个flag，无论是不是雷，都代表是否失败，True为失败
        # 该函数维护boardofGame，具体为标雷
        # （i，j）一定是未打开状态
        if self.board[i][j] == -1:
            # MatrixA, Matrixx, Matrixb = refreshMatrix(boardofGame)
            if self.gameMode <= 3:
                return True
            elif self.gameMode == 4 or self.gameMode == 5:
                self.boardofGame, flagJ = mm.isJudgeable(self.boardofGame)
                if flagJ:
                    return True
                else:
                    self.board, flag = mm.enumerateChangeBoard(self.board, self.boardofGame, i, j)
                    #上面这个函数，返回True是改图成功，False是改图失败（由于没有多余的空位等）
                    return not flag
            else:
                self.board, flag = mm.enumerateChangeBoard(self.board, self.boardofGame, i, j)
                return not flag
        else:
            if self.gameMode <= 2 or self.gameMode >= 5:
                return False
            else:
                if mm.xyisJudgeable(self.boardofGame, i, j):
                    return False
                else:
                    if self.gameMode == 4:
                        self.boardofGame, flagJ = mm.isJudgeable(self.boardofGame)
                        if not flagJ:
                            return False
                        else:
                            return True
                    else:
                        return True
        # print(self.boardofGame)

    def mineAreaLeftRelease(self, i, j):
        if self.game_state == 'ready':
            if i >= self.row or j >= self.column:
                self.operationStream.append(('lr', (self.row, self.column)))
                self.label.ms_board.step('lr', (self.row, self.column))
                pixmap = QPixmap(self.pixmapNum[14])
                self.label_2.setPixmap(pixmap)
                self.label_2.setScaledContents(True)
            else:
                self.layMine(i, j)
                self.game_state = 'playing'
                self.timer.start()
                self.startTime = time.time()
            
        if self.game_state == 'playing' or self.game_state == 'joking':
            self.operationStream.append(('lr', (i, j)))
            self.label.ms_board.step('lr', (i, j))
            pixmap = QPixmap(self.pixmapNum[14])
            self.label_2.setPixmap(pixmap)
            self.label_2.setScaledContents(True)
            if self.label.ms_board.game_board_state == 3:
                self.gameWin()
            elif self.label.ms_board.game_board_state == 4:
                self.gameFailed()
            self.label.update()
            
            
    def mineAreaRightRelease(self, i, j):
        if self.game_state == 'ready' or self.game_state == 'playing' or self.game_state == 'joking':
            self.operationStream.append(('rr', (i, j)))
            self.label.ms_board.step('rr', (i, j))
            self.label.update()
                
            pixmap = QPixmap(self.pixmapNum[14])
            self.label_2.setPixmap(pixmap)
            self.label_2.setScaledContents(True)

    def mineAreaRightPressed(self, i, j):
        if self.game_state == 'ready' or self.game_state == 'playing' or self.game_state == 'joking':
            if self.label.ms_board.game_board[i][j] == 11:
                self.mineUnFlagedNum += 1
                self.showMineNum(self.mineUnFlagedNum)
            elif self.label.ms_board.game_board[i][j] == 10:
                self.mineUnFlagedNum -= 1
                self.showMineNum(self.mineUnFlagedNum)
            self.operationStream.append(('rc', (i, j)))
            self.label.ms_board.step('rc', (i, j))
            self.label.update()
            
            pixmap = QPixmap(self.pixmapNum[15])
            self.label_2.setPixmap(pixmap)
            self.label_2.setScaledContents(True)

    def mineAreaLeftPressed(self, i, j):
        if self.game_state == 'ready' or self.game_state == 'playing' or self.game_state == 'joking':
            self.operationStream.append(('lc', (i, j)))  # 记录鼠标动作
            self.label.ms_board.step('lc', (i, j))
            self.label.update()
            
            pixmap = QPixmap(self.pixmapNum[15])
            self.label_2.setPixmap(pixmap)
            self.label_2.setScaledContents(True)

    def mineAreaLeftAndRightPressed(self, i, j):
        if self.game_state == 'ready' or self.game_state == 'playing' or self.game_state == 'joking':
            self.operationStream.append(('cc', (i, j)))
            self.label.ms_board.step('cc', (i, j))
            self.label.update()
            
            pixmap = QPixmap(self.pixmapNum[15])
            self.label_2.setPixmap(pixmap)
            self.label_2.setScaledContents(True)

    def mineKeyReleaseEvent(self, keyName):
        # 松开空格键
        if keyName == 'Space':
            if self.game_state == 'show':
                self.game_state = 'joking'
                self.label.paintPossibility = False
                self.label.setMouseTracking(False)
                self.label.update()

    def mineAreaLeftAndRightRelease(self, i, j):
        if self.game_state == 'ready' or self.game_state == 'playing' or self.game_state == 'joking':
            if self.label.ms_board.mouse_state == 2:
                self.operationStream.append(('lr', (i, j)))
                self.label.ms_board.step('lr', (i, j))
            elif self.label.ms_board.mouse_state == 7:
                self.operationStream.append(('rr', (i, j)))
                self.label.ms_board.step('rr', (i, j))
            pixmap = QPixmap(self.pixmapNum[14])
            self.label_2.setPixmap(pixmap)
            self.label_2.setScaledContents(True)
            if self.label.ms_board.game_board_state == 3:
                self.gameWin()
            elif self.label.ms_board.game_board_state == 4:
                self.gameFailed()
            self.label.update()

    def mineMouseMove(self, i, j):
        # 按住空格后的鼠标移动事件，与概率的显示有关
        if self.game_state == 'show':
            text4 = '{:.3f}'.format(max(0, self.label.boardPossibility[i][j]))
            self.label_info.setText(text4)
            return
        # 正常情况的鼠标移动事件，与高亮的显示有关
        elif self.game_state == 'playing' or self.game_state == 'joking' or self.game_state == 'ready':
            self.label.update()

    def gameStart(self):  # 画界面，但是不埋雷
        self.mineUnFlagedNum = self.mineNum  # 没有标出的雷，显示在左上角
        self.showMineNum(self.mineUnFlagedNum)    # 在左上角画雷数
        pixmap = QPixmap(self.pixmapNum[14])
        self.label_2.setPixmap(pixmap)
        self.label_2.setScaledContents(True)
        self.time = 0
        self.showTime(self.time)
        self.timer.stop()
        self.initMineArea()
        self.showShot = False
        self.mainWindow.setMinimumSize(0, 0)
        self.mainWindow.resize(0, 0)
        self.operationStream = []  # 记录整局的鼠标操作流，格式例如[('l1',(x,y)),('r1',(x,y)),('c2',(x,y))]
       
        self.label.paintPossibility = False
        self.label.setMouseTracking(False)
        
        if self.game_state == 'study':
            self.game_state = 'ready'
            self.num_bar_ui.QWidget.close()
        else:
            self.game_state = 'ready'

    def gameRestart(self, e = None):  # 画界面，但是不埋雷，改数据而不是重新生成label
        if e:
        # 点脸周围时，会传入一个e参数
            if not (self.MinenumTimeWigdet.width() >= e.localPos().x() >= 0 and 0 <= e.localPos().y() <= self.MinenumTimeWigdet.height()):
                return
        # 点击脸时调用
        self.time = 0
        self.showTime(self.time)
        self.mineUnFlagedNum = self.mineNum
        self.showMineNum(self.mineUnFlagedNum)
        # pixmap = QPixmap(self.pixmapNum[14])
        # self.label_2.setPixmap(pixmap)
        # self.label_2.setScaledContents(True)
        self.timer.stop()
        self.label.ms_board = ms.MinesweeperBoard([[0] * self.column for _ in range(self.row)])
        self.label.update()
        self.label.paintPossibility = False
        self.showShot = False
        self.label.setMouseTracking(False)
        if self.game_state == 'study':
            self.num_bar_ui.QWidget.close()
        self.game_state = 'ready'

    def gameFinished(self):  # 游戏结束画残局，改状态
        
        if self.label.ms_board.game_board_state == 3 and self.gameover_flag:
            board = self.label.ms_board.board
            game_board = self.label.ms_board.game_board
            for idx, row in enumerate(board):
                for idy, item in enumerate(row):
                    if item == -1 and game_board[idx][idy] == 10:
                        game_board[idx][idy] = 11
            self.label.ms_board.game_board = game_board
        elif self.label.ms_board.game_board_state == 4:
            board = self.label.ms_board.board
            game_board = self.label.ms_board.game_board
            for idx, row in enumerate(board):
                for idy, item in enumerate(row):
                    if item == -1 and game_board[idx][idy] == 10:
                        game_board[idx][idy] = 16 # 白雷
            self.label.ms_board.game_board = game_board
        self.label.update()
        # print(self.operationStream)

    def gameWin(self):  # 成功后改脸和状态变量，停时间
        self.endTime = time.time()
        self.gameTime = self.endTime - self.startTime # 精确的游戏时间
        self.timer.stop()
        
        self.game_state = 'win'
        pixmap = QPixmap(self.pixmapNum[17])
        self.label_2.setPixmap(pixmap)
        self.label_2.setScaledContents(True)
        
        if self.row == 8 and self.column == 8 and self.mineNum == 10:
            Difficulty = 1
        elif self.row == 16 and self.column == 16 and self.mineNum == 40:
            Difficulty = 2
        elif self.row == 16 and self.column == 30 and self.mineNum == 99:
            Difficulty = 3
        else:
            Difficulty = 4
        self.scores, self.scoresValue, msBoard = mm.calScores(self.gameMode, self.gameWinFlag, time.time() - self.startTime,
                                                      self.operationStream, self.board, Difficulty)
        if msBoard.solved3BV / ms.cal3BV(self.board) * 100 >= self.auto_show_score:
            self.gameFinished()
            self.showScores()
        else:
            self.gameFinished()

    def gameFailed(self): # 失败后改脸和状态变量
        self.endTime = time.time()
        self.gameTime = self.endTime - self.startTime # 精确的游戏时间
        self.timer.stop()
        
        self.game_state = 'fail'
        
        pixmap = QPixmap(self.pixmapNum[16])
        self.label_2.setPixmap(pixmap)
        self.label_2.setScaledContents(True)
        
        if self.row == 8 and self.column == 8 and self.mineNum == 10:
            Difficulty = 1
        elif self.row == 16 and self.column == 16 and self.mineNum == 40:
            Difficulty = 2
        elif self.row == 16 and self.column == 30 and self.mineNum == 99:
            Difficulty = 3
        else:
            Difficulty = 4
        self.scores, self.scoresValue, msBoard = mm.calScores(self.gameMode, self.gameWinFlag, time.time() - self.startTime,
                                                      self.operationStream, self.board, Difficulty)
        if msBoard.solved3BV / ms.cal3BV(self.board) * 100 >= self.auto_show_score:
            self.gameFinished()
            self.showScores()
        elif msBoard.solved3BV / ms.cal3BV(self.board) * 100 <= self.auto_replay:
            self.gameRestart()
        else:
            self.gameFinished()

    def showMineNum(self, n):
        # 显示剩余雷数，雷数大于等于0，小于等于999，整数
        # if needCalPoss:
        #     ans = minesweeper_master.calPossibility_onboard(self.label.ms_board.game_board, self.mineNum)
        #     self.label.boardPossibility = ans[0]
        #     self.label.update()
        # self.mineNumShow = n
        if n >= 0 and n <= 999:
            self.label_11.setPixmap(self.pixmapLEDNum[n//100])
            self.label_12.setPixmap(self.pixmapLEDNum[n//10%10])
            self.label_13.setPixmap(self.pixmapLEDNum[n%10])
        elif n < 0:
            self.label_11.setPixmap(self.pixmapLEDNum[0])
            self.label_12.setPixmap(self.pixmapLEDNum[0])
            self.label_13.setPixmap(self.pixmapLEDNum[0])
        elif n >= 1000:
            self.label_11.setPixmap(self.pixmapLEDNum[9])
            self.label_12.setPixmap(self.pixmapLEDNum[9])
            self.label_13.setPixmap(self.pixmapLEDNum[9])
        
    def showMineNumCalPoss(self):
        # 显示雷数并展示概率
        ans = ms.cal_possibility_onboard(self.label.ms_board.game_board, self.mineNumShow)
        self.label.boardPossibility = ans[0]
        self.label.update()
        
        n = self.mineNumShow
        if n >= 0 and n <= 999:
            self.label_11.setPixmap(self.pixmapLEDNum[n//100])
            self.label_12.setPixmap(self.pixmapLEDNum[n//10%10])
            self.label_13.setPixmap(self.pixmapLEDNum[n%10])
            return
        elif n < 0:
            self.label_11.setPixmap(self.pixmapLEDNum[0])
            self.label_12.setPixmap(self.pixmapLEDNum[0])
            self.label_13.setPixmap(self.pixmapLEDNum[0])
            return
        elif n >= 1000:
            self.label_11.setPixmap(self.pixmapLEDNum[9])
            self.label_12.setPixmap(self.pixmapLEDNum[9])
            self.label_13.setPixmap(self.pixmapLEDNum[9])
            return

    def showTime(self, t):
        # 显示剩余时间，时间数大于等于0，小于等于999秒，整数
        if t >= 0 and t <= 999:
            self.label_31.setPixmap(self.pixmapLEDNum[t//100])
            self.label_32.setPixmap(self.pixmapLEDNum[t//10%10])
            self.label_33.setPixmap(self.pixmapLEDNum[t%10])
            return
        elif t >= 1000:
            return

    def actionChecked(self, k):
        # 菜单前面打勾
        self.actionchu_ji.setChecked(False)
        self.actionzhogn_ji.setChecked(False)
        self.actiongao_ji.setChecked(False)
        self.actionzi_ding_yi.setChecked(False)
        if k == 'B':
            self.actionchu_ji.setChecked(True)
        elif k == 'I':
            self.actionzhogn_ji.setChecked(True)
        elif k == 'E':
            self.actiongao_ji.setChecked(True)
        elif k == 'C':
            self.actionzi_ding_yi.setChecked(True)

    def action_BEvent(self):
        self.actionChecked('B')
        self.setBoard_and_start(8, 8, 10)

    def action_IEvent(self):
        self.actionChecked('I')
        self.setBoard_and_start(16, 16, 40)

    def action_Event(self):
        self.actionChecked('E')
        self.setBoard_and_start(16, 30, 99)

    def predefined_Board(self, k):
        self.gameMode = self.predefinedBoardPara[k][0]
        self.max3BV = self.predefinedBoardPara[k][1]
        self.min3BV = self.predefinedBoardPara[k][2]
        self.timesLimit = self.predefinedBoardPara[k][6]
        self.enuLimit = self.predefinedBoardPara[k][7]
        self.pixSize = self.predefinedBoardPara[k][5]
        self.importLEDPic(self.pixSize)
        self.label.importCellPic(self.pixSize)
        self.label_2.reloadFace(self.pixSize)
        self.setBoard_and_start(self.predefinedBoardPara[k][3],
                                self.predefinedBoardPara[k][4],
                                self.predefinedBoardPara[k][8])
        self.refreshSettingsDefault()

    def action_CEvent(self):
        # 点击菜单栏的自定义后回调
        self.actionChecked('C')
        ui = gameDefinedParameter.ui_Form(self.row, self.column, self.mineNum)
        ui.Dialog.setModal(True)
        ui.Dialog.show()
        ui.Dialog.exec_()
        if ui.alter:
            self.setBoard_and_start(ui.row, ui.column, ui.mineNum)

    def setBoard_and_start(self, row, column, mineNum):
        # 把局面设置成(row, column, mineNum)，把3BV的限制设置成min3BV, max3BV
        if (self.row, self.column, self.mineNum) != (row, column, mineNum):
            for i in range(self.row):
                self.gridLayout.setRowMinimumHeight(i, 0)
            for i in range(self.column):
                self.gridLayout.setColumnMinimumWidth(i, 0)
            self.row = row
            self.column = column
            self.mineNum = mineNum
            conf = configparser.ConfigParser()
            conf.read("gameSetting.ini")
            conf.set("DEFAULT", "row", str(row))
            conf.set("DEFAULT", "column", str(column))
            conf.set("DEFAULT", "mineNum", str(mineNum))
            if (row, column, mineNum) == (8, 8, 10):
                self.min3BV = conf.getint('BEGINNER', 'min3BV')
                self.max3BV = conf.getint('BEGINNER', 'max3BV')
            elif (row, column, mineNum) == (16, 16, 40):
                self.min3BV = conf.getint('INTERMEDIATE', 'min3BV')
                self.max3BV = conf.getint('INTERMEDIATE', 'max3BV')
            elif (row, column, mineNum) == (16, 30, 99):
                self.min3BV = conf.getint('EXPERT', 'min3BV')
                self.max3BV = conf.getint('EXPERT', 'max3BV')
            else:
                self.min3BV = conf.getint('CUSTOM', 'min3BV')
                self.max3BV = conf.getint('CUSTOM', 'max3BV')
            conf.write(open('gameSetting.ini', "w"))
            self.gameStart()
        else:
            self.gameRestart()


    def action_NEvent(self):
        # 游戏设置
        self.actionChecked('N')
        ui = gameSettings.ui_Form()
        ui.Dialog.setModal(True)
        ui.Dialog.show()
        ui.Dialog.exec_()
        if ui.alter:
            self.min3BV = ui.min3BV
            self.max3BV = ui.max3BV
            self.timesLimit = ui.timesLimit
            self.enuLimit = ui.enuLimit
            self.gameMode = ui.gameMode
            self.pixSize = ui.pixSize
            self.auto_replay = ui.auto_replay
            self.auto_show_score = ui.auto_show_score
            self.gameover_flag = ui.gameover_flag
            self.importLEDPic(self.pixSize)
            self.label.importCellPic(self.pixSize)
            self.label_2.reloadFace(self.pixSize)
            self.gameStart()
            self.mainWindow.setWindowOpacity(ui.transparency / 100)

    def action_QEvent(self):
        # 词典，即游戏帮助、术语表
        self.actionChecked('Q')
        ui = gameSettingShortcuts.myGameSettingShortcuts()
        ui.Dialog.setModal(True)
        ui.Dialog.show()
        ui.Dialog.exec_()
        if ui.alter:
            self.readPredefinedBoard()

    def action_HEvent(self):
        # 词典，即游戏帮助、术语表
        self.actionChecked('H')
        ui = gameTerms.Ui_Form()
        ui.Dialog.setModal(True)
        ui.Dialog.show()
        ui.Dialog.exec_()

    def action_AEvent(self):
        # 关于
        self.actionChecked('A')
        ui = gameAbout.Ui_Form()
        ui.Dialog.setModal(True)
        ui.Dialog.show()
        ui.Dialog.exec_()

    def action_JEvent(self):
        # 入门教程
        self.actionChecked('J')
        ui = gameHelp.Ui_Form()
        ui.Dialog.setModal(True)
        ui.Dialog.show()
        ui.Dialog.exec_()

    def screenShot(self):
        # ‘ctrl’ + ‘space’ 事件，启动截图
        
        ui = captureScreen.CaptureScreen()
        ui.show()
        ui.exec_()
        
        
        if len(ui.board) < 6 or len(ui.board[0]) < 6:
            return
        
        
        ans = ms.cal_possibility_onboard(ui.board, 0.20625 if len(ui.board[0]) >= 24 else 0.15625)
        
        
        self.num_bar_ui = mine_num_bar.ui_Form(ans[1], self.pixSize * len(ui.board))
        self.num_bar_ui.QWidget.barSetMineNum.connect(self.showMineNum)
        self.num_bar_ui.QWidget.barSetMineNumCalPoss.connect(self.showMineNumCalPoss)
        self.num_bar_ui.setSignal()
        
        self.mainWindow.closeEvent_.connect(self.num_bar_ui.QWidget.close)
        
        self.num_bar_ui.QWidget.show()
        
        self.setBoard_and_start(len(ui.board), len(ui.board[0]), ans[1][1])
        self.mineNumShow = ans[1][1]
        
        self.label.ms_board.game_board = ui.board
        ans = ms.cal_possibility_onboard(ui.board, self.mineNumShow)
        self.label.boardPossibility = ans[0]
        self.label.paintPossibility = True
        # self.showShot = True
        self.label.update()
        # self.finish = True
        # self.spaceHold = True
        self.label.setMouseTracking(True)
        self.game_state = 'study'    # 局面进入研究模式
        

    def showScores(self):
        # 按空格
        if self.game_state == 'win' or self.game_state == 'fail':
            # 游戏结束后，按空格展示成绩
            ui = gameScores.Ui_Form(self.scores, self.scoresValue)
            ui.setModal(True)
            ui.show()
            ui.exec_()
            # 展示每格概率
        elif self.game_state == 'playing' or self.game_state == 'joking':
            self.game_state = 'show'
            self.label.paintPossibility = True
            self.label.setMouseTracking(True)
            mineNum = self.mineNum
            ans = ms.cal_possibility_onboard(self.label.ms_board.game_board, mineNum)
            self.label.boardPossibility = ans[0]
            # print(self.label.boardPossibility)
            self.label.update()



    def refreshSettingsDefault(self):
        # 刷新游戏设置.ini里默认部分的设置，与当前游戏里一致，
        # 除了transparency、mainwintop和mainwinleft
        conf = configparser.ConfigParser()
        conf.read("gameSetting.ini")
        conf.set("DEFAULT", "timeslimit", str(self.timesLimit))
        conf.set("DEFAULT", "enulimit", str(self.enuLimit))
        conf.set("DEFAULT", "gamemode", str(self.gameMode))
        conf.set("DEFAULT", "pixsize", str(self.pixSize))
        conf.set("DEFAULT", "row", str(self.row))
        conf.set("DEFAULT", "column", str(self.column))
        conf.set("DEFAULT", "minenum", str(self.mineNum))
        conf.write(open('gameSetting.ini', "w"))












