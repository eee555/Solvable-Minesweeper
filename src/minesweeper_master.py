# author : Wang Jianing(18201)
from random import shuffle, choice
# from random import randint, seed, sample
from typing import List
# import time
from safe_eval import safe_eval
import configparser

import ms_toollib as ms
import math

# OutputEnable = 0
# seedNum = 60223
EnuLimit = 40

def choose_3BV(board_constraint, attempt_times_limit, params):
    # def choose_3BV_laymine(laymine):
    #     t = 0
    #     while t < attempt_times_limit:
    #         ans = laymine(params)
    #         if not isinstance(ans, tuple):
    #             ans = (ans, True)
            
    #         if min_3BV <= ms.cal3BV(ans[0]) <= max_3BV:
    #             return (ans[0], True and ans[1])
    #     return (ans[0], False)
    # return choose_3BV_laymine
    def choose_3BV_laymine(laymine):
        if not board_constraint:
            b = laymine(params)
            if isinstance(b, tuple):
                b, success_flag = b
            else:
                success_flag = True
            return (b, success_flag)
        t = 0
        while t < attempt_times_limit:
            b = laymine(params)
            if isinstance(b, tuple):
                b, success_flag = b
            else:
                success_flag = True
                
            constraints = {
                "sin": math.sin,
                "tan": math.tan,
                "cos": math.cos,
                } # 也许还要加row, column, mine_num, level, mode
            wrapper_b = ms.Board(b)
            if "bbbv" in board_constraint:
                constraints.update({"bbbv": wrapper_b.bbbv})
            if "op" in board_constraint:
                constraints.update({"op": wrapper_b.op})
            if "isl" in board_constraint:
                constraints.update({"isl": wrapper_b.isl})
            if "cell0" in board_constraint:
                constraints.update({"cell0": wrapper_b.cell0})
            if "cell1" in board_constraint:
                constraints.update({"cell1": wrapper_b.cell1})
            if "cell2" in board_constraint:
                constraints.update({"cell2": wrapper_b.cell2})
            if "cell3" in board_constraint:
                constraints.update({"cell3": wrapper_b.cell3})
            if "cell4" in board_constraint:
                constraints.update({"cell4": wrapper_b.cell4})
            if "cell5" in board_constraint:
                constraints.update({"cell5": wrapper_b.cell5})
            if "cell6" in board_constraint:
                constraints.update({"cell6": wrapper_b.cell6})
            if "cell7" in board_constraint:
                constraints.update({"cell7": wrapper_b.cell7})
            if "cell8" in board_constraint:
                constraints.update({"cell8": wrapper_b.cell8})
            try:
                expression_flag = safe_eval(board_constraint, globals=constraints)
            except:
                return (b, success_flag)
            if expression_flag:
                return (b, success_flag)
            t += 1
        return (b, success_flag)
    return choose_3BV_laymine
    
# 此处的board，看似是函数，实际由于装饰器的缘故是一个局面的列表
def laymine_solvable_thread(board_constraint, attempt_times_limit, params):
    @choose_3BV(board_constraint, attempt_times_limit, params)
    def board(pp):
        return ms.laymine_solvable_thread(*pp)
    return board

def laymine(board_constraint, attempt_times_limit, params):
    @choose_3BV(board_constraint, attempt_times_limit, params)
    def board(pp):
        return ms.laymine(*pp)
    return board

def laymine_op(board_constraint, attempt_times_limit, params):
    @choose_3BV(board_constraint, attempt_times_limit, params)
    def board(pp):
        return ms.laymine_op(*pp)
    return board

def laymine_solvable_adjust(board_constraint, attempt_times_limit, params):
    # 暂时用不了
    @choose_3BV(board_constraint, attempt_times_limit, params)
    def board(pp):
        return ms.laymine_solvable_adjust(*pp)
    return board

