# author : Wang Jianing(18201)
from random import shuffle, choice
# from random import randint, seed, sample
# from itertools import combinations
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

# def SolveDirect(MatrixA, Matrixx, Matrixb, BoardofGame):
#     # 考虑只一个方程判雷，比如3个方格，雷数也是正好是3，等等
#     # 返回MatrixA, Matrixx, Matrixb, BoardofGame, NotMine, flag
#     # flag=1表明有所动作，比如标雷或发现NotMine
#     # NotMine存储非雷的位置
#     # 注意：处理结束后的矩阵可能有重复的行(?)
#     flag = 0
#     NotMine = []
#     MatrixColumn = len(Matrixx)
#     MatrixRow = len(Matrixb)
#     for i in range(MatrixRow-1, -1, -1):#第一轮循环，找是雷的位置
#         if sum(MatrixA[i][:]) == Matrixb[i]:
#             flag = 1
#             for k in range(MatrixColumn-1, -1, -1):
#                 if MatrixA[i][k] == 1:
#                     m,n = Matrixx[k]
#                     BoardofGame[m][n] = 11#在游戏局面中标雷
#                     Matrixx.pop(k)
#                     for t in range(0,MatrixRow):
#                         if MatrixA[t][k] == 0:
#                             MatrixA[t].pop(k)
#                         else:
#                             MatrixA[t].pop(k)
#                             Matrixb[t] -= 1
#                     MatrixColumn -= 1
#             MatrixA.pop(i)
#             Matrixb.pop(i)
#             MatrixRow -= 1
#     for i in range(MatrixRow-1, -1, -1):# 第二轮循环，找不是雷的位置
#         if Matrixb[i]==0:
#             flag = 1
#             for k in range(MatrixColumn-1, -1, -1):
#                 if MatrixA[i][k] == 1 and Matrixx[k] not in NotMine:
#                     NotMine.append(Matrixx[k])

#     return BoardofGame, NotMine, flag

# SolveMinus = ms_toollib.py_SolveMinus
# SolveMinus(MatrixA, Matrixx, Matrixb, BoardofGame)
# 用减法和集合的包含关系判雷
# 返回BoardofGame, NotMine, flag
# 如果发现IsMine而没有发现NotMine，会再用单集合找一遍。如果发现NotMine，则不调用方法1
# 因此，若方法2没有发现NotMine，则方法1也不可能发现NotMine；
# 若方法2发现NotMine，则方法1还可能发现NotMine
# 注意：处理结束后的矩阵可能有重复的行

# SolveEnumerate = ms_toollib.py_SolveEnumerate
# SolveEnumerate(MatrixA, Matrixx, Matrixb, BoardofGame, enuLimit=30)
#枚举法判雷

# calPossibility = ms_toollib.py_cal_possibility

# calPossibility_onboard = ms_toollib.py_cal_possibility_onboard

def refreshMatrixWithNotMine(MatrixA,Matrixx,Matrixb,NotMine):
    # 用非雷刷新三个矩阵，同时删掉全为0的行
    # 拟弃用。不合理。
    # MatrixA,Matrixx,Matrixb = refreshMatrixWithNotMine(MatrixA,Matrixx,Matrixb,NotMine)
    MatrixRow = len(Matrixb)
    # MatrixColumn = len(Matrixx)
    NotMineRel = []
    for j in NotMine:
        NotMineRel.append(Matrixx.index(j))
    NotMineRel.sort(reverse=True)
    for m in NotMineRel:
        Matrixx.pop(m)
    for i in range(MatrixRow-1, -1, -1):
        if sum(MatrixA[i][:]) == 0:
            MatrixA.pop(i)
            Matrixb.pop(i)
            continue
        for m in NotMineRel:
            MatrixA[i].pop(m)

    return MatrixA, Matrixx, Matrixb

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


def enumerateChangeBoard(board, BoardofGame, xx, yy):
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
        return board, False
    
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
                print('%3.d'%j, end=', ')
            print()
    elif mode == 1:
        for i in arr:
            for j in i:
                print('%3.d'%j.num, end=', ')
            print()
    elif mode == 2:
        for i in arr:
            for j in i:
                print('%3.d'%j.status, end=', ')
            print()

def debug_ms_board(ms_board):
    for i in range(ms_board.events_len):
        print(f"{ms_board.events_time(i)}: '{ms_board.events_mouse(i)}', ({ms_board.events_y(i)}, {ms_board.events_x(i)})")



# layMineSolvable = ms_toollib.layMineSolvable
# layMineSolvable = ms_toollib.py_layMineSolvable_thread
# layMineSolvable(Row, Column, MineNum, X0, Y0, Min3BV = 0, Max3BV = 1e6,
#                 MaxTimes = 1e6, enuLimit = 30)
# 3BV下限、上限，最大尝试次数，返回是否成功。
# 若不成功返回最后生成的局面（不一定无猜），默认尝试十万次
# 工具箱里的这两个函数，一个是单线程，一个是多线程
# 性能对比：(16, 16, 72) -> 10.49, 32.02
# (16, 30, 99) -> 2.98, 2.66
# layMineSolvable = debug_laymine


