# author : Wang JiaNing(18201)
from random import randint, seed
from itertools import combinations

OutputEnable = 0
EnuLimit = 30    #枚举极限
  

def LayMine(Row , Column , MineNum , X0 , Y0):
    #布雷，参数依次是行、列、雷数、起手位置的第几行-1、第几列-1
    #起手不开空，必不为雷
    #返回二维列表，0~8代表数字，-1代表雷
    area = Row*Column-1
    if MineNum < area/2:
        Board1Dim = [0]*(area-MineNum)
        Board1Dim = Board1Dim+[-1]*MineNum
        for i in range(area-MineNum,area):
            idd=randint(0,i-1)
            if Board1Dim[idd]!=-1:
                Board1Dim[idd]=-1
                Board1Dim[i]=0
    else:
        Board1Dim = [-1]*MineNum
        Board1Dim = Board1Dim+[0]*(area-MineNum)
        for i in range(MineNum,area):
            idd=randint(0,i-1)
            if Board1Dim[idd] != 0:
                Board1Dim[idd] = 0
                Board1Dim[i] = -1
    #插入起手位置
    Board1Dim.insert(X0+Y0*Row , 0)
    #1维转2维同时算数字
    Board=[[0]*Column for _ in range(Row)]
    for i in range(0,area):
        if Board1Dim[i] < 0:
            x = i % Row
            y = i // Row
            Board[ x ][ y ] = -1
            for j in range(max(0 , x-1), min(Row , x+2)):
                for k in range(max(0 , y-1), min(Column , y+2)):
                    if Board[ j ][ k ]>=0:
                        Board[ j ][ k ] += 1
    return Board

def layMineOp(Row , Column , MineNum , X0 , Y0):
    #布雷，参数依次是行、列、雷数、起手位置的第几行-1、第几列-1
    #起手必开空，不校验雷数是否超过空格数
    #返回二维列表，0~8代表数字，-1代表雷
    if X0 == 0 or Y0 == 0 or X0 == Row-1 or Y0 == Column-1:
        if X0 == 0 and Y0 == 0 or X0 == 0 and Y0 == Column-1 or X0 == Row-1 and Y0 == 0 or X0 == Row-1 and Y0 == Column-1:
            areaOp = 4
        else:
            areaOp = 6
    else:
        areaOp = 9
    area = Row*Column-areaOp
    if MineNum < area/2:
        Board1Dim = [0]*(area-MineNum)
        Board1Dim = Board1Dim+[-1]*MineNum
        for i in range(area-MineNum,area):
            idd=randint(0,i-1)
            if Board1Dim[idd]!=-1:
                Board1Dim[idd]=-1
                Board1Dim[i]=0
    else:
        Board1Dim = [-1]*MineNum
        Board1Dim = Board1Dim+[0]*(area-MineNum)
        for i in range(MineNum,area):
            idd=randint(0,i-1)
            if Board1Dim[idd] != 0:
                Board1Dim[idd] = 0
                Board1Dim[i] = -1
    #1维转2维同时算数字
    Board=[[0]*Column for _ in range(Row)]
    i = 0
    while i < area + areaOp:
        x = i % Row
        y = i // Row
        if abs(x-X0)<=1 and abs(y-Y0)<=1:
            Board1Dim.insert(i,0)
        if Board1Dim[i] < 0:
            Board[ x ][ y ] = -1
        i += 1
    for x in range(0,Row):
        for y in range(0,Column):
            for j in range(max(0 , x-1), min(Row , x+2)):
                for k in range(max(0 , y-1), min(Column , y+2)):
                    if Board[ j ][ k ]<0 and Board[ x ][ y ]>=0:
                        Board[ x ][ y ] += 1
    return Board

def addedCellId(Board , BoardofGame , ClickedPos):
    #局面，游戏局面，点击位置，可以同时点多个位置
    #返回在ClickedPos进行左击后，局面中更新的数字的坐标，包括ClickedPos本身
    #ClickedPos一定不能是雷,也不能是空,是序列格式
    #这段写得效率不高，有冗余
    ExpandPos=[]
    for pos in ClickedPos:
        BoardofGame,ExpandPos2 = addedCellIdOneStep(Board , BoardofGame , pos)
        ExpandPos=ExpandPos+ExpandPos2
    return BoardofGame , ExpandPos