def get_mine_times_limit(row: int, column: int):
    '''
    计算局面的雷数上限和尝试次数上限。当雷数小于等于雷数上限时，才可以用筛选法(考虑游戏体验)。
    
    Parameters
    ----------
    row : int
        >= 1, 行数/高。
    column : int
        >= 1, 列数/宽。

    Returns
    -------
    int
        雷数上限。
    int
        尝试次数上限。

    '''
    area = row * column
    if area <= 64:
        return (int(area * 0.375) + 1, 100000)
    elif area <= 256:
        return (int(area * (-area * 0.00048828125 + 0.40625)) + 2, 100000)
    elif area <= 480:
        return (int(area * (-area * 0.00013950892857 + 0.3169642857136)) + 2, 100000)
    elif area <= 864:
        return (int(area * (-area * 4.8225308641979135e-05 + 0.27314814814814997)) + 2, 50000)
    elif area <= 6400:
        return (int(area * (-area * 5.686683793619943e-06 + 0.23639477627916763)) + 2, 20000)
    else:
        return (int(area * 0.2) + 2, 10000)

def laymine_solvable_auto(row, column, mine_num, x, y):
    # 自动选择方式的无猜埋雷
    (max_mine_num, max_times) = get_mine_times_limit(row, column)
    if mine_num <= max_mine_num:
        ans = ms.laymine_solvable_thread(row, column, mine_num, x, y, max_times)
        if ans[1]:
            return ans
    return ms.laymine_solvable_adjust(row, column, mine_num, x, y)
    
    
def laymine_solvable(board_constraint, attempt_times_limit, params):
    @choose_3BV(board_constraint, attempt_times_limit, params)
    def board(pp):
        return laymine_solvable_auto(*pp)
    return board

def refreshBoard2(Board , BoardofGame, ClickedPoses):
    # 给出点击位置，刷新局面
    # 参数：局面，游戏局面，点击位置，可以同时点多个位置
    # ClickedPoses一定不能是雷，是列表格式
    # 拟弃用，工具箱里也有
    Row=len(Board)
    Column=len(Board[0])
    while ClickedPoses:
        (i, j) = ClickedPoses.pop()
        if Board[i][j] > 0:
            BoardofGame[i][j] = Board[i][j]
        elif Board[i][j] == 0:
            BoardofGame[i][j] = 0
            for m in range(max(0, i-1), min(Row, i+2)):
                for n in range(max(0, j-1), min(Column, j+2)):
                    if (i != m or j != n) and BoardofGame[m][n] == 10:
                        ClickedPoses.append((m,n))
    return BoardofGame



def Victory(BoardofGame,Board):
    # 判断当前是否获胜
    # 游戏局面中必须没有标错的雷
    # 工具箱里也有，但没暴露
    Row = len(BoardofGame)
    Col = len(BoardofGame[0])
    for i in range(0,Row):
        for j in range(0,Col):
            if BoardofGame[i][j] == 10 and Board[i][j] != -1:
                return 0
    return 1