# calOp = ms_toollib.py_calOp # 输入列表的局面，计算空，0的8连通域数
# calOp(Board)

# cal3BV = ms_toollib.py_cal3BV
# 计算3BV，接受列表
# def cal3BV(Board):

# def isJudgeable(BoardofGame, EnuLimit=30):
#     # 返回此时是否存在可判的格子，如果还能判返回True
#     # 这个过程中，如果AI见到的游戏局面中有未标的雷，会标雷，但仍然可能有漏标的
#     # flag = 0
#     MatrixA, Matrixx, Matrixb = refreshMatrix(BoardofGame)
#     BoardofGame, NotMine, flag = SolveDirect(MatrixA, Matrixx, Matrixb, BoardofGame)
#     if not NotMine:
#         MatrixA, Matrixx, Matrixb = refreshMatrix(BoardofGame)
#         BoardofGame, NotMine, flag = SolveMinus(MatrixA, Matrixx, Matrixb, BoardofGame)
#         if not NotMine:
#             Matrix_as, Matrix_xs, Matrix_bs, _ = refresh_matrixs(BoardofGame)
#             BoardofGame, NotMine, flag = SolveEnumerate(Matrix_as, Matrix_xs, Matrix_bs, BoardofGame, EnuLimit)
#             if not NotMine:
#                 return BoardofGame, False
#     return BoardofGame, True

# def xyisJudgeable(BoardofGame, x, y, EnuLimit=30):
#     # (x,y)是否必然安全，如果必然安全，返回True
#     MatrixA, Matrixx, Matrixb = refreshMatrix(BoardofGame)

#     if (x,y) not in Matrixx:  # 内部的非雷按理无法判出
#         return False

#     BoardofGame, NotMine, flag = SolveDirect(MatrixA, Matrixx, Matrixb, BoardofGame)
#     if (x,y) not in NotMine:
#         MatrixA, Matrixx, Matrixb = refreshMatrix(BoardofGame)
#         BoardofGame, NotMine, flag = SolveMinus(MatrixA, Matrixx, Matrixb, BoardofGame)
#         if (x,y) not in NotMine:
#             Matrix_as, Matrix_xs, Matrix_bs, _, _ = refresh_matrixs(BoardofGame)  # result of refresh_matrixs has len of 5
#             BoardofGame, NotMine, flag = SolveEnumerate(Matrix_as, Matrix_xs, Matrix_bs, BoardofGame, EnuLimit)
#             if (x,y) not in NotMine:
#                 return False
#     return True

def calBoardIndex(Board):
    # 拟弃用
    # 原则上计算局面中所有指标，包括以后新发明的指标
    # 3BV, Ops, Isls
    # 以后会加各个数字出现次数等等
    # 返回字典
    indexes = {}
    # Row = len(Board)
    # Column = len(Board[0])
    indexes['Ops'] = ms.cal_op(Board)
    indexes['3BV'] = ms.cal3BV(Board)
    indexes['Isls'] = '还在写'
    return indexes