def addedCellIdOneStep(Board , BoardofGame , ClickedPos):
    #递归的拓展算法
    #ClickedPos一定不能是雷,也不能是空,是元组格式
    ExpandPos=[]
    Row=len(Board)
    Column=len(Board[0])
    i,j=ClickedPos
    if Board[i][j] > 0:
        BoardofGame[i][j]=Board[i][j]
        return BoardofGame , [ClickedPos]
    if Board[i][j] == 0:
        BoardofGame[i][j]=Board[i][j]
        for m in range(max(0 , i-1), min(Row , i+2)):
            for n in range(max(0 , j-1), min(Column , j+2)):
                if (i!=m or j!=n) and BoardofGame[m][n] == 10:
                    BoardofGame[m][n]=Board[m][n]
                    BoardofGame , ExpandPos2 = addedCellIdOneStep(Board , BoardofGame , (m,n))
                    ExpandPos=ExpandPos+ExpandPos2
    return BoardofGame , ExpandPos


def find(List,x):
    for i,item in enumerate(List):
        if item==x:
            return 1,i
    return 0,0


def calMatrix(AddedCell , BoardofGame , MatrixA , Matrixx , Matrixb):
    #函数用途：根据AddedCell维护MatrixA , Matrixx , Matrixb
    #MatrixA , Matrixx , Matrixb
    #系数矩阵为二维列表，x向量为元组列表，b向量为一维列表
    #BoardMatrix为二维列表，记录局面中某个位置的方程在矩阵中的列索引，-1为不在矩阵中
    #返回维护后的MatrixA , Matrixx , Matrixb
    Row=len(BoardofGame)
    Column=len(BoardofGame[0])
    MatrixColumn=len(Matrixx)
    MatrixRow=len(Matrixb)
    for i,j in AddedCell:
        if MatrixColumn == 0:
            MatrixA.append([])
        else:
            MatrixA = MatrixA + [[0]*MatrixColumn]
        MatrixRow += 1
        FlagedNum = 0#在周围已经标出的雷
        FlagNeed = 0  #周围有不确定的格
        for m in range(max(0 , i-1), min(Row , i+2)):
            for n in range(max(0 , j-1), min(Column , j+2)):
                if (i!=m or j!=n) and BoardofGame[m][n] == 10:
                    Flag,Id = find(Matrixx , (m,n))
                    FlagNeed = 1
                    if Flag:
                        MatrixA[MatrixRow-1][Id] = 1
                    else:
                        for z in range(0,MatrixRow-1):
                            MatrixA[z].append(0)
                        MatrixA[MatrixRow-1].append(1)
                        Matrixx.append((m,n))
                        MatrixColumn += 1
                if BoardofGame[m][n] == 11:
                    FlagedNum += 1
        if FlagNeed:
            Matrixb.append(BoardofGame[i][j]-FlagedNum)
        else:
            MatrixA.pop()
            MatrixRow -= 1
    return MatrixA , Matrixx , Matrixb


def SolveDirect(MatrixA , Matrixx , Matrixb , BoardofGame):
    #考虑只一个方程判雷，比如3个方格，雷数也是正好是3，等等
    #返回MatrixA , Matrixx , Matrixb , BoardofGame
    #NotMine存储非雷的位置
    #注意：处理结束后的矩阵可能有重复的行
    NotMine = []
    MatrixColumn = len(Matrixx)
    MatrixRow = len(Matrixb)
    while 1:    #重复执行，直到彻底判完。可能有更加巧妙的算法，有待后期优化
        FlagFinish = 1
        for i in range(MatrixRow-1 , -1 , -1):#第一轮循环，找是雷的位置
            BlockNum = 0
            for k in range(0 , MatrixColumn):
                if MatrixA[i][k] == 1:
                    BlockNum += 1
            if BlockNum == Matrixb[i]:
                FlagFinish = 0
                for k in range(MatrixColumn-1 , -1 , -1):
                    if MatrixA[i][k] == 1:
                        m,n = Matrixx[k]
                        BoardofGame[m][n] = 11#在游戏局面中标雷
                        Matrixx.pop(k)
                        for t in range(0,MatrixRow):
                            if MatrixA[t][k] == 0:
                                MatrixA[t].pop(k)
                            else:
                                MatrixA[t].pop(k)
                                Matrixb[t] -= 1
                        MatrixColumn -= 1
                MatrixA.pop(i)
                Matrixb.pop(i)
                MatrixRow -= 1
        for i in range(MatrixRow-1 , -1 , -1):#第二轮循环，找不是雷的位置,倒着找边找边删
            if Matrixb[i]==0:
                FlagFinish = 0
                for k in range(MatrixColumn-1 , -1 , -1):
                    if MatrixA[i][k] == 1:
                        NotMine.append(Matrixx[k])
                        Matrixx.pop(k)
                        for t in range(MatrixRow-1 , -1 , -1):
                            MatrixA[t].pop(k)
                        MatrixColumn -= 1
                MatrixA.pop(i)
                Matrixb.pop(i)
                MatrixRow -= 1
        if FlagFinish:
            break
    return MatrixA , Matrixx , Matrixb , BoardofGame , NotMine
    
    