def enumerateChangeBoard(board, BoardofGame, xx, yy) -> (List[List[int]], bool):
    # 等可能给出全部可能情况中(i,j)不为雷的随机一种情况,此时(i,j)一定是未打开状态；
    # 但若超过最大枚举长度，
    # 将返回非随机的某一种可能的情况（暂未实现），若剩余位置数少于雷数，则返回原图
    # 直接返回改好的图和flag，0是改图失败，1是成功
    # 理论上（xx,yy）原本必须是雷
    # 局限：有时候，重排需要用更多的雷，但内部方格里没有这么多雷，本算法不能从
    #       边缘方格中抽取雷

    # MatrixA, Matrixx, Matrixb = refreshMatrix(BoardofGame)
    # # mineLabel0 = board.copy() # 备份，重排失败后启用

    # #先判定是否是必然的雷，即有没有枚举的必要
    # BoardofGame,NotMine,flag= SolveDirect(MatrixA, Matrixx, Matrixb, BoardofGame)
    # if BoardofGame[xx][yy] == 11:
    #     return board, False
    # else:
    #     MatrixA, Matrixx, Matrixb = refreshMatrix(BoardofGame)
    #     BoardofGame, NotMine,flag= SolveMinus(MatrixA, Matrixx, Matrixb, BoardofGame)
    #     if BoardofGame[xx][yy] == 11:
    #         return board, False
    if not isinstance(board, list):
        board = board.into_vec_vec()
    if ms.is_guess_while_needless(BoardofGame, (xx, yy)) == 4:
        return board, False# 踩到必然的雷
    
    MatrixA, Matrixx, Matrixb = ms.refresh_matrix(BoardofGame)
    MatrixColumn = len(Matrixx)
    MatrixRow = len(Matrixb)

    #统计一下一共有几个雷
    MineNum0 = 0
    Mineinside = 0  # 内部的雷数
    for idm, m in enumerate(board):
        for idn, n in enumerate(m):
            if n == -1:
                MineNum0 += 1
                if (idm, idn) not in Matrixx:
                    Mineinside += 1

    #再判断是不是内部的雷
    if (xx,yy) not in Matrixx:
        board[xx][yy] = 9
        # 如果是内部的雷，就直接改成非雷,而且是正常情况绝不会出现的数做记号
        board = refreshMineLable(board, MineNum0, BoardofGame)
        return board, True

    Id = Matrixx.index((xx,yy))
    MatrixRow = len(Matrixb)
    #第二步，整理成分块矩阵
    ColId = list(range(MatrixColumn))
    RowId = list(range(MatrixRow))
    GroupCol = []  #单个组的临时索引
    GroupRow = []
    Groupb = []
    Groupx = []
    TempCol = []
    TempRow = []
    TempCol.append(Id)
    ColId.remove(Id)
    while TempCol or TempRow:
        if TempCol:
            for i in range(MatrixRow):
                if MatrixA[i][TempCol[-1]] == 1:
                    if i in RowId:
                        TempRow.append(i)
                        RowId.remove(i)
            temp = TempCol.pop()
            GroupCol.append(temp)
            Groupx.append(Matrixx[temp])
        if TempRow:
            for j in range(MatrixColumn):
                if MatrixA[TempRow[-1]][j] == 1: #越界，当只剩最后一个2*2的二选一时
                    if j in ColId:
                        TempCol.append(j)
                        ColId.remove(j)
            temp = TempRow.pop()
            GroupRow.append(temp)
            Groupb.append(Matrixb[temp])

    if len(GroupCol) >= EnuLimit:#枚举法的极限
        #超过枚举极限时，暂时不能给出可能的解，有待升级
        return board, False
        # newTable, flag = boardFastSol(MatrixA,Matrixx,Matrixb,GroupCol,GroupRow,Id)

    AllTable = [[2]*len(GroupCol)]
    for i in GroupRow:
        b = Matrixb[i]
        TableId = []
        for j in GroupCol:
            if MatrixA[i][j] == 1:
                TableId.append(GroupCol.index(j))
        # if not AllTable:
        #     return mineLabel0, 0
        AllTable = ms.enuOneStep(AllTable, TableId, b)

    for index, item in enumerate(AllTable[:]):
        # 删除重排后原位置还是雷的情况
        # 前面的步骤保证AllTable的第一列一定是代表(xx,yy)，所以只要删除首位是雷的可能
        if item[0] == 1:
            AllTable.remove(item)
    if not AllTable:
        return board, False
    newTable = choice(AllTable)#随机抽取列表中某个元素
    #随机重排后可能雷数有增减

    deltaMine = 0  # 重排前后相差的雷数不能超过内部的雷数
    for index, item in enumerate(GroupCol):
        (m,n) = Matrixx[item]
        deltaMine = deltaMine + newTable[index] - (board[m][n] == -1)
    if deltaMine > Mineinside:
        return board, False

    for index, item in enumerate(GroupCol):
        (m,n) = Matrixx[item]
        board[m][n] = -newTable[index]


    board[xx][yy] = 9
    board = refreshMineLable(board, MineNum0, BoardofGame)

    return board, True

