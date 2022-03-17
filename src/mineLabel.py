from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPainter, QColor, QPixmap, QFont
from PyQt5.QtWidgets import QWidget
import ms_toollib as ms

class mineLabel(QWidget):
    # 一整个局面的控件，而不是一个格子
    leftRelease = QtCore.pyqtSignal (int, int)  # 定义信号
    rightRelease = QtCore.pyqtSignal (int, int)
    leftPressed = QtCore.pyqtSignal (int, int)
    rightPressed = QtCore.pyqtSignal (int, int)
    leftAndRightPressed = QtCore.pyqtSignal (int, int)
    leftAndRightRelease = QtCore.pyqtSignal (int, int)
    mouseMove = QtCore.pyqtSignal (int, int)

    def __init__(self, row, column, pixSize):
        super (mineLabel, self).__init__()
        self.ms_board = ms.MinesweeperBoard([[0] * column for _ in range(row)])
        self.leftAndRightClicked = False
        self.paintPossibility = False  # 是否打印概率
        self.pixSize = pixSize
        # self.board = [[10] * column for _ in range(row)]
        # 0~8，10代表未打开，11代表标雷，12代表红雷，13代表叉雷，14代表雷，-2代表被按下的阴影
        self.boardPossibility = [[0.0] * self.ms_board.column for _ in range(self.ms_board.row)]
        self.importCellPic(pixSize)

    def mousePressEvent(self, e):  # 重载一下鼠标点击事件
        xx = e.localPos().x() // self.pixSize
        yy = e.localPos().y() // self.pixSize
        # xx和yy是反的，列、行
        if e.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.RightButton:
            self.ms_board.step(('cc', (yy, xx)))
            self.leftAndRightPressed.emit (yy, xx)
            self.leftAndRightClicked = True
        else:
            if e.buttons () == QtCore.Qt.LeftButton:
                self.ms_board.step(('lc', (yy, xx)))
                self.leftPressed.emit(yy, xx)
            elif e.buttons () == QtCore.Qt.RightButton:
                self.ms_board.step(('rc', (yy, xx)))
                self.rightPressed.emit(yy, xx)

    def mouseReleaseEvent(self, e):
        #每个标签的鼠标事件发射给槽的都是自身的坐标
        #所以获取释放点相对本标签的偏移量，矫正发射的信号
        xx = e.localPos().x() // self.pixSize
        yy = e.localPos().y() // self.pixSize
        # print('抬起位置{}, {}'.format(xx, yy))
        if self.leftAndRightClicked:
            if e.button () == QtCore.Qt.LeftButton:
                self.ms_board.step(('lr', (yy, xx)))
            elif e.button () == QtCore.Qt.RightButton:
                self.ms_board.step(('rr', (yy, xx)))
            self.leftAndRightRelease.emit(yy, xx)
            self.leftAndRightClicked=False
        else:
            if e.button () == QtCore.Qt.LeftButton:
                self.ms_board.step(('lr', (yy, xx)))
                self.leftRelease.emit(yy, xx)
            elif e.button () == QtCore.Qt.RightButton:
                self.ms_board.step(('rr', (yy, xx)))
                self.rightRelease.emit(yy, xx)
    
    def mouseMoveEvent(self, e):

        xx = e.localPos().x()
        yy = e.localPos().y()
        # print('移动位置{}, {}'.format(xx, yy))
        self.mouseMove.emit (yy//self.pixSize, xx//self.pixSize)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter()
        painter.begin(self)
        painter.setFont(QFont('Roman times',8))
        game_board = self.ms_board.game_board
        for i in range(0, self.row):
            for j in range(0, self.column):
                if game_board[i][j] == 10:
                    painter.drawPixmap(j*self.pixSize, i*self.pixSize, QPixmap(self.pixmapNum[9]))
                    if self.paintPossibility:
                        painter.setOpacity(self.boardPossibility[i][j])
                        painter.drawPixmap(j*self.pixSize, i*self.pixSize, QPixmap(self.pixmapNum[14]))
                        painter.setOpacity(1.0)
                elif game_board[i][j] <= 0:
                    painter.drawPixmap(j*self.pixSize, i*self.pixSize, QPixmap(self.pixmapNum[0]))
                elif game_board[i][j] == 1:
                    painter.drawPixmap(j*self.pixSize, i*self.pixSize, QPixmap(self.pixmapNum[1]))
                elif game_board[i][j] == 2:
                    painter.drawPixmap(j*self.pixSize, i*self.pixSize, QPixmap(self.pixmapNum[2]))
                elif game_board[i][j] == 3:
                    painter.drawPixmap(j*self.pixSize, i*self.pixSize, QPixmap(self.pixmapNum[3]))
                elif game_board[i][j] == 4:
                    painter.drawPixmap(j*self.pixSize, i*self.pixSize, QPixmap(self.pixmapNum[4]))
                elif game_board[i][j] == 5:
                    painter.drawPixmap(j*self.pixSize, i*self.pixSize, QPixmap(self.pixmapNum[5]))
                elif game_board[i][j] == 6:
                    painter.drawPixmap(j*self.pixSize, i*self.pixSize, QPixmap(self.pixmapNum[6]))
                elif game_board[i][j] == 7:
                    painter.drawPixmap(j*self.pixSize, i*self.pixSize, QPixmap(self.pixmapNum[7]))
                elif game_board[i][j] == 8:
                    painter.drawPixmap(j*self.pixSize, i*self.pixSize, QPixmap(self.pixmapNum[8]))
                elif game_board[i][j] == 11:
                    painter.drawPixmap(j*self.pixSize, i*self.pixSize, QPixmap(self.pixmapNum[10]))
                elif game_board[i][j] == 12:
                    painter.drawPixmap(j*self.pixSize, i*self.pixSize, QPixmap(self.pixmapNum[11]))
                elif game_board[i][j] == 13:
                    painter.drawPixmap(j*self.pixSize, i*self.pixSize, QPixmap(self.pixmapNum[13]))
                elif game_board[i][j] == 14:
                    painter.drawPixmap(j*self.pixSize, i*self.pixSize, QPixmap(self.pixmapNum[12]))
        painter.end()

    def importCellPic(self, pixSize):
        # 导入资源，并缩放到希望的尺寸、比例
        pixmap0 = QPixmap("media/10.png")
        pixmap1 = QPixmap("media/11.png")
        pixmap2 = QPixmap("media/12.png")
        pixmap3 = QPixmap("media/13.png")
        pixmap4 = QPixmap("media/14.png")
        pixmap5 = QPixmap("media/15.png")
        pixmap6 = QPixmap("media/16.png")
        pixmap7 = QPixmap("media/17.png")
        pixmap8 = QPixmap("media/18.png")
        pixmap9 = QPixmap("media/00.png")
        pixmap_mine = QPixmap("media/01.png")
        pixmap10 = QPixmap("media/03.png")
        pixmap11 = QPixmap("media/02.png")
        pixmap12 = QPixmap("media/01.png")
        pixmap13 = QPixmap("media/04.png")
        pixmap0 = pixmap0.scaled(pixSize, pixSize)
        pixmap1 = pixmap1.scaled(pixSize, pixSize)
        pixmap2 = pixmap2.scaled(pixSize, pixSize)
        pixmap3 = pixmap3.scaled(pixSize, pixSize)
        pixmap4 = pixmap4.scaled(pixSize, pixSize)
        pixmap5 = pixmap5.scaled(pixSize, pixSize)
        pixmap6 = pixmap6.scaled(pixSize, pixSize)
        pixmap7 = pixmap7.scaled(pixSize, pixSize)
        pixmap8 = pixmap8.scaled(pixSize, pixSize)
        pixmap9 = pixmap9.scaled(pixSize, pixSize)
        pixmap_mine = pixmap_mine.scaled(pixSize, pixSize)
        pixmap10 = pixmap10.scaled(pixSize, pixSize)
        pixmap11 = pixmap11.scaled(pixSize, pixSize)
        pixmap12 = pixmap12.scaled(pixSize, pixSize)
        pixmap13 = pixmap13.scaled(pixSize, pixSize)
        self.pixmapNum = {0: pixmap0, 1: pixmap1, 2: pixmap2, 3: pixmap3, 4: pixmap4,
                     5: pixmap5, 6: pixmap6, 7: pixmap7, 8: pixmap8, 9: pixmap9,
                     10: pixmap10, 11: pixmap11, 12: pixmap12, 13: pixmap13, 14:pixmap_mine}




    
            

            
            
        