def SolveMinus(MatrixA , Matrixx , Matrixb , BoardofGame):
    #用减法和集合的包含关系判雷
    #注意：处理结束后的矩阵可能有重复的行
    NotMine = []
    NotMineRel = []
    IsMineRel = []  #先找到是雷和非雷的ID，最后才处理
    MatrixColumn = len(Matrixx)
    MatrixRow = len(Matrixb)
    if MatrixRow<=1:
        return MatrixA , Matrixx , Matrixb , BoardofGame , NotMine
    for i in range(MatrixRow-1 , -2 , -1):
        for j in range(i-1 , -1 , -1):
            ADval1=[]  #记录相减后为1和-1的列索引
            ADvaln1=[]
            FlagAdj = 0 #两个方程是否相邻的标志
            for k in range(0 , MatrixColumn): #开始相减
                if MatrixA[i][k] and MatrixA[j][k]:
                    FlagAdj=1
                    continue
                if MatrixA[i][k] - MatrixA[j][k] == 1:
                    ADval1.append(k)
                elif MatrixA[i][k] - MatrixA[j][k] == -1:
                    ADvaln1.append(k)
            if FlagAdj:
                bDval = Matrixb[i] - Matrixb[j]
                if len(ADval1) == bDval:  #减法过后，剩余格数等于剩余雷数
                    IsMineRel = IsMineRel + ADval1
                    NotMineRel = NotMineRel + ADvaln1
                elif len(ADvaln1) == -bDval:
                    IsMineRel = IsMineRel + ADvaln1
                    NotMineRel = NotMineRel + ADval1 #此时集合中有重复的元素
    IsMineRel = list(set(IsMineRel))
    NotMineRel = list(set(NotMineRel))#去除重复的元素
    NAndIMineRel=IsMineRel[:]+NotMineRel[:]
    NAndIMineRel.sort(reverse = True)
    for i in range(0,len(NotMineRel)):
        NotMine.append(Matrixx[NotMineRel[i]])#相对索引改成绝对索引  
    #双集合判雷完成后必须用单集合再搜索一下有没有不是雷的
    #否则有些方程会在接下类被误删除
    #双集合判完由于新标出了一些雷，此时用单集合还能再判出一些
    for i in range(MatrixRow-1 , -1 , -1):
        if Matrixb[i]==0:
            FlagFinish = 0
            for k in range(MatrixColumn-1 , -1 , -1):
                if MatrixA[i][k] == 1:
                    NotMine.append(Matrixx[k])
                    Matrixx.pop(k)
                    for t in range(MatrixRow-1 , -1 , -1):
                        MatrixA[t].pop(k)
                    MatrixColumn -= 1
            MatrixA.pop(i)
            Matrixb.pop(i)
            MatrixRow -= 1
    
    
    
    
    #完成双集合判雷，开始处理
    for i in range(MatrixRow-1 , -1 , -1):
        for j in NAndIMineRel:
            if MatrixA[i][j] and j in IsMineRel:
                Matrixb[i] -= 1
            MatrixA[i].pop(j)
        if Matrixb[i] == 0:
            MatrixA.pop(i)
            Matrixb.pop(i)
            MatrixRow -= 1
    for i in NAndIMineRel:
        m,n = Matrixx[i]
        if i in IsMineRel:
            BoardofGame[m][n] = 11
        Matrixx.pop(i)
    return MatrixA , Matrixx , Matrixb , BoardofGame , NotMine