def calScores(mode, rtime, operationStream, MinesweeperBoard, Difficulty):
    # 拟弃用
    # 计算游戏得分，展示用，返回一个字典，都是字符串
    # MinesweeperBoard是整局游戏的包装类，属性比较多
    # print('----------------')
    # print(operationStream)
    # print2(Board)
    winflag = True if MinesweeperBoard.game_board_state == 3 else False
    Board = MinesweeperBoard.board
    rtime = max(rtime, 1e-4)
    Row = len(Board)
    Column = len(Board[0])
    s = Row * Column
    scores = {}
    indexes = calBoardIndex(Board)
    BBBV = indexes['3BV']
    msBoard = ms.MinesweeperBoard(Board)
    msBoard.step_flow(operationStream)
    scores['RTime'] = '{:.3f}'.format(rtime)
    scores['3BV'] = str(msBoard.solved3BV) + '/' + str(BBBV)
    scores['EstTime'] = '{:.3f}'.format(rtime) if winflag else '{:.3f}'.format(min(999, rtime*BBBV/max(msBoard.solved3BV, 0.001)))
    scores['Ops'] = str(indexes['Ops'])
    scores['Isls'] = str(indexes['Isls'])
    scores['Left'] = str(msBoard.left) + '@' + ('--' if rtime < 1e-3 else '{:.3f}'.format(msBoard.left/(rtime)))
    scores['Right'] = str(msBoard.right) + '@' + ('--' if rtime < 1e-3 else '{:.3f}'.format(msBoard.right/rtime))
    scores['Double'] = str(msBoard.chording)
    clNum = msBoard.left + msBoard.right + msBoard.chording
    scores['Cl'] = str(clNum) + '@' + ('--' if rtime < 1e-3 else '{:.3f}'.format(clNum/rtime))
    IOE = msBoard.solved3BV/clNum
    scores['IOE'] = '{:.3f}'.format(IOE)
    scores['Thrp'] = '{:.3f}'.format(msBoard.solved3BV/msBoard.ces)
    scores['Corr'] = '{:.3f}'.format(msBoard.ces/(msBoard.left + msBoard.right + msBoard.chording))
    BBBV_s = min(100, msBoard.solved3BV/rtime)
    scores['3BV/s'] = '{:.3f}'.format(BBBV_s)
    RQP = rtime**2/BBBV
    scores['RQP'] = '{:.3f}'.format(RQP) if winflag else '--'
    if Difficulty == 1:
        STNB = 47.22/(rtime**1.7/BBBV)*(msBoard.solved3BV/BBBV)
    elif Difficulty == 2:
        STNB = 153.73/(rtime**1.7/BBBV)*(msBoard.solved3BV/BBBV)
    elif Difficulty == 3:
        STNB = 435.001/(rtime**1.7/BBBV)*(msBoard.solved3BV/BBBV)
    else:
        STNB = 0
    STNB = min(STNB, 1000)
    scores['STNB'] = '{:.3f}'.format(STNB)
    scores['STNB'] = '{:.3f}'.format((0.0016*s*s+0.1020*s+24.8904)/(rtime**1.7/BBBV)*(msBoard.solved3BV/BBBV)**1.7)
    Ce_s = min(20, msBoard.ces/rtime)
    scores['Ce/s'] = '{:.3f}'.format(Ce_s)
    scores['Ces'] = str(msBoard.ces) + '@' + '{:.3f}'.format(Ce_s)
    if mode == 0:
        scores['Mode'] = '标准'
    elif mode == 1:
        scores['Mode'] = 'win7'
    elif mode == 2:
        scores['Mode'] = '竞速无猜'
    elif mode == 3:
        scores['Mode'] = '强无猜'
    elif mode == 4:
        scores['Mode'] = '弱无猜'
    elif mode == 5:
        scores['Mode'] = '准无猜'
    elif mode == 6:
        scores['Mode'] = '强可猜'
    elif mode == 7:
        scores['Mode'] = '弱可猜'
    if Difficulty == 1:
        scores['Difficulty'] = '初级'
        scoresValue = []
        scoresValue.append(1 if Ce_s > 7.1 else -0.0005*Ce_s**3-0.0061*Ce_s*Ce_s+0.2065*Ce_s)
        scoresValue.append(math.atan(BBBV_s*0.7)*0.63661977)
        Time = rtime if winflag else 999
        scoresValue.append(math.atan(10/Time)*0.63661977)
        scoresValue.append(math.atan(STNB/50)*0.63661977)
        scoresValue.append(0.0209*IOE**3-0.2311*IOE*IOE+0.8374*IOE-0.0049)
        scoresValue.append(math.atan(10/RQP)*0.63661977)
    elif Difficulty == 2:
        scores['Difficulty'] = '中级'
        scoresValue = []
        scoresValue.append(1 if Ce_s > 7.1 else -0.0005*Ce_s**3-0.0061*Ce_s*Ce_s+0.2065*Ce_s)
        scoresValue.append(math.atan(BBBV_s*1.1)*0.63661977)
        Time = rtime if winflag else 999
        scoresValue.append(math.atan(150/Time)*0.63661977)
        scoresValue.append(math.atan(STNB/25)*0.63661977)
        scoresValue.append((0.1097*IOE**3+0.3169*IOE*IOE-0.01307*IOE+0.0005845)/(IOE*IOE-1.342*IOE+0.899))
        scoresValue.append(math.atan(30/RQP)*0.63661977)
    elif Difficulty == 3:
        scores['Difficulty'] = '高级'
        scoresValue = []
        scoresValue.append(1 if Ce_s > 7.1 else -0.0005*Ce_s**3-0.0061*Ce_s*Ce_s+0.2065*Ce_s)
        scoresValue.append(math.atan(BBBV_s*1.2)*0.63661977)
        Time = rtime if winflag else 999
        scoresValue.append(math.atan(300/Time)*0.63661977)
        scoresValue.append(math.atan(STNB/20)*0.63661977)
        scoresValue.append((0.1097*IOE**3+0.3169*IOE*IOE-0.01307*IOE+0.0005845)/(IOE*IOE-1.342*IOE+0.899))
        scoresValue.append(math.atan(50/RQP)*0.63661977)
    elif Difficulty == 4:
        scores['Difficulty'] = '自定义'
        scoresValue = []
        scoresValue.append(1 if Ce_s > 7.1 else -0.0005*Ce_s**3-0.0061*Ce_s*Ce_s+0.2065*Ce_s)
        scoresValue.append(math.atan(BBBV_s*1.2)*0.63661977)
        Time = rtime if winflag else 999
        scoresValue.append(math.atan(300/Time)*0.63661977)
        scoresValue.append(math.atan(STNB/20)*0.63661977)
        scoresValue.append((0.1097*IOE**3+0.3169*IOE*IOE-0.01307*IOE+0.0005845)/(IOE*IOE-1.342*IOE+0.899))
        scoresValue.append(math.atan(50/RQP)*0.63661977)
    # print(scoresValue)
    return scores, scoresValue, msBoard


def updata_ini(file_name: str, data):
    conf = configparser.ConfigParser()
    conf.read(file_name)
    for i in data:
        conf.set(i[0], i[1], str(i[2]))
    conf.write(open(file_name, "w"))

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