def refreshMineLable(board, MineNum0, BoardofGame):
    # 该刷新用在局面重排后
    # 根据真实局面和游戏局面，以及总雷数，刷新真实局面
    # 游戏局面是不变的，真实局面的未打开的数字会刷新
    # 如果有雷数的增减，则内部的雷会重排
    # 请保证雷数不多于内部格数
    Row = len(board)
    Column = len(board[0])
    MineNum1 = 0
    for i in board:
        for j in i:
            if j == -1:
                MineNum1 += 1
    #如果雷数不一样，内部就要重排
    if not MineNum1 == MineNum0:
        posInside = []
        mineNumInside = 0
        for x, itemx in enumerate(board):
            for y, itemy in enumerate(itemx):
                insideFlag = 1
                for i in range(max(0, x - 1), min(Row, x + 2)):
                    for j in range(max(0, y - 1), min(Column, y + 2)):
                        if not BoardofGame[i][j] == 10:
                        # BoardofGame 和 board的区别是后者是玩家标的雷可能乱标雷
                        # 而前者的雷都是算法标上去的
                            insideFlag = 0
                if insideFlag and itemy != 9:
                    posInside.append((x, y))
                    if itemy == -1:
                        mineNumInside += 1
        #改正总的雷数
        mineNumInside = mineNumInside + MineNum0 - MineNum1
        posNum = len(posInside) - mineNumInside
        # if posNum < 0: # 这种情况是内部格子数比雷数少，重排失败
        #     return mineLabel, 0
        #重新布内部的雷
        newInsideBoard = [-1] * mineNumInside + [0] * (posNum)
        shuffle(newInsideBoard)
        for index, (x, y) in enumerate(posInside[:]):
            board[x][y] = newInsideBoard[index]
    # 重排完毕，开始刷新
    for x, itemx in enumerate(board):
        for y, itemy in enumerate(itemx):
            if not itemy == -1:
                boardNum = 0
                for i in range(max(0, x - 1), min(Row, x + 2)):
                    for j in range(max(0, y - 1), min(Column, y + 2)):
                        if board[i][j] == -1:
                            boardNum += 1
                board[x][y] = boardNum
    return board

def trans_expression(expression: str):
    expression = expression.lower().strip()
    expression = expression.replace("3bv", "bbbv")
    expression = expression.replace("opening", "op")
    expression = expression.replace("click", "cl")
    expression = expression.replace("\"", "'")
    expression = expression.replace("island", "isl")
    expression = expression.replace("chording", "double")
    expression = expression.replace("solved_bbbv", "bbbv_solved")
    return expression

# isSolvable = ms_toollib.py_isSolvable
# isSolvable2(Board, X0, Y0, enuLimit)
# 从指定位置开始扫，判断局面是否无猜
# 周围一圈都是雷，那么中间是雷不算猜，中间不是雷算猜

def trans_game_mode(mode: int) -> str:
    if mode == 0:
        return '标准'
    elif mode == 1:
        return 'upk'
    elif mode == 2:
        return 'cheat'
    elif mode == 3:
        return 'Density'
    elif mode == 4:
        return 'win7'
    elif mode == 5:
        return '竞速无猜'
    elif mode == 6:
        return '强无猜'
    elif mode == 7:
        return '弱无猜'
    elif mode == 8:
        return '准无猜'
    elif mode == 9:
        return '强可猜'
    elif mode == 10:
        return '弱可猜'
    
class abstract_game_board(object):
    __slots__ = ('game_board', 'mouse_state', 'game_board_state')
    def reset(self, *args):
        ...
    def step(self, *args):
        ...
        

# unsolvableStructure = ms_toollib.py_unsolvableStructure
# unsolvableStructure2(BoardCheck)
# 用几种模板，检测局面中是否有明显的死猜的结构
# 不考虑起手位置，因为起手必开空
# 局面至少大于4*4
# 返回0或1