def SolveEnumerate(MatrixA , Matrixx , Matrixb , BoardofGame):
    #枚举法判雷
    NotMine = []
    NotMineRel = []
    IsMineRel = []
    MatrixColumn = len(Matrixx)
    MatrixRow = len(Matrixb)
    #第一步，删去重复的行
    for i in range(MatrixRow-1 , -2 , -1):
        for j in range(i-1 , -1 , -1):
            if MatrixA[i] == MatrixA[j]:
                MatrixA.pop(i)
                Matrixb.pop(i)
                break
    MatrixRow = len(Matrixb)
    #第二步，整理成分块矩阵
    ColId = list(range(0,MatrixColumn))
    RowId = list(range(0,MatrixRow))
    GroupCol = []  #单个组的临时索引
    GroupRow = []
    Groupb = []
    Groupx = []
    TempCol = []
    TempRow = []
    while ColId:#结束条件
        TempCol.append(ColId.pop())
        while TempCol or TempRow:
            if TempCol:
                for i in range(0,MatrixRow):
                    if MatrixA[i][TempCol[-1]] == 1:
                        if i in RowId:
                            TempRow.append(i)
                            RowId.remove(i)
                temp = TempCol.pop()
                GroupCol.append(temp)
                Groupx.append(Matrixx[temp])
            if TempRow:
                for j in range(0,MatrixColumn):
                    if MatrixA[TempRow[-1]][j] == 1:
                        if j in ColId:
                            TempCol.append(j)
                            ColId.remove(j)
                temp = TempRow.pop()
                GroupRow.append(temp)
                Groupb.append(Matrixb[temp])
        
        AllTable = [[2]*len(GroupCol)]
        for i in GroupRow:
            b = Matrixb[i]
            TableId = []
            for j in GroupCol:
                if MatrixA[i][j] == 1:
                    TableId.append(GroupCol.index(j))
            AllTable = enuOneStep(AllTable , TableId , b)
        if len(GroupCol) >= EnuLimit:#枚举法的极限
            return MatrixA , Matrixx , Matrixb , BoardofGame , []
        for j in range(1,len(GroupCol)):
            if AllTable[0][j] == 0:
                NotMineRel.append(GroupCol[j])
                for i in range(1,len(AllTable)):
                    if AllTable[i][j] == 1:
                        NotMineRel.pop()
                        break
            else:
                IsMineRel.append(GroupCol[j])
                for i in range(1,len(AllTable)):
                    if AllTable[i][j] == 0:
                        IsMineRel.pop()
                        break
            
    IsMineRel = list(set(IsMineRel))
    NotMineRel = list(set(NotMineRel))#去除重复的元素
    NAndIMineRel=IsMineRel+NotMineRel
    NAndIMineRel.sort(reverse = True)
    for i in range(0,len(NotMineRel)):
        NotMine.append(Matrixx[NotMineRel[i]])#相对索引改成绝对索引  
    #完成减法判雷，开始处理
    for i in range(MatrixRow-1 , -1 , -1):
        for j in NAndIMineRel:
            if MatrixA[i][j] and j in IsMineRel:
                Matrixb[i] -= 1
            MatrixA[i].pop(j)
        if Matrixb[i] == 0:
            MatrixA.pop(i)
            Matrixb.pop(i)
            MatrixRow -= 1
    for i in NAndIMineRel:
        m,n = Matrixx[i]
        if i in IsMineRel:
            BoardofGame[m][n] = 11
        Matrixx.pop(i)
           
    return MatrixA , Matrixx , Matrixb , BoardofGame , NotMine   

def enuOneStep(AllTable , TableId , b):
    #AllTable中，0表示非雷，1表示雷，2表示暂未枚举
    #TableId保存了AllTable的索引，AllTable的列和GroupCol的列一致
    #b表示TableId指向的位置中有几个雷
    NewId = []
    for i in TableId:
        if AllTable[0][i] == 2:
            NewId.append(i)
    DelId = []
    for i in range(0,len(AllTable)):
        ExtraMine = b
        for j in TableId:
            if AllTable[i][j] == 1:
                ExtraMine -= 1
        if ExtraMine < 0 or ExtraMine > len(NewId):
            #当前方案的雷数超过方程的限制，则删除该方案
            #当前方案的雷数超过方格数，也要删除该方案
            DelId.append(i)
            continue
        AddedTable = enumerateSub(len(NewId) , ExtraMine)
        #给当前表格增加方案
        for t in range(0,len(NewId)):
            AllTable[i][NewId[t]] = AddedTable[0][t]
        for m in range(1,len(AddedTable)):
            AllTable.append(AllTable[i][:])
            for t in range(0,len(NewId)):
                AllTable[-1][NewId[t]] = AddedTable[m][t]
    
    DelId.sort(reverse=True)
    for i in DelId:
        AllTable.pop(i)
    return AllTable
        
    
    
    

