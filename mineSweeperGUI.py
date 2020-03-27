from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer, QCoreApplication
from PyQt5.QtGui import QPalette, QPixmap, QFont, QIcon
from PyQt5.QtWidgets import QLineEdit, QInputDialog
import superGUI, mineLabel,selfDefinedParameter
import random, sip
import minesweeper_master


class MineSweeperGUI(superGUI.Ui_MainWindow):
    def __init__(self, MainWindow):
        self.row = 8
        self.column = 8
        self.mineNum = 10
        self.finish = False
        self.gamestart = False
        self.mainWindow = MainWindow
        self.mainWindow.setWindowIcon(QIcon("media/mine.ico"))
        self.mainWindow.setFixedSize(self.mainWindow.minimumSize())
        self.setupUi(self.mainWindow)
        self.mineLabel = []#局面
        
        pixmap0=QPixmap("media/10.png")
        pixmap1=QPixmap("media/11.png")
        pixmap2=QPixmap("media/12.png")
        pixmap3=QPixmap("media/13.png")
        pixmap4=QPixmap("media/14.png")
        pixmap5=QPixmap("media/15.png")
        pixmap6=QPixmap("media/16.png")
        pixmap7=QPixmap("media/17.png")
        pixmap8=QPixmap("media/18.png")
        pixmap9=QPixmap("media/00.png")
        pixmap10=QPixmap("media/03.png")
        self.pixmapNum={0:pixmap0,1:pixmap1,2:pixmap2,3:pixmap3,4:pixmap4,
                   5:pixmap5,6:pixmap6,7:pixmap7,8:pixmap8,9:pixmap9,10:pixmap10}
        
        self.initMineArea()
        self.label_2.leftRelease.connect(self.gameRestart)
        pixmap = QPixmap("media/f0.png")
        self.label_2.setPixmap(pixmap)
        self.label_2.setScaledContents(True)
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.black)  # 设置字体颜色
        self.label_3.setPalette(pe)
        self.label_3.setFont(QFont("Roman times", 15, QFont.Bold))
        self.label.setPalette(pe)
        self.label.setFont(QFont("Roman times", 15, QFont.Bold))
        self.label.setText(str(self.mineNum))
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timeCount)
        self.timeStart = False

        # 绑定菜单栏事件
        self.action.triggered.connect(self.gameRestart)
        self.action_B.triggered.connect(self.action_BEvent)
        self.action_I.triggered.connect(self.action_IEvent)
        self.action_E.triggered.connect(self.action_Event)
        self.action_C.triggered.connect(self.action_CEvent)
        self.action_X_2.triggered.connect(QCoreApplication.instance().quit)
        self.actionChecked('B')  # 默认选择初级
        
    def outOfBorder(self, i, j):
        if i < 0 or i >= self.row or j < 0 or j >= self.column:
            return True
        return False

    def layMine(self,i,j):    #mineLabel[r][c].num是真实局面，-1为雷，数字为数字
        xx=self.row
        yy=self.column
        num = self.mineNum
        Board = minesweeper_master.layMineSolvable(xx , yy , num , i , j)
        
        
        for r in range(0, xx):
            for c in range(0, yy):
                self.mineLabel[r][c].num = Board[r][c]
        

    def initMineArea(self):
        self.gridLayout.setSpacing(0) #网格布局间距为0
        for i in range(0, self.row):
            self.mineLabel.append([])
            for j in range(0, self.column):
                label = mineLabel.mineLabel(i, j, 0, "")
                label.setPixmap(self.pixmapNum[9])
                label.setMinimumSize(32, 32)   #改局面中的方格大小
                label.setAlignment(Qt.AlignCenter)

                # 绑定雷区点击事件
                label.leftPressed.connect(self.mineAreaLeftPressed)
                label.leftAndRightPressed.connect(self.mineAreaLeftAndRightPressed)
                label.leftAndRightRelease.connect(self.mineAreaLeftAndRightRelease)
                label.leftRelease.connect(self.mineAreaLeftRelease)
                label.rightPressed.connect(self.mineAreaRightPressed)
                label.setStyleSheet("border:0px solid red")

                self.mineLabel[i].append(label)
                self.gridLayout.addWidget(label, i, j)#把子控件添加到网格布局管理器中

    def timeCount(self):
        self.label_3.setText(str(int(self.label_3.text()) + 1))

    def DFS(self, i, j, start0):
        if self.mineLabel[i][j].status == 0:
            self.mineLabel[i][j].status = 1
            if self.mineLabel[i][j].num >= 0:
                if not self.timeStart:
                    self.timeStart = True
                    self.timer.start()
                self.mineLabel[i][j].setPixmap(self.pixmapNum[self.mineLabel[i][j].num])
            if self.isGameFinished():
                self.gameWin()
            if self.mineLabel[i][j].num == 0:
                for r in range(i - 1, i + 2):
                    for c in range(j - 1, j + 2):
                        if not self.outOfBorder(r, c) and self.mineLabel[r][
                            c].status == 0 and self.mineLabel[r][c].num != -1:
                            self.DFS(r, c, start0)

    def mineAreaLeftRelease(self, i, j):
        if not self.gamestart:
            self.layMine(i,j)
            self.gamestart=True
        if not self.finish:
            if self.mineLabel[i][j].num >= 0:
                self.DFS(i, j, self.mineLabel[i][j].num == 0)
                if self.isGameFinished():
                    self.gameWin()
            else:
                self.gameFailed()

    def mineAreaRightPressed(self, i, j):
        if not self.finish:
            if self.mineLabel[i][j].status == 0:
                pixmap = QPixmap(self.pixmapNum[10])
                self.mineLabel[i][j].setPixmap(pixmap)
                self.mineLabel[i][j].setScaledContents(True)
                self.mineLabel[i][j].status = 2
                self.label.setText(str(int(self.label.text()) - 1))
            elif self.mineLabel[i][j].status == 2:
                self.mineLabel[i][j].setPixmap(self.pixmapNum[9])
                self.mineLabel[i][j].status = 0
                self.label.setText(str(int(self.label.text()) + 1))

    def mineAreaLeftPressed(self, i, j):
        pass

    def mineAreaLeftAndRightPressed(self, i, j):