def print2(arr, mode = 0):
    # 调试时便于打印 print2(BoardofGame)
    if mode == 0:
        for i in arr:
            for j in i:
                print('%2.d'%j, end=', ')
            print()
    elif mode == 1:
        for i in arr:
            for j in i:
                print('%2.d'%j.num, end=', ')
            print()
    elif mode == 2:
        for i in arr:
            for j in i:
                print('%2.d'%j.status, end=', ')
            print()

def debug_ms_board(ms_board):
    for i in range(ms_board.events_len):
        print(f"{ms_board.events_time(i)}: '{ms_board.events_mouse(i)}', ({ms_board.events_y(i)}, {ms_board.events_x(i)})")



def updata_ini(file_name: str, data):
    conf = configparser.ConfigParser()
    conf.read(file_name, encoding='utf-8')
    for i in data:
        conf.set(i[0], i[1], str(i[2]))
    conf.write(open(file_name, "w", encoding='utf-8'))

def main():
    # # 测试枚举法判雷速度算例
    # time1 = time.time()
    # BoardofGame = [[10]*12, [10]+[1]*10+[10], [10]+[1]+[0]*8+[1]+[10], [10]+[1]+[0]*8+[1]+[10], [10]+[1]+[0]*8+[1]+[10], \
    #                [10]+[1]+[0]*8+[1]+[10], [10]+[1]+[0]*8+[1]+[10], [10]+[1]+[0]*8+[1]+[10], [10]+[1]+[0]*8+[1]+[10], \
    #                [10]+[1]+[0]*8+[1]+[10], [10]+[1]+[0]*8+[1]+[10], [10]+[1]+[0]*8+[1]+[10], [10]+[1]+[0]*8+[1]+[10], \
    #                [10]+[1]+[0]*8+[1]+[10], [10]+[1]+[0]*8+[1]+[10], [10]+[1]+[0]*8+[1]+[10], [10]+[1]+[0]*8+[1]+[10], \
    #                [10]+[1]+[0]*8+[1]+[10], [10]+[1]+[0]*8+[1]+[10], [10]+[1]+[0]*8+[1]+[10], [10]+[1]+[0]*8+[1]+[10], \
    #                [10]+[1]+[0]*8+[1]+[10], [10]+[1]*10+[10], [10]*12]
    # MatrixA, Matrixx, Matrixb = refreshMatrix(BoardofGame)
    # BoardofGame, NotMine, flag = SolveEnumerate(MatrixA, Matrixx, Matrixb, BoardofGame, 100)
    # print(NotMine)
    # time2 = time.time()
    # print(time2 - time1)


    # # 测试埋雷+计算3BV速度算例
    # time1 = time.time()
    # for i in range(100000):
    #     layMine(16, 30, 99, 1, 1, Min3BV=0, Max3BV=1000000, MaxTimes=1000000)
    # time2 = time.time()
    # print(time2 - time1)

    # # 测试  速度算例
    # time1 = time.time()
    # for i in range(10000):
    #     layMineOp(16, 30, 99, 1, 1)
    # time2 = time.time()
    # print(time2 - time1)

    # 测试生成无猜局面速度算例
    # num = 0
    # T = 500
    # time1 = time.time()
    # for i in range(T):
    #     (bb, Parameters) = ms.laymine_solvable_thread(16, 30, 99, 10, 10, 1000000)
    #     num += Parameters[2]
    # time2 = time.time()
    # print(time2 - time1)
    # print(num/T)




    # import minepy
    # import numpy as np
    # for ii in range(10):
    #     a = layMine(16, 30, 99, 1, 1, Min3BV=0, Max3BV=1e6, MaxTimes=1e6)[0]
    #     x = []
    #     y = []
    #     for i in range(16):
    #         for j in range(30):
    #             if a[i][j] == -1:
    #                 x.append(i)
    #                 y.append(j)
    #     mine = minepy.MINE(alpha=0.6, c=15, est="mic_approx")
    #     mine.compute_score(x, y)
    #     print(mine.mic())
    
    a = laymine_solvable(0, 10, 100000, (8, 8, 10, 0, 0, 100000))
    print(a)


if __name__ == '__main__':
    
    main()