def Victory(BoardofGame,Board):
    #判断当前是否获胜
    #游戏局面中必须没有标错的雷
    #这个函数不具备普遍意义
    Row = len(BoardofGame)
    Col = len(BoardofGame[0])
    for i in range(0,Row):
        for j in range(0,Col):
            if BoardofGame[i][j] == 10 and Board[i][j] != -1:
                return 0
    return 1

def enumerateSub(Col , MineNum):
    #返回长度为Col，其中含有MineNum个1的所有01序列，形状为[[][][][]]
    Out=[]
    List=range(0,Col)
    for i in combinations(List, MineNum):
        Out.append([0]*Col)
        for j in range(0,MineNum):
            Out[-1][i[j]]=1
    return Out

def isSolvable(Board , X0 , Y0):
    #从指定位置开始扫，判断局面是否无猜
    #周围一圈都是雷，那么中间是雷不算猜，中间不是雷算猜
    if unsolvableStructure(Board):#若包含不可判雷结构，则不是无猜
        return 0
    BoardofGame = [[10]*len(Board[0]) for _ in range(len(Board))]
    #10是未打开，11是标雷
    #局面大小必须超过6*6
    MatrixA = []
    Matrixx = []
    Matrixb = []
    BoardofGame , AddedCell = addedCellId(Board , BoardofGame , [(X0,Y0)] )
    MatrixA , Matrixx , Matrixb = calMatrix(AddedCell , BoardofGame , MatrixA , Matrixx , Matrixb)
    if Victory(BoardofGame,Board):
        return 1
    while 1:
        MatrixA , Matrixx , Matrixb , BoardofGame , NotMine = SolveDirect(MatrixA , Matrixx , Matrixb , BoardofGame)       
        if not NotMine:
            MatrixA , Matrixx , Matrixb , BoardofGame , NotMine = SolveMinus(MatrixA , Matrixx , Matrixb , BoardofGame)
            if not NotMine:
                MatrixA , Matrixx , Matrixb , BoardofGame , NotMine = SolveEnumerate(MatrixA , Matrixx , Matrixb , BoardofGame)
                if not NotMine:
                    return 0
        BoardofGame , AddedCell = addedCellId(Board , BoardofGame , NotMine)
        MatrixA , Matrixx , Matrixb = calMatrix(AddedCell , BoardofGame , MatrixA , Matrixx , Matrixb)
        if Victory(BoardofGame,Board):
            return 1

