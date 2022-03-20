from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPainter, QColor, QPixmap, QFont
from PyQt5.QtWidgets import QWidget
import ms_toollib as ms
# from PyQt5.QtSvg import QSvgWidget


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
        self.row = row
        self.column = column
        self.ms_board = ms.MinesweeperBoard([[0] * column for _ in range(row)])
        self.paintPossibility = False  # 是否打印概率
        self.pixSize = pixSize
        self.boardPossibility = [[0.0] * self.ms_board.column for _ in range(self.ms_board.row)]
        self.importCellPic(pixSize)
        self.resize(QtCore.QSize(pixSize * column, pixSize * row))
        
        self.current_x = row # 鼠标坐标，和高亮的展示有关
        self.current_y = column

    def mousePressEvent(self, e):  # 重载一下鼠标点击事件
        xx = int(e.localPos().x() // self.pixSize)
        yy = int(e.localPos().y() // self.pixSize)
        if yy < 0 or xx < 0 or yy >= self.row or xx >= self.column:
            self.current_x = self.row
            self.current_y = self.column
        else:
            self.current_x = yy
            self.current_y = xx
        # xx和yy是反的，列、行
        if e.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.RightButton:
            self.leftAndRightPressed.emit(self.current_x, self.current_y)
        else:
            if e.buttons () == QtCore.Qt.LeftButton:
                self.leftPressed.emit(self.current_x, self.current_y)
            elif e.buttons () == QtCore.Qt.RightButton:
                self.rightPressed.emit(self.current_x, self.current_y)

    def mouseReleaseEvent(self, e):
        #每个标签的鼠标事件发射给槽的都是自身的坐标
        #所以获取释放点相对本标签的偏移量，矫正发射的信号
        xx = int(e.localPos().x() // self.pixSize)
        yy = int(e.localPos().y() // self.pixSize)
        # print('抬起位置{}, {}'.format(xx, yy))
        # print(e.button ())
        if yy < 0 or xx < 0 or yy >= self.row or xx >= self.column:
            self.current_x = self.row
            self.current_y = self.column
        else:
            self.current_x = yy
            self.current_y = xx
        if e.button() == QtCore.Qt.LeftButton:
            self.leftRelease.emit(self.current_x, self.current_y)
        elif e.button () == QtCore.Qt.RightButton:
            self.rightRelease.emit(self.current_x, self.current_y)

    def mouseMoveEvent(self, e):
        xx = int(e.localPos().x() // self.pixSize)
        yy = int(e.localPos().y() // self.pixSize)
        # print('移动位置{}, {}'.format(xx, yy))
        if yy < 0 or xx < 0 or yy >= self.row or xx >= self.column:
            self.current_x = self.row
            self.current_y = self.column
        else:
            self.current_x = yy
            self.current_y = xx
        self.mouseMove.emit(yy, xx)

    def paintEvent(self, event):
        super().paintEvent(event)
        pix_size = self.pixSize
        painter = QPainter()
        painter.begin(self)
        # 画游戏局面
        game_board = self.ms_board.game_board
        for i in range(self.row):
            for j in range(self.column):
                if game_board[i][j] == 10:
                    painter.drawPixmap(j * pix_size, i * pix_size, QPixmap(self.pixmapNum[10]))
                    if self.paintPossibility:
                        painter.setOpacity(self.boardPossibility[i][j])
                        painter.drawPixmap(j * pix_size, i * pix_size, QPixmap(self.pixmapNum[100]))
                        painter.setOpacity(1.0)
                else:
                    painter.drawPixmap(j * pix_size, i * pix_size, QPixmap(self.pixmapNum[game_board[i][j]]))
        # 画高亮
        if (self.ms_board.game_board_state == 2 or self.ms_board.game_board_state == 1) and\
            not self.paintPossibility and self.current_x < self.row and self.current_y < self.column:
            if self.ms_board.mouse_state == 5 or self.ms_board.mouse_state == 6:
                for r in range(max(self.current_x - 1, 0), min(self.current_x + 2, self.row)):
                    for c in range(max(self.current_y - 1, 0), min(self.current_y + 2, self.column)):
                        if game_board[r][c] == 10:
                            painter.drawPixmap(c * pix_size, r * pix_size, QPixmap(self.pixmapNum[0]))
            elif self.ms_board.mouse_state == 4 and game_board[self.current_x][self.current_y] == 10:
                painter.drawPixmap(self.current_y * pix_size, self.current_x * pix_size, QPixmap(self.pixmapNum[0]))
        painter.end()

    def importCellPic(self, pixSize):
        # 导入资源，并缩放到希望的尺寸、比例
        celldown = QPixmap("media/celldown.svg").scaled(pixSize, pixSize)
        cell1 = QPixmap("media/cell1.svg").scaled(pixSize, pixSize)
        cell2 = QPixmap("media/cell2.svg").scaled(pixSize, pixSize)
        cell3 = QPixmap("media/cell3.svg").scaled(pixSize, pixSize)
        cell4 = QPixmap("media/cell4.svg").scaled(pixSize, pixSize)
        cell5 = QPixmap("media/cell5.svg").scaled(pixSize, pixSize)
        cell6 = QPixmap("media/cell6.svg").scaled(pixSize, pixSize)
        cell7 = QPixmap("media/cell7.svg").scaled(pixSize, pixSize)
        cell8 = QPixmap("media/cell8.svg").scaled(pixSize, pixSize)
        cellup = QPixmap("media/cellup.svg").scaled(pixSize, pixSize)
        cellmine = QPixmap("media/cellmine.svg").scaled(pixSize, pixSize) # 白雷
        cellflag = QPixmap("media/cellflag.svg").scaled(pixSize, pixSize) # 标雷
        blast = QPixmap("media/blast.svg").scaled(pixSize, pixSize) # 红雷
        falsemine = QPixmap("media/falsemine.svg").scaled(pixSize, pixSize) # 叉雷
        mine = QPixmap("media/mine.svg").scaled(pixSize, pixSize)
        self.pixmapNum = {0: celldown, 1: cell1, 2: cell2, 3: cell3, 4: cell4,
                     5: cell5, 6: cell6, 7: cell7, 8: cell8, 9: None,
                     10: cellup, 11: cellflag, 12: None, 13: None, 14: falsemine,
                     15: blast, 16: cellmine, 100: mine}
        