#        return 0
        if not self.finish:
            if self.mineLabel[i][j].status == 1:
                count = 0
                for r in range(i - 1, i + 2):
                    for c in range(j - 1, j + 2):
                        if not self.outOfBorder(r, c):
                            if self.mineLabel[r][c].status == 0:
                                self.mineLabel[r][c].setFrameShape(QtWidgets.QFrame.Panel)
                                self.mineLabel[r][c].setFrameShadow(QtWidgets.QFrame.Sunken)
                            elif self.mineLabel[r][c].status == 2:
                                count += 1
                return count == self.mineLabel[i][j].num
            else:
                return False

    def mineAreaLeftAndRightRelease(self, i, j):
        if not self.finish:
            if self.mineLabel[i][j].status == 1:
                if self.mineAreaLeftAndRightPressed(i, j):
                    Fail = False
                    for r in range(i - 1, i + 2):
                        for c in range(j - 1, j + 2):
                            if not self.outOfBorder(r, c):
                                if self.mineLabel[r][c].status == 0:
                                    if self.mineLabel[r][c].num >= 0:
                                        self.DFS(r, c, self.mineLabel[r][c].num == 0)
                                    else:
                                        Fail = True
                    if Fail:
                        self.gameFailed()
                else:
                    for r in range(i - 1, i + 2):
                        for c in range(j - 1, j + 2):
                            if not self.outOfBorder(r, c):
                                if self.mineLabel[r][c].status == 0:
                                    self.mineLabel[r][c].setFrameShape(QtWidgets.QFrame.Panel)
                                    self.mineLabel[r][c].setFrameShadow(QtWidgets.QFrame.Sunken)

    def gameStart(self):#画界面，但是不埋雷
        for i in self.mineLabel:
            for j in i:
                self.gridLayout.removeWidget(j)
                sip.delete(j)
        self.label.setText(str(self.mineNum))
        pixmap = QPixmap("media/f0.png")
        self.label_2.setPixmap(pixmap)
        self.label_2.setScaledContents(True)
        self.label_3.setText("0")
        self.timeStart = False
        self.finish = False
        self.timer.stop()
        self.mineLabel.clear()
        self.mineLabel = []
        self.initMineArea()
        self.gamestart = False
        self.mainWindow.setMinimumSize(0, 0)
        self.mainWindow.resize(self.mainWindow.minimumSize())
        #把窗口尽量缩小，以免从高级改成中级时窗口不能缩小
    
    def gameRestart(self):#画界面，但是不埋雷，改数据而不是重新生成label
        #点击脸时调用
        self.label.setText(str(self.mineNum))
        pixmap = QPixmap("media/f0.png")
        self.label_2.setPixmap(pixmap)
        self.label_2.setScaledContents(True)
        self.label_3.setText("0")
        self.timeStart = False
        self.finish = False
        self.timer.stop()
        for i in range(0, self.row):
            for j in range(0, self.column):
                self.mineLabel[i][j].status = 0
                self.mineLabel[i][j].setPixmap(self.pixmapNum[9])
        self.gamestart = False
        #把窗口尽量缩小，以免从高级改成中级时窗口不能缩小

    def gameFinished(self):#游戏结束画残局，停时间，改状态
        for i in self.mineLabel:
            for j in i:
                if j.num == -1 or j.status == 2:
                    j.setFrameShape(QtWidgets.QFrame.Panel)
                    j.setFrameShadow(QtWidgets.QFrame.Sunken)
                    if j.num == -1 and j.status == 2:
                        pixmap = QPixmap("media/03.png")
                    elif j.num == -1:
                        pixmap = QPixmap("media/01.png")
                    else:
                        pixmap = QPixmap("media/04.png")
                    j.setPixmap(pixmap)
                    j.setScaledContents(True)
                j.status = 1
        self.timer.stop()
        self.finish = True

    def isGameFinished(self):
        for i in self.mineLabel:
            for j in i:
                if j.status == 0 and j.num != -1:
                    return False
        return True

    def gameWin(self):
        pixmap = QPixmap("media/f3.png")
        self.label_2.setPixmap(pixmap)
        self.label_2.setScaledContents(True)
        self.gameFinished()

    def gameFailed(self):
        pixmap = QPixmap("media/f2.png")
        self.label_2.setPixmap(pixmap)
        self.label_2.setScaledContents(True)
        self.gameFinished()

    def actionChecked(self, k):
        self.action_B.setChecked(False)
        self.action_I.setChecked(False)
        self.action_E.setChecked(False)
        self.action_C.setChecked(False)
        if k == 'B':
            self.action_B.setChecked(True)
        elif k == 'I':
            self.action_I.setChecked(True)
        elif k == 'E':
            self.action_E.setChecked(True)
        elif k == 'C':
            self.action_C.setChecked(True)

    def action_BEvent(self):
        self.actionChecked('B')
        self.row = 8
        self.column = 8
        self.mineNum = 10
        self.gameStart()

    def action_IEvent(self):
        self.actionChecked('I')
        self.row = 16
        self.column = 16
        self.mineNum = 40
        self.gameStart()

    def action_Event(self):
        self.actionChecked('E')
        self.row = 16
        self.column = 30
        self.mineNum = 99
        self.gameStart()

    def action_CEvent(self):
        self.actionChecked('C')
        ui = selfDefinedParameter.Ui_Dialog(self.row, self.column,
                                            self.mineNum)
        ui.Dialog.setModal(True)
        ui.Dialog.show()
        ui.Dialog.exec_()
        if ui.alter:
            self.row = ui.row
            self.column = ui.column
            self.mineNum = ui.mineNum
            self.gameStart()