def unsolvableStructure(BoardCheck):
    #检测局面中是否有明显的死猜的结构
    #不考虑起手位置，因为起手必开空
    #局面至少大于4*4
    #返回0或1
    Board = [[0]*len(BoardCheck[0]) for _ in range(len(BoardCheck))]
    Row = len(Board)
    Column = len(Board[0])
    for i in range(0,Row):
        for j in range(0,Column):
            if BoardCheck[i][j] == -1:
                Board[i][j] = -1
    for i in range(0,Row-2):#检查左右两侧
        if i < Row-3:
            if Board[i][0] == -1 and Board[i][1] == -1 and Board[i+3][0] == -1 and Board[i+3][1] == -1 and Board[i+1][0]+Board[i+2][0] == -1 \
            or Board[i][Column-1] == -1 and Board[i][Column-2] == -1 and Board[i+3][Column-1] == -1 and Board[i+3][Column-2] == -1 and Board[i+1][Column-1]+Board[i+2][Column-1] == -1:
                return 1
        if Board[i][2] == -1 and Board[i+1][2] == -1 and Board[i+2][2] == -1 and Board[i+1][0]+Board[i+1][1] == -1 \
        or Board[i][Column-3] == -1 and Board[i+1][Column-3] == -1 and Board[i+2][Column-3] == -1 and Board[i+1][Column-1]+Board[i+1][Column-2] == -1 \
        or Board[i][0] == -1 and Board[i][1] == -1 and Board[i+1][1] == -1 and Board[i+2][1] == -1 and Board[i+2][0] == -1 and Board[i+1][0] == 0 \
        or Board[i][Column-1] == -1 and Board[i][Column-2] == -1 and Board[i+1][Column-2] == -1 and Board[i+2][Column-2] == -1 and Board[i+2][Column-1] == -1 and Board[i+1][Column-1] == 0:
            return 1
        if i < Row-3:
            if Board[i][2] == -1 and Board[i+3][2] == -1 and Board[i+1][0]+Board[i+1][1] == -1 and Board[i+1][1]+Board[i+2][1] == -1 and Board[i+2][1]+Board[i+2][0] == -1 \
            or Board[i][Column-3] == -1 and Board[i+3][Column-3] == -1 and Board[i+1][Column-1]+Board[i+1][Column-2] == -1 and Board[i+1][Column-2]+Board[i+2][Column-2] == -1 and Board[i+2][Column-2]+Board[i+2][Column-1] == -1:
                return 1
            
    for j in range(0,Column-2):#检查上下两侧
        if j < Column-3:
            if Board[0][j] == -1 and Board[1][j] == -1 and Board[0][j+3] == -1 and Board[1][j+3] == -1 and Board[0][j+1]+Board[0][j+2] == -1 \
            or Board[Row-1][j] == -1 and Board[Row-2][j] == -1 and Board[Row-1][j+3] == -1 and Board[Row-2][j+3] == -1 and Board[Row-1][j+1]+Board[Row-1][j+2] == -1:
                return 1
        if Board[2][j] == -1 and Board[2][j+1] == -1 and Board[2][j+2] == -1 and Board[0][j+1]+Board[1][j+1] == -1 \
        or Board[Row-3][j] == -1 and Board[Row-3][j+1] == -1 and Board[Row-3][j+2] == -1 and Board[Row-1][j+1]+Board[Row-2][j+1] == -1 \
        or Board[0][j] == -1 and Board[1][j] == -1 and Board[1][j+1] == -1 and Board[1][j+2] == -1 and Board[0][j+2] == -1 and Board[0][j+1] == 0 \
        or Board[Row-1][j] == -1 and Board[Row-2][j] == -1 and Board[Row-2][j+1] == -1 and Board[Row-2][j+2] == -1 and Board[Row-1][j+2] == -1 and Board[Row-1][j+1] == 0:
            return 1
        if j < Column-3:
            if Board[2][j] == -1 and Board[2][j+3] == -1 and Board[0][j+1]+Board[1][j+1] == -1 and Board[1][j+1]+Board[1][j+2] == -1 and Board[1][j+2]+Board[0][j+2] == -1 \
            or Board[Row-3][j] == -1 and Board[Row-3][j+3] == -1 and Board[Row-1][j+1]+Board[Row-2][j+1] == -1 and Board[Row-2][j+1]+Board[Row-2][j+2] == -1 and Board[Row-2][j+2]+Board[Row-1][j+2] == -1:
                return 1
    if Board[0][2] == -1 and Board[1][2] == -1 and Board[0][0]+Board[0][1] == -1 \
    or Board[2][0] == -1 and Board[2][1] == -1 and Board[0][0]+Board[1][0] == -1 \
    or Board[0][Column-3] == -1 and Board[1][Column-3] == -1 and Board[0][Column-1]+Board[0][Column-2] == -1 \
    or Board[2][Column-1] == -1 and Board[2][Column-2] == -1 and Board[0][Column-1]+Board[1][Column-1] == -1 \
    or Board[Row-1][2] == -1 and Board[Row-2][2] == -1 and Board[Row-1][0]+Board[Row-1][1] == -1 \
    or Board[Row-3][0] == -1 and Board[Row-3][1] == -1 and Board[Row-1][0]+Board[Row-2][0] == -1 \
    or Board[Row-1][Column-3] == -1 and Board[Row-2][Column-3] == -1 and Board[Row-1][Column-1]+Board[Row-1][Column-2] == -1 \
    or Board[Row-3][Column-1] == -1 and Board[Row-3][Column-2] == -1 and Board[Row-1][Column-1]+Board[Row-2][Column-1] == -1 \
    or Board[0][1]+Board[1][1]+Board[1][0] == -3 and Board[0][0] == 0 \
    or Board[0][Column-2]+Board[1][Column-2]+Board[1][Column-1] == -3 and Board[0][Column-1] == 0 \
    or Board[Row-1][Column-2]+Board[Row-2][Column-2]+Board[Row-2][Column-1] == -3 and Board[Row-1][Column-1] == 0 \
    or Board[Row-1][1]+Board[Row-2][1]+Board[Row-2][0] == -3 and Board[Row-1][0] == 0 \
    or Board[2][2] == -1 and Board[0][1]+Board[1][1] == -1 and Board[1][0]+Board[1][1] == -1 \
    or Board[Row-3][2] == -1 and Board[Row-1][1]+Board[Row-2][1] == -1 and Board[Row-2][0]+Board[Row-2][1] == -1 \
    or Board[Row-3][Column-3] == -1 and Board[Row-1][Column-2]+Board[Row-2][Column-2] == -1 and Board[Row-2][Column-1]+Board[Row-2][Column-2] == -1 \
    or Board[2][Column-3] == -1 and Board[0][Column-2]+Board[1][Column-2] == -1 and Board[1][Column-1]+Board[1][Column-2] == -1:#检查四个角
        return 1
    for i in range(0,Row-2):   #找中间的工、回、器形结构
        for j in range(0,Column-2):
            if j < Column-3:
                if Board[i][j] == -1 and Board[i+1][j] == -1 and Board[i+2][j] == -1 and Board[i][j+3] == -1 and Board[i+1][j+3] == -1 and Board[i+2][j+3] == -1 and Board[i+1][j+1]+Board[i+1][j+2] == -1:
                    return 1
            if i < Row-3:
                if Board[i][j] == -1 and Board[i][j+1] == -1 and Board[i][j+2] == -1 and Board[i+3][j] == -1 and Board[i+3][j+1] == -1 and Board[i+3][j+2] == -1 and Board[i+1][j+1]+Board[i+2][j+1] == -1:
                    return 1
            if Board[i][j] == -1 and Board[i+1][j] == -1 and Board[i+2][j] == -1 and Board[i][j+1] == -1 and Board[i+2][j+1] == -1 and Board[i][j+2] == -1 and Board[i+1][j+2] == -1 and Board[i+2][j+2] == -1 and Board[i+1][j+1] == 0:
                return 1
            if j < Column-3 and i < Row-3:
                if Board[i][j] == -1 and Board[i+3][j] == -1 and Board[i][j+3] == -1 and Board[i+3][j+3] == -1 and Board[i+1][j+1]+Board[i+2][j+1] == -1 and Board[i+1][j+1]+Board[i+1][j+2] == -1 and Board[i+2][j+1]+Board[i+2][j+2] == -1:
                    return 1
    return 0

