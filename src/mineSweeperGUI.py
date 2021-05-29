# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QCoreApplication, QPoint
from PyQt5.QtGui import QPixmap, QPainter
# from PyQt5.QtWidgets import QLineEdit, QInputDialog, QShortcut
import gameDefinedParameter
import superGUI
import gameAbout
import gameSettings
import gameHelp
import gameTerms
import gameScores
import minesweeper_master
import configparser
import time
import widgetLib


class MineSweeperGUI(superGUI.Ui_MainWindow):
    def __init__(self, MainWindow):
        super(MineSweeperGUI, self).__init__(MainWindow)
        # MineSweeperGUI父类的init中读.ini、读图片、设置字体、局面初始化等
        self.finish = False
        self.gamestart = False

        self.operationStream = []
        self.gameWinFlag = False
        self.leftHeld = False
        self.leftAndRightHeld = False  # 鼠标是否被按下的标志位
        self.oldCell = (0, 0)  # 鼠标的上个停留位置，用于绘制按下去时的阴影
        self.boardofGame = [[10] * self.column for _ in range(self.row)]
        # boardofGame保存了判雷AI所看到的局面,不需要维护，只需要维持传递
        # 包括0~8，10代表未打开，11代表标雷
        # 比如，玩家没有标出来的雷，AI会在这上面标出来，但不一定标全
        self.notMine = []  # 保存AI判出来的雷

        self.matrixA = []
        self.matrixx = []
        self.matrixb = []
        self.enuLimitAI = 30  # AI采用的最大枚举长度限制
        self.board = [[0] * self.column for _ in range(self.row)]


        self.time = 0
        self.showTime(self.time)
        self.timer = QTimer()
        self.timer.setInterval(1000)  # 一千毫秒回调一次的定时器
        self.timer.timeout.connect(self.timeCount)
        text4 = '1'
        self.label_info.setText(text4)
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



    def outOfBorder(self, i, j):
        if i < 0 or i >= self.row or j < 0 or j >= self.column:
            return True
        return False

    def layMine(self, i, j):  # mineLabel[r][c].num是真实局面，-1为雷，数字为数字
        xx = self.row
        yy = self.column
        num = self.mineNum
        if self.gameMode >= 3:  # 如果是模式3及以后，需要用判雷器
            self.boardofGame = [[10] * self.column for _ in range(self.row)]

        if self.gameMode == 2 or self.gameMode == 3 or self.gameMode == 6:
            # 根据模式生成局面
            Board, Parameters = minesweeper_master.layMineSolvable(xx, yy, num, i, j, self.min3BV, self.max3BV,
                                                                   self.timesLimit, self.enuLimit)
        elif self.gameMode == 0 or self.gameMode == 4 or self.gameMode == 5 or self.gameMode == 7:
            Board, Parameters = minesweeper_master.layMine(xx, yy, num, i, j, self.min3BV, self.max3BV, self.timesLimit)
        elif self.gameMode == 1:
            Board, Parameters = minesweeper_master.layMineOp(xx, yy, num, i, j, self.min3BV, self.max3BV,
                                                             self.timesLimit)
        if Parameters[0]:
            # text4 = 'Sucess! 3BV=%d\n尝试次数为%d'%(Parameters[1],Parameters[2])
            # text4 = 'ttt'
            text4 = 'Success! 尝试次数为%d' % (Parameters[2])
            self.label_info.setText(text4)
        else:
            # text4 = 'Failure! 3BV=%d\n尝试次数为%d'%(Parameters[1],Parameters[2])
            # text4 = 'iii'
            text4 = 'Failure! 尝试次数为%d' % (Parameters[2])
            self.label_info.setText(text4)

        for r in range(0, xx):
            for c in range(0, yy):
                # self.mineLabel[r][c].num = Board[r][c]
                self.board[r][c] = Board[r][c]

    def timeCount(self):  # 定时器改时间
        self.time += 1
        self.showTime(self.time)

    def DFS(self, i, j):
        # 改label.board 和 boardofGame
        # board[i][j]一定要没有打开的状态，一定不能是雷
        cellToOpen = [(i, j)]
        while cellToOpen:
            x, y = cellToOpen.pop()
            if self.label.board[x][y] == 10 or self.label.board[x][y] == -2:
                self.label.board[x][y] = self.board[x][y]
                self.boardofGame[x][y] = self.board[x][y]
                if not self.timer.isActive():
                    self.timer.start()
                if self.board[x][y] == 0:
                    for r in range(x - 1, x + 2):
                        for c in range(y - 1, y + 2):
                            if not self.outOfBorder(r, c) and (self.label.board[x][y] == 10 or self.label.board[x][y] == -2) == 0:
                                cellToOpen.append((r, c))
        if self.isGameFinished():
            self.gameWin()

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
                self.boardofGame, flagJ = minesweeper_master.isJudgeable(self.boardofGame)
                if flagJ:
                    return True
                else:
                    self.board, flag = minesweeper_master.enumerateChangeBoard(self.board, self.boardofGame, i, j)
                    #上面这个函数，返回True是改图成功，False是改图失败（由于没有多余的空位等）
                    return not flag
            else:
                self.board, flag = minesweeper_master.enumerateChangeBoard(self.board, self.boardofGame, i, j)
                return not flag
        else:
            if self.gameMode <= 2 or self.gameMode >= 5:
                return False
            else:
                if minesweeper_master.xyisJudgeable(self.boardofGame, i, j):
                    return False
                else:
                    if self.gameMode == 4:
                        self.boardofGame, flagJ = minesweeper_master.isJudgeable(self.boardofGame)
                        if not flagJ:
                            return False
                        else:
                            return True
                    else:
                        return True

    def mineAreaLeftRelease(self, i, j):
        if not self.finish:
            self.label_2.setPixmap(QPixmap(self.pixmapNum[14]))
            self.label_2.setScaledContents(True)
            self.operationStream.append(('l2', (i, j)))  # 记录鼠标动作
        if self.leftHeld:
            self.leftHeld = False  # 防止双击中的左键弹起被误认为真正的左键弹起
            if not self.outOfBorder(i, j) and not self.finish:
                # 鼠标按住并移出局面时，索引会越界
                if self.label.board[i][j] == -2 or self.label.board[i][j] == 10:
                    self.label.board[i][j] == 10
                    # self.mineLabel[i][j].setPixmap(self.pixmapNum[9]) # 把格子恢复成没打开的样子

                    if not self.gamestart:
                        self.operationStream = self.operationStream[-2:] # 初始化并记录鼠标动作
                        # 生成的图要保证点一下不能直接获胜，所以在这里埋雷
                        self.layMine(i, j)
                        self.gamestart = True
                        self.boardofGame = minesweeper_master.refreshBoard(self.board, self.boardofGame, [(i, j)])
                        self.DFS(i, j)
                        self.startTime = time.time()
                        self.DFS(i, j)

                    else:
                        failflag = self.ai(i, j)
                        if not failflag:
                            self.DFS(i, j)
                        else:
                            self.label.board[i][j] = 12
                            self.gameFailed()
                    if self.isGameFinished():
                        self.gameWin()
                self.label.update()

    def mineAreaRightRelease(self, i, j):
        if not self.finish:
            self.operationStream.append(('r2', (i, j)))  # 记录鼠标动作
            self.label_2.setPixmap(QPixmap(self.pixmapNum[14]))
            self.label_2.setScaledContents(True)

    def mineAreaRightPressed(self, i, j):
        if not self.finish:
            self.operationStream.append(('r1', (i, j)))  # 记录鼠标动作
            self.label_2.setPixmap(QPixmap(self.pixmapNum[15]))
            self.label_2.setScaledContents(True)
            if self.label.board[i][j] == 10:  # 标雷
                self.label.board[i][j] = 11
                self.mineUnFlagedNum -= 1
                self.showMineNum(self.mineUnFlagedNum)
            elif self.label.board[i][j] == 11:  # 取消标雷
                self.label.board[i][j] = 10
                self.mineUnFlagedNum += 1
                self.showMineNum(self.mineUnFlagedNum)
            self.label.update()

    def mineAreaLeftPressed(self, i, j):
        self.leftHeld = True
        self.oldCell = (i, j)
        if not self.finish:
            self.operationStream.append(('l1', (i, j)))  # 记录鼠标动作
            self.label_2.setPixmap(QPixmap(self.pixmapNum[15]))
            self.label_2.setScaledContents(True)
            if self.label.board[i][j] == 10:
                self.label.board[i][j] = -2
                self.label.update()

    def mineAreaLeftAndRightPressed(self, i, j):
        self.leftAndRightHeld = True
        self.oldCell = (i, j)
        if not self.finish:
            self.operationStream.append(('c1', (i, j)))  # 记录鼠标动作
            for r in range(i - 1, i + 2):
                for c in range(j - 1, j + 2):
                    if not self.outOfBorder(r, c):
                        if self.label.board[r][c] == 10:
                            self.label.board[r][c] = -2
            self.label.update()

    def chordingFlag(self, i, j):
        # i, j 周围标雷数是否满足双击的要求
        if self.label.board[i][j] <= 8 and self.label.board[i][j] >= 0:
            count = 0
            for r in range(i - 1, i + 2):
                for c in range(j - 1, j + 2):
                    if not self.outOfBorder(r, c):
                        if self.label.board[r][c] == 11:
                            count += 1
            if count == 0:
                return False
            else:
                return count == self.board[i][j]
        else:
            return False

    def mineAreaLeftAndRightRelease(self, i, j):
        self.leftAndRightHeld = False
        self.leftHeld = False
        if not self.finish:
            self.operationStream.append(('c2', (i, j)))  # 记录鼠标动作
            pixmap = QPixmap(self.pixmapNum[14])
            self.label_2.setPixmap(pixmap)
            self.label_2.setScaledContents(True)
        if not self.outOfBorder(i, j) and not self.finish:
            # 鼠标按住并移出局面时，索引会越界
            for r in range(i - 1, i + 2):
                for c in range(j - 1, j + 2):
                    if not self.outOfBorder(r, c):
                        if self.label.board[r][c] == -2:
                            self.label.board[r][c] = 10

            if not self.finish:
                if self.label.board[i][j] <= 8 and self.label.board[i][j] >= 0:
                    # 如果是已经打开的格子
                    if self.chordingFlag(i, j):
                        Fail = False
                        for r in range(i - 1, i + 2):
                            for c in range(j - 1, j + 2):
                                if not self.outOfBorder(r, c):
                                    if (self.label.board[r][c] == 10 or self.label.board[r][c] == -2):
                                        if self.board[r][c] >= 0:
                                            self.DFS(r, c)
                                        else:
                                            Fail = True
                        if Fail:
                            for r in range(i - 1, i + 2):
                                for c in range(j - 1, j + 2):
                                    if not self.outOfBorder(r, c):
                                        if (self.label.board[r][c] == 10 or self.label.board[r][c] == -2)  and self.board[r][c] == -1:
                                            # self.mineLabel[r][c].setPixmap(self.pixmapNum[11])
                                            self.label.board[r][c] = 12
                            self.gameFailed()
            self.label.update()

    def mineMouseMove(self, i, j):
        if not self.finish:
            if not self.outOfBorder(i, j):
                if (i, j) != self.oldCell and (self.leftAndRightHeld or self.leftHeld):
                    ii, jj = self.oldCell
                    self.oldCell = (i, j)
                    if self.leftAndRightHeld:
                        for r in range(ii - 1, ii + 2):
                            for c in range(jj - 1, jj + 2):
                                if not self.outOfBorder(r, c):
                                    if self.label.board[r][c] == -2:
                                        # self.mineLabel[r][c].setPixmap(self.pixmapNum[9])
                                        self.label.board[r][c] = 10
                        for r in range(i - 1, i + 2):
                            for c in range(j - 1, j + 2):
                                if not self.outOfBorder(r, c):
                                    if self.label.board[r][c] == 10:
                                        # self.mineLabel[r][c].setPixmap(self.pixmapNum[0])
                                        self.label.board[r][c] = -2

                    elif self.leftHeld:
                        if self.label.board[i][j] == 10:
                            self.label.board[i][j] = -2
                        if self.label.board[ii][jj] == -2:
                            self.label.board[ii][jj] = 10
            elif self.leftAndRightHeld or self.leftHeld:
                ii, jj = self.oldCell
                if self.leftAndRightHeld:
                    for r in range(ii - 1, ii + 2):
                        for c in range(jj - 1, jj + 2):
                            if not self.outOfBorder(r, c):
                                if self.label.board[r][c] == -2:
                                    self.label.board[r][c] = 10
                elif self.leftHeld:
                    if self.label.board[ii][jj] == -2:
                        self.label.board[ii][jj] = 10
            self.label.update()

    def gameStart(self):  # 画界面，但是不埋雷
        self.mineUnFlagedNum = self.mineNum  # 没有标出的雷，显示在左上角
        self.showMineNum(self.mineUnFlagedNum)    # 在左上角画雷数
        pixmap = QPixmap(self.pixmapNum[14])
        self.label_2.setPixmap(pixmap)
        self.label_2.setScaledContents(True)
        self.time = 0
        self.showTime(self.time)
        self.finish = False
        self.timer.stop()
        self.initMineArea()
        self.gamestart = False
        self.mainWindow.setMinimumSize(0, 0)
        self.mainWindow.resize(0, 0)
        self.board = [[0] * self.column for _ in range(self.row)]
        self.operationStream = []  # 记录整局的鼠标操作流，格式为[('l1',(x,y)),('r1',(x,y)),('c2',(x,y))]
        self.boardofGame = [[10] * self.column for _ in range(self.row)]

    def gameRestart(self):  # 画界面，但是不埋雷，改数据而不是重新生成label
        # 点击脸时调用
        self.time = 0
        self.showTime(self.time)
        self.mineUnFlagedNum = self.mineNum
        self.showMineNum(self.mineUnFlagedNum)
        # pixmap = QPixmap(self.pixmapNum[14])
        # self.label_2.setPixmap(pixmap)
        # self.label_2.setScaledContents(True)
        self.finish = False
        self.timer.stop()
        self.label.board = [[10] * self.column for _ in range(self.row)]
        self.label.update()
        self.gamestart = False

    def gameFinished(self):  # 游戏结束画残局，停时间，改状态
        # print(self.operationStream)#调试用，否则请注释
        self.endTime = time.time()
        self.gameTime = self.endTime - self.startTime # 精确的游戏时间
        self.timer.stop()
        if self.gameWinFlag:
            for idx, row in enumerate(self.board):
                for idy, item in enumerate(row):
                    if item == -1:
                        self.label.board[idx][idy] = 11
        else:
            for idx, row in enumerate(self.board):
                for idy, item in enumerate(row):
                    if item == -1 or self.label.board[idx][idy] == 11 or self.label.board[idx][idy] == 12:
                        if item == -1 and self.label.board[idx][idy] == 11:
                            self.label.board[idx][idy] = 11
                        elif item == -1 and self.label.board[idx][idy] == 10:
                            self.label.board[idx][idy] = 14
                        elif item != -1 and self.label.board[idx][idy] == 11:
                            self.label.board[idx][idy] = 13
                        # elif jj.status == 3:
                        #     jj.setPixmap(self.pixmapNum[11])
        self.label.update()
        self.finish = True
        # print(self.operationStream)

    def isGameFinished(self):
        for i, row in enumerate(self.label.board):
            for j, item in enumerate(row):
                if (item == 10 or item == -2) and self.board[i][j] != -1:
                    return False
        return True

    def gameWin(self):  # 成功后改脸和状态变量
        pixmap = QPixmap(self.pixmapNum[17])
        self.label_2.setPixmap(pixmap)
        self.label_2.setScaledContents(True)
        self.gameWinFlag = True
        self.gameFinished()

    def gameFailed(self): # 失败后改脸和状态变量
        pixmap = QPixmap(self.pixmapNum[16])
        self.label_2.setPixmap(pixmap)
        self.label_2.setScaledContents(True)
        self.gameWinFlag = False
        self.gameFinished()

    def showMineNum(self, n):
        # 显示剩余雷数，雷数大于等于0，小于等于999，整数
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
        ui = gameDefinedParameter.Ui_Form(self.row, self.column, self.mineNum)
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
            self.importLEDPic(self.pixSize)
            self.label.importCellPic(self.pixSize)
            self.label_2.reloadFace(self.pixSize)
            self.gameStart()
            self.mainWindow.setWindowOpacity(ui.transparency / 100)

    def action_QEvent(self):
        # 词典，即游戏帮助、术语表
        self.actionChecked('Q')
        ui = widgetLib.myGameSettingShortcuts()
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

    def showScores(self):
        # 游戏结束后，按空格展示成绩
        if self.finish:
            if self.row == 8 and self.column == 8 and self.mineNum == 10:
                Difficulty = 1
            elif self.row == 16 and self.column == 16 and self.mineNum == 40:
                Difficulty = 2
            elif self.row == 16 and self.column == 30 and self.mineNum == 99:
                Difficulty = 3
            else:
                Difficulty = 4
            scores, scoresValue = minesweeper_master.calScores(self.gameMode, self.gameWinFlag, self.gameTime,
                                                  self.operationStream, self.board, Difficulty)
            ui = gameScores.Ui_Form(scores, scoresValue)
            ui.setModal(True)
            ui.show()
            ui.exec_()

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