def print2(arr):
    for i in range(len(arr)):      # 控制行，0~2
        for j in range(len(arr[i])):    # 控制列
            print(arr[i][j], end='\t')
        print()

def layMineSolvable(Row , Column , MineNum , X0 , Y0):
    while 1:
        Board = layMineOp(Row , Column , MineNum ,X0, Y0)
        if isSolvable(Board , X0, Y0):
            return Board
    
def main():
    seed(605)
    
    Board=layMineSolvable(16,10,35,0,0)
#    print(isSolvable(Board , 5 , 9))
    # print2(Board)
    
    
#    Board = [[0, 1,-1, 1,0,0],
#             [1, 2, 2, 2,1,0],
#             [-1,2, 3,-1,2,0],
#             [1, 2,-1,-1,2,0],
#             [0, 1, 2, 2,1,0],
#             [0, 0, 0, 0,0,0]]
    # BoardofGame = [[10]*len(Board[0]) for _ in range(len(Board))]
##    #10是未打开，11是标雷
##    #局面大小必须超过6*6
    # MatrixA = []
    # Matrixx = []
    # Matrixb = []
    # X0 = 0
    # Y0 = 0
    # BoardofGame , AddedCell = addedCellId(Board , BoardofGame , [(X0,Y0)] )
    # MatrixA , Matrixx , Matrixb = calMatrix(AddedCell , BoardofGame , MatrixA , Matrixx , Matrixb)
    # MatrixA , Matrixx , Matrixb , BoardofGame , NotMine = SolveEnumerate(MatrixA , Matrixx , Matrixb , BoardofGame)         
#    SolveDirect   SolveEnumerate
#    print(NotMine)
    
    
    
    
if __name__ == '__main__':
    main()










