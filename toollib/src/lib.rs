use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use rand::seq::SliceRandom;
use rand::thread_rng;
// use pyo3::PyTraverseError;
use pyo3::class::basic::PyObjectProtocol;
use std::cmp::max;
use std::cmp::min;
use itertools::Itertools;
use std::sync::{Mutex, Arc};
use std::thread;
// use rayon::prelude::*;
use std::sync::mpsc;


fn refreshMatrix(BoardofGame: &Vec<Vec<i32>>) -> (Vec<Vec<i32>>, Vec<(usize, usize)>, Vec<i32>) {
    // BoardofGame必须且肯定是正确标雷的游戏局面，但不需要标全
    // 根据游戏局面生成矩阵，不分块。生成的是一整个大矩阵，缺点是占用内存较多。
    let Row = BoardofGame.len();
    let Column = BoardofGame[0].len();
    let mut MatrixA: Vec<Vec<i32>> = Vec::new();
    let mut Matrixx: Vec<(usize, usize)> = Vec::new();
    let mut Matrixb: Vec<i32> = Vec::new();
    let mut MatrixARowNum = 0;
    let mut MatrixAColumnNum = 0;

    for i in 0..Row {
        for j in 0..Column {
            if BoardofGame[i][j] > 0 && BoardofGame[i][j] < 10 {
                let mut flag: bool = false;
                for m in max(1, i) - 1..min(Row, i + 2) {
                    for n in max(1, j) - 1..min(Column, j + 2) {
                        if BoardofGame[m][n] == 10 {
                            flag = true;
                        }
                    }
                }
                if flag {
                    MatrixA.push(vec![0; MatrixAColumnNum]);
                    Matrixb.push(BoardofGame[i][j]);
                    MatrixARowNum += 1;
                    for m in max(1, i) - 1..min(Row, i + 2) {
                        for n in max(1, j) - 1..min(Column, j + 2) {
                            if BoardofGame[m][n] == 11 {
                                Matrixb[MatrixARowNum - 1] -= 1
                            } else if BoardofGame[m][n] == 10 {
                                let mut flag_exit: bool = false;
                                for idMatrixx in 0..MatrixAColumnNum {
                                    if Matrixx[idMatrixx].0 == m && Matrixx[idMatrixx].1 == n {
                                        flag_exit = true;
                                        MatrixA[MatrixARowNum - 1][idMatrixx] = 1;
                                    }
                                }
                                if !flag_exit {
                                    for ii in 0..MatrixARowNum {
                                        MatrixA[ii].push(0)
                                    }
                                    Matrixx.push((m, n));
                                    MatrixAColumnNum += 1;
                                    MatrixA[MatrixARowNum - 1][MatrixAColumnNum - 1] = 1;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    (MatrixA, Matrixx, Matrixb)
}

#[pyfunction]
fn py_refreshMatrix(BoardofGame: Vec<Vec<i32>>) -> PyResult<(Vec<Vec<i32>>, Vec<(usize, usize)>, Vec<i32>)> {
    Ok(refreshMatrix(&BoardofGame))
}

fn infectBoard(mut Board: Vec<Vec<i32>>, x: usize, y: usize) -> Vec<Vec<i32>> {
    // Board(x, y)位置的空用数字1填满，计算Op用
    // 接口在模块中不暴露
    let Row = Board.len();
    let Column = Board[0].len();
    for i in max(1, x) - 1..min(Row, x + 2) {
        for j in max(1, y) - 1..min(Column, y + 2) {
            if Board[i][j] == 0 {
                Board[i][j] = 1;
                Board = infectBoard(Board, i, j);
            }
        }
    }
    Board
}

fn calOp(mut Board: Vec<Vec<i32>>) -> usize {
    // 输入局面，计算空，即0的8连通域数
    let Row = Board.len();
    let Column = Board[0].len();
    let mut Op = 0;
    for i in 0..Row {
        for j in 0..Column {
            if Board[i][j] == 0 {
                Board[i][j] = 1;
                Board = infectBoard(Board, i, j);
                Op += 1;
            }
        }
    }
    Op
}

#[pyfunction]
fn py_calOp(mut Board: Vec<Vec<i32>>) -> PyResult<usize> {
    Ok(calOp(Board))
}

fn cal3BVonIsland(Board: &Vec<Vec<i32>>) -> usize {
    // 计算除空以外的3BV
    let Row = Board.len();
    let Column = Board[0].len();
    let mut Num3BVonIsland = 0;
    for i in 0..Row {
        for j in 0..Column {
            if Board[i][j] > 0 {
                let mut flag: bool = true;
                for x in max(1, i) - 1..min(Row, i + 2) {
                    for y in max(1, j) - 1..min(Column, j + 2) {
                        if Board[x][y] == 0 {
                            flag = false;
                        }
                    }
                }
                if flag {
                    Num3BVonIsland += 1;
                }
            }
        }
    }
    Num3BVonIsland
}

fn layMineNumber(Row: usize, Column: usize, MineNum: usize, X0: usize, Y0: usize) -> Vec<Vec<i32>> {
    // 通用标准埋雷引擎
    // 输出为二维的局面
    let mut rng = thread_rng();
    let area: usize = Row * Column - 1;
    let mut Board1Dim: Vec<i32> = vec![];
    Board1Dim.reserve(area);
    Board1Dim = vec![0; area - MineNum];
    Board1Dim.append(&mut vec![-1; MineNum]);
    Board1Dim.shuffle(&mut rng);
    let mut Board1Dim_2: Vec<i32> = vec![];
    Board1Dim_2.reserve(area + 1);
    let pointer = X0 + Y0 * Row;
    for i in 0..pointer {
        Board1Dim_2.push(Board1Dim[i]);
    }
    Board1Dim_2.push(0);
    for i in pointer..area {
        Board1Dim_2.push(Board1Dim[i]);
    }
    let mut Board: Vec<Vec<i32>> = vec![vec![0; Column]; Row];
    for i in 0..(area + 1) {
        if Board1Dim_2[i] < 0 {
            let x = i % Row;
            let y = i / Row;
            Board[x][y] = -1;
            for j in max(1, x) - 1..min(Row, x + 2) {
                for k in max(1, y) - 1..min(Column, y + 2) {
                    if Board[j][k] >= 0 {
                        Board[j][k] += 1;
                    }
                }
            }
        }
    }
    Board
}

#[pyfunction]
fn py_layMineNumber(Row: usize, Column: usize, MineNum: usize, X0: usize, Y0: usize) -> PyResult<Vec<Vec<i32>>> {
    // 通用标准埋雷引擎
    // 输出为二维的局面
    Ok(layMineNumber(Row, Column, MineNum, X0, Y0))
}

fn cal3BV(Board: &Vec<Vec<i32>>) -> usize {
    cal3BVonIsland(&Board) + calOp(Board.clone())
}

#[pyfunction]
fn py_cal3BV(Board: Vec<Vec<i32>>) -> PyResult<usize> {
    Ok(cal3BV(&Board))
}

#[pyfunction(Min3BV = 0, Max3BV = 1000_000, MaxTimes = 1000_000, method = 0)]
fn layMine(Row: usize, Column: usize, MineNum: usize, X0: usize, Y0: usize, Min3BV: usize, Max3BV: usize,
    MaxTimes: usize, method: usize) -> PyResult<(Vec<Vec<i32>>, Vec<usize>)> {
    // 埋雷，参数依次是行、列、雷数、起手位置的第几行-1、第几列-1
    // 适用于游戏的埋雷算法。
    // 起手不开空，必不为雷
    // 返回二维列表，0~8代表数字，-1代表雷
    // method = 0筛选算法；1调整算法
    let mut Times = 0;
    let mut Parameters = vec![];
    let mut Num3BV = 0;
    let mut Board = vec![vec![0; Column]; Row];
    while Times < MaxTimes {
        Board = layMineNumber(Row, Column, MineNum, X0, Y0);
        Times += 1;
        Num3BV = cal3BV(&Board);
        if Num3BV >= Min3BV && Num3BV <= Max3BV {
            Parameters.push(1);
            Parameters.push(Num3BV);
            Parameters.push(Times);
            return Ok((Board, Parameters))
        }
    }
    Parameters.push(0);
    Parameters.push(Num3BV);
    Parameters.push(Times);
    Ok((Board, Parameters))
}

fn SolveMinus(MatrixA: &Vec<Vec<i32>>, Matrixx: &Vec<(usize, usize)>, Matrixb: &Vec<i32>, BoardofGame: &mut Vec<Vec<i32>>,
) -> (Vec<(usize, usize)>, bool) {
    let mut flag = false;
    let mut NotMine = vec![];
    let mut NotMineRel = vec![];
    let mut IsMineRel = vec![];
    let mut MatrixColumn = Matrixx.len();
    let mut MatrixRow = Matrixb.len();
    if MatrixRow <= 1 {
        return (NotMine, false)
    }
    for i in 1..MatrixRow {
        for j in 0..i {
            let mut ADval1 = vec![];
            let mut ADvaln1 = vec![];
            let mut FlagAdj = false;
            for k in 0..MatrixColumn {
                if MatrixA[i][k] >= 1 && MatrixA[j][k] >= 1 {
                    FlagAdj = true;
                    continue;
                }
                if MatrixA[i][k] - MatrixA[j][k] == 1 {
                    ADval1.push(k)
                }
                else if MatrixA[i][k] - MatrixA[j][k] == -1 {
                    ADvaln1.push(k)
                }
            }
            if FlagAdj {
                let bDval = Matrixb[i] - Matrixb[j];
                if ADval1.len() as i32 == bDval {
                    IsMineRel.append(&mut ADval1);
                    NotMineRel.append(&mut ADvaln1);
                }
                else if ADvaln1.len() as i32 == -bDval {
                    IsMineRel.append(&mut ADvaln1);
                    NotMineRel.append(&mut ADval1);
                }
            }
        }
    }
    if IsMineRel.len() > 0 || NotMineRel.len() > 0 {
        flag = true;
    }
    IsMineRel.dedup();
    NotMineRel.dedup();
    for i in 0..NotMineRel.len() {
        NotMine.push(Matrixx[NotMineRel[i]]);
    }
    for i in IsMineRel {
        let (m, n) = Matrixx[i];
        BoardofGame[m][n] = 11;
    }
    (NotMine, flag)
}

#[pyfunction]
fn py_SolveMinus(mut MatrixA: Vec<Vec<i32>>, mut Matrixx: Vec<(usize, usize)>, mut Matrixb: Vec<i32>, mut BoardofGame: Vec<Vec<i32>>,
) -> PyResult<(Vec<Vec<i32>>, Vec<(usize, usize)>, bool)> {
    let (notMine, flag) = SolveMinus(&mut MatrixA, &mut Matrixx, &mut Matrixb, &mut BoardofGame);
    Ok((BoardofGame, notMine, flag))
}

fn refreshBoard(Board: &Vec<Vec<i32>>, BoardofGame: &mut Vec<Vec<i32>>, mut ClickedPoses: Vec<(usize, usize)>) {
    let Row = Board.len();
    let Column = Board[0].len();
    // let mut i: usize = 0;
    // let mut j: usize = 0;
    while let Some(top) = ClickedPoses.pop() {
        let (i, j) = top;
        if Board[i][j] > 0 {
            BoardofGame[i][j] = Board[i][j];
        }
        else if Board[i][j] == 0 {
            BoardofGame[i][j] = 0;
            for m in max(1, i) - 1..min(Row, i + 2) {
                for n in max(1, j) - 1..min(Column, j + 2) {
                    if (i!=m || j!=n) && BoardofGame[m][n] == 10 {
                        ClickedPoses.push((m,n));
                    }
                }
            }
        }
    }
}

#[pyfunction]
fn py_refreshBoard(board: Vec<Vec<i32>>, mut BoardofGame: Vec<Vec<i32>>, ClickedPoses: Vec<(usize, usize)>) -> PyResult<Vec<Vec<i32>>>{
    refreshBoard(&board, &mut BoardofGame, ClickedPoses);
    Ok(BoardofGame)
}

fn sum(v: &Vec<i32>) -> i32 {
    let mut ret = 0;
    for i in v {
        ret += *i;
    }
    ret
}

fn SolveDirect(MatrixA: &mut Vec<Vec<i32>>, Matrixx: &mut Vec<(usize, usize)>, Matrixb: &mut Vec<i32>, BoardofGame: &mut Vec<Vec<i32>>,
) -> (Vec<(usize, usize)>, bool) {
    let mut flag = false;
    let mut NotMine = vec![];
    let mut MatrixColumn = Matrixx.len();
    let mut MatrixRow = Matrixb.len();
    for i in (0..MatrixRow).rev() {
        if sum(&MatrixA[i]) == Matrixb[i] {
            flag = true;
            for k in (0..MatrixColumn).rev() {
                if MatrixA[i][k] == 1 {
                    let (m, n) = Matrixx[k];
                    BoardofGame[m][n] = 11;
                    Matrixx.remove(k);
                    for t in 0..MatrixRow {
                        if MatrixA[t][k] == 0 {
                            MatrixA[t].remove(k);
                        }
                        else {
                            MatrixA[t].remove(k);
                            Matrixb[t] -= 1;
                        }
                    }
                    MatrixColumn -= 1;
                }
            }
            MatrixA.remove(i);
            Matrixb.remove(i);
            MatrixRow -= 1;
        }
    }
    for i in 0..MatrixRow {
        if Matrixb[i]==0 {
            flag = true;
            for k in 0..MatrixColumn {
                if MatrixA[i][k] == 1 {
                    NotMine.push(Matrixx[k]);
                }
            }
        }
    }
    NotMine.dedup();
    (NotMine, flag)
}

#[pyfunction]
fn py_SolveDirect(mut MatrixA: Vec<Vec<i32>>, mut Matrixx: Vec<(usize, usize)>, mut Matrixb: Vec<i32>, mut BoardofGame: Vec<Vec<i32>>,
) -> PyResult<(Vec<Vec<i32>>, Vec<(usize, usize)>, bool)> {
    let (notMine, flag) = SolveDirect(&mut MatrixA, &mut Matrixx, &mut Matrixb, &mut BoardofGame);
    Ok((BoardofGame, notMine, flag))
}


fn layMineOpNumber(Row: usize, Column: usize, MineNum: usize, X0: usize, Y0: usize) -> Vec<Vec<i32>> {
    let mut rng = thread_rng();
    let mut areaOp = 9;
    if X0 == 0 || Y0 == 0 || X0 == Row - 1 || Y0 == Column - 1 {
        if X0 == 0 && Y0 == 0 || X0 == 0 && Y0 == Column - 1 || X0 == Row - 1 && Y0 == 0 || X0 == Row - 1 && Y0 == Column - 1 {
            areaOp = 4;
        }
        else {
            areaOp = 6;
        }
    }
    let area = Row * Column - areaOp;
    let mut Board1Dim = vec![0; area - MineNum];
    Board1Dim.append(&mut vec![-1; MineNum]);
    Board1Dim.shuffle(&mut rng);
    let mut Board = vec![vec![0; Column]; Row];
    let mut skip = 0;
    for i in 0..(area + areaOp) {
        let x = i % Row;
        let y = i / Row;
        if x <= X0 + 1 && X0 <= x + 1 && y <= Y0 + 1 && Y0 <= y + 1 {
            skip += 1;
            continue;
        }
        if Board1Dim[i - skip] < 0 {
            Board[x][y] = -1;
            for j in max(1, x) - 1..min(Row, x + 2) {
                for k in max(1, y) - 1..min(Column, y + 2) {
                    if Board[j][k] >= 0 {
                        Board[j][k] += 1
                    }
                }
            }
        }
    }
    Board
}

#[pyfunction]
fn py_layMineOpNumber(Row: usize, Column: usize, MineNum: usize, X0: usize, Y0: usize) -> PyResult<Vec<Vec<i32>>> {
    Ok(layMineOpNumber(Row, Column, MineNum, X0, Y0))
}

#[pyfunction(Min3BV = 0, Max3BV = 1000_000, MaxTimes = 1000_000, method = 0)]
fn layMineOp(Row: usize, Column: usize, MineNum: usize, X0: usize, Y0: usize, Min3BV: usize, Max3BV: usize,
    MaxTimes: usize, method: usize) -> PyResult<(Vec<Vec<i32>>, Vec<usize>)> {
    let mut Times = 0;
    let mut Parameters = vec![];
    let mut Num3BV = 0;
    let mut Board = vec![vec![0; Column]; Row];
    while Times < MaxTimes {
        Board = layMineOpNumber(Row, Column, MineNum, X0, Y0);
        Times += 1;
        let mut Num3BV = cal3BV(&Board);
        if Num3BV >= Min3BV && Num3BV <= Max3BV {
            Parameters.push(1);
            Parameters.push(Num3BV);
            Parameters.push(Times);
            return Ok((Board, Parameters))
        }
    }
    Parameters.push(0);
    Parameters.push(Num3BV);
    Parameters.push(Times);
    Ok((Board, Parameters))
}

fn SolveEnumerate(MatrixA: &Vec<Vec<i32>>, Matrixx: &Vec<(usize, usize)>, Matrixb: &Vec<i32>, BoardofGame: &mut Vec<Vec<i32>>,
enuLimit: usize) -> (Vec<(usize, usize)>, bool) {
    let mut flag = false;
    let mut NotMine = vec![];
    let mut NotMineRel = vec![];
    let mut IsMineRel = vec![];
    let mut MatrixColumn = Matrixx.len();
    let MatrixRow = Matrixb.len();
    let mut ColId: Vec<usize> = (0..MatrixColumn).collect();
    let mut RowId: Vec<usize> = (0..MatrixRow).collect();
    let mut TempCol = vec![];
    let mut TempRow = vec![];
    while let Some(top) = ColId.pop() {
    // while ColId {
        TempCol.push(top);
        let mut Groupb = vec![];
        let mut Groupx = vec![];
        let mut GroupCol: Vec<usize> = vec![];
        let mut GroupRow = vec![];
        while !(TempCol.is_empty() && TempRow.is_empty()) {
            if !TempCol.is_empty() {
                for i in 0..MatrixRow {
                    let len = TempCol.len() - 1;
                    if MatrixA[i][TempCol[len]] == 1 {
                        for ii in (0..RowId.len()).rev() {
                            TempRow.push(RowId[ii]);
                            RowId.remove(ii);
                        }
                    }
                }
                if let Some(temp) = TempCol.pop() {
                    GroupCol.push(temp);
                    Groupx.push(Matrixx[temp]);
                }
            }
            if !TempRow.is_empty() {
                for j in 0..MatrixColumn {
                    let len = TempRow.len() - 1;
                    if MatrixA[TempRow[len]][j] == 1 {
                        for jj in (0..ColId.len()).rev() {
                            TempCol.push(jj);
                            ColId.remove(jj);
                        }
                    }
                }
                if let Some(temp) = TempRow.pop() {
                    GroupRow.push(temp);
                    Groupb.push(Matrixb[temp]);
                }
            }
        }
        if GroupCol.len() >= enuLimit {
            continue;
        }
        let mut AllTable: Vec<Vec<usize>> = vec![vec![2; GroupCol.len()]];
        for i in GroupRow {
            let b = Matrixb[i];
            let mut TableId = vec![];
            for j in 0..GroupCol.len() {
                if MatrixA[i][GroupCol[j]] == 1 {
                    TableId.push(GroupCol[j]);
                }
            }
            AllTable = enuOneStep(AllTable, TableId, b);
        }
        for j in 0..GroupCol.len() {
            if AllTable[0][j] == 0 {
                NotMineRel.push(GroupCol[j]);
                for i in 1..AllTable.len() {
                    if AllTable[i][j] == 1 {
                        NotMineRel.pop();
                        break;
                    }
                }
            }
            else {
                IsMineRel.push(GroupCol[j]);
                for i in 1..AllTable.len() {
                    if AllTable[i][j] == 0 {
                        IsMineRel.pop();
                        break;
                    }
                }
            }
        }
    }
    IsMineRel.dedup();
    NotMineRel.dedup();
    IsMineRel.sort_by(|a, b| b.cmp(&a));
    for i in NotMineRel {
        NotMine.push(Matrixx[i]);
    }
    for i in IsMineRel {
        let (m, n) = Matrixx[i];
        BoardofGame[m][n] = 11;
    }
    (NotMine, flag)
}

#[pyfunction(enuLimit = 30)]
fn py_SolveEnumerate(MatrixA: Vec<Vec<i32>>, Matrixx: Vec<(usize, usize)>, Matrixb: Vec<i32>, mut BoardofGame: Vec<Vec<i32>>,
enuLimit: usize) -> PyResult<(Vec<Vec<i32>>, Vec<(usize, usize)>, bool)> {
    let (notMine, flag) = SolveEnumerate(&MatrixA, &Matrixx, &Matrixb, &mut BoardofGame, enuLimit);
    Ok((BoardofGame, notMine, flag))
}

fn enuOneStep(mut AllTable: Vec<Vec<usize>>, TableId: Vec<usize>, b: i32) -> Vec<Vec<usize>> {
    // AllTable不能为空
    let mut NewId: Vec<usize> = vec![];
    for i in &TableId {
        if AllTable[0][*i] == 2 {
            NewId.push(*i);
        }
    }
    let mut DelId = vec![];
    for i in 0..AllTable.len() {
        let mut ExtraMine = b;
        for j in &TableId {
            if AllTable[i][*j] == 1 {
                ExtraMine -= 1;
            }
        }
        if ExtraMine < 0 || ExtraMine as usize > NewId.len() {
            DelId.push(i);
            continue;
        }
        let mut AddedTable = enumerateSub(NewId.len(), ExtraMine as usize);
        for t in 0..NewId.len() {
            AllTable[i][NewId[t]] = AddedTable[0][t];
        }
        for m in 1..AddedTable.len() {
            AllTable.push(AllTable[i].clone());
            for t in 0..NewId.len() {
                let len = AllTable.len() - 1;
                AllTable[len][NewId[t]] = AddedTable[m][t];
            }
        }
    }
    DelId.sort_by(|a, b| b.cmp(&a));
    for i in DelId {
        AllTable.remove(i);
    }
    AllTable
}

#[pyfunction]
fn py_enuOneStep(AllTable: Vec<Vec<usize>>, TableId: Vec<usize>, b: i32) -> PyResult<Vec<Vec<usize>>> {
    Ok(enuOneStep(AllTable, TableId, b))
}

fn enumerateSub(Col: usize, MineNum: usize) -> Vec<Vec<usize>> {
    let mut Out: Vec<Vec<usize>> = vec![];
    for i in (0..Col).combinations(MineNum) {
        Out.push(vec![0; Col]);
        let len = Out.len() - 1;
        for j in 0..MineNum {
            Out[len][i[j]] = 1;
        }
    }
    Out
}

fn isVictory(BoardofGame: &Vec<Vec<i32>>, Board: &Vec<Vec<i32>>) -> bool {
    // 判断当前是否获胜
    // 游戏局面中必须没有标错的雷
    // 这个函数不具备普遍意义
    let Row = BoardofGame.len();
    let Col = BoardofGame[0].len();
    for i in 0..Row {
        for j in 0..Col {
            if BoardofGame[i][j] == 10 && Board[i][j] != -1 {
                return false
            }
        }
    }
    return true
}

fn unsolvableStructure(BoardCheck: &Vec<Vec<i32>>) -> bool {
    // 用几种模板，检测局面中是否有明显的死猜的结构
    // 不考虑起手位置，因为起手必开空
    // 局面至少大于4*4
    // 返回0或1
    let Row = BoardCheck.len();
    let Column = BoardCheck[0].len();
    let mut Board = vec![vec![0; Column]; Row];
    for i in 0..Row {
        for j in 0..Column {
            if BoardCheck[i][j] == -1 {
                Board[i][j] = -1;
            }
        }
    }
    for i in 0..Row-2 {       // 检查左右两侧的工
        if i < Row-3 {
            if Board[i][0] == -1 && Board[i][1] == -1 && Board[i+3][0] == -1 && Board[i+3][1] == -1 &&
             Board[i+1][0]+Board[i+2][0] == -1 || Board[i][Column-1] == -1 && Board[i][Column-2] == -1 &&
              Board[i+3][Column-1] == -1 && Board[i+3][Column-2] == -1 && Board[i+1][Column-1]+Board[i+2][Column-1] == -1 {
                return true
            }
        }
        if Board[i][2] == -1 && Board[i+1][2] == -1 && Board[i+2][2] == -1 && Board[i+1][0]+Board[i+1][1] == -1 ||
         Board[i][Column-3] == -1 && Board[i+1][Column-3] == -1 && Board[i+2][Column-3] == -1 &&
          Board[i+1][Column-1] + Board[i+1][Column-2] == -1 || Board[i][0] == -1 && Board[i][1] == -1 &&
           Board[i+1][1] == -1 && Board[i+2][1] == -1 && Board[i+2][0] == -1 && Board[i+1][0] == 0 ||
            Board[i][Column-1] == -1 && Board[i][Column-2] == -1 && Board[i+1][Column-2] == -1 &&
             Board[i+2][Column-2] == -1 && Board[i+2][Column-1] == -1 && Board[i+1][Column-1] == 0 {
            return true
        }
        if i < Row-3 {
            if Board[i][2] == -1 && Board[i+3][2] == -1 && Board[i+1][0]+Board[i+1][1] == -1 &&
             Board[i+1][1]+Board[i+2][1] == -1 && Board[i+2][1]+Board[i+2][0] == -1 || Board[i][Column-3] == -1 &&
              Board[i+3][Column-3] == -1 && Board[i+1][Column-1]+Board[i+1][Column-2] == -1 &&
               Board[i+1][Column-2]+Board[i+2][Column-2] == -1 && Board[i+2][Column-2]+Board[i+2][Column-1] == -1 {
                return true
            }
        }
    }
    for j in 0..Column-2 {          // 检查上下两侧
        if j < Column-3 {
            if Board[0][j] == -1 && Board[1][j] == -1 && Board[0][j+3] == -1 && Board[1][j+3] == -1 &&
             Board[0][j+1]+Board[0][j+2] == -1 || Board[Row-1][j] == -1 && Board[Row-2][j] == -1 &&
              Board[Row-1][j+3] == -1 && Board[Row-2][j+3] == -1 && Board[Row-1][j+1]+Board[Row-1][j+2] == -1 {
                return true
            }
        }
        if Board[2][j] == -1 && Board[2][j+1] == -1 && Board[2][j+2] == -1 && Board[0][j+1]+Board[1][j+1] == -1 ||
         Board[Row-3][j] == -1 && Board[Row-3][j+1] == -1 && Board[Row-3][j+2] == -1 &&
          Board[Row-1][j+1]+Board[Row-2][j+1] == -1 || Board[0][j] == -1 && Board[1][j] == -1 &&
           Board[1][j+1] == -1 && Board[1][j+2] == -1 && Board[0][j+2] == -1 && Board[0][j+1] == 0 ||
            Board[Row-1][j] == -1 && Board[Row-2][j] == -1 && Board[Row-2][j+1] == -1 && Board[Row-2][j+2] == -1 &&
             Board[Row-1][j+2] == -1 && Board[Row-1][j+1] == 0 {
            return true
        }
        if j < Column-3 {
            if Board[2][j] == -1 && Board[2][j+3] == -1 && Board[0][j+1]+Board[1][j+1] == -1 &&
             Board[1][j+1]+Board[1][j+2] == -1 && Board[1][j+2]+Board[0][j+2] == -1 || Board[Row-3][j] == -1 &&
              Board[Row-3][j+3] == -1 && Board[Row-1][j+1]+Board[Row-2][j+1] == -1 &&
               Board[Row-2][j+1]+Board[Row-2][j+2] == -1 && Board[Row-2][j+2]+Board[Row-1][j+2] == -1 {
                return true
            }
        }
    }
    if Board[0][2] == -1 && Board[1][2] == -1 && Board[0][0]+Board[0][1] == -1 || Board[2][0] == -1 &&
     Board[2][1] == -1 && Board[0][0]+Board[1][0] == -1 || Board[0][Column-3] == -1 && Board[1][Column-3] == -1 &&
      Board[0][Column-1]+Board[0][Column-2] == -1 || Board[2][Column-1] == -1 && Board[2][Column-2] == -1 &&
       Board[0][Column-1]+Board[1][Column-1] == -1 || Board[Row-1][2] == -1 && Board[Row-2][2] == -1 &&
        Board[Row-1][0]+Board[Row-1][1] == -1 || Board[Row-3][0] == -1 && Board[Row-3][1] == -1 &&
         Board[Row-1][0]+Board[Row-2][0] == -1 || Board[Row-1][Column-3] == -1 && Board[Row-2][Column-3] == -1 &&
          Board[Row-1][Column-1]+Board[Row-1][Column-2] == -1 || Board[Row-3][Column-1] == -1 &&
           Board[Row-3][Column-2] == -1 && Board[Row-1][Column-1]+Board[Row-2][Column-1] == -1 ||
            Board[0][1]+Board[1][1]+Board[1][0] == -3 && Board[0][0] == 0 ||
             Board[0][Column-2]+Board[1][Column-2]+Board[1][Column-1] == -3 && Board[0][Column-1] == 0 ||
              Board[Row-1][Column-2]+Board[Row-2][Column-2]+Board[Row-2][Column-1] == -3 && Board[Row-1][Column-1] == 0 ||
               Board[Row-1][1]+Board[Row-2][1]+Board[Row-2][0] == -3 && Board[Row-1][0] == 0 || Board[2][2] == -1 &&
                Board[0][1]+Board[1][1] == -1 && Board[1][0]+Board[1][1] == -1 || Board[Row-3][2] == -1 &&
                 Board[Row-1][1]+Board[Row-2][1] == -1 && Board[Row-2][0]+Board[Row-2][1] == -1 ||
                  Board[Row-3][Column-3] == -1 && Board[Row-1][Column-2]+Board[Row-2][Column-2] == -1 &&
                   Board[Row-2][Column-1]+Board[Row-2][Column-2] == -1 || Board[2][Column-3] == -1 &&
                    Board[0][Column-2]+Board[1][Column-2] == -1 && Board[1][Column-1]+Board[1][Column-2] == -1 {     //检查四个角
        return true
    }
    for i in 0..Row-2 {        // 找中间的工、回、器形结构
        for j in 0..Column-2 {
            if j < Column-3 {
                if Board[i][j] == -1 && Board[i+1][j] == -1 && Board[i+2][j] == -1 && Board[i][j+3] == -1 &&
                 Board[i+1][j+3] == -1 && Board[i+2][j+3] == -1 && Board[i+1][j+1]+Board[i+1][j+2] == -1 {
                    return true
                }
            }
            if i < Row-3 {
                if Board[i][j] == -1 && Board[i][j+1] == -1 && Board[i][j+2] == -1 && Board[i+3][j] == -1 &&
                 Board[i+3][j+1] == -1 && Board[i+3][j+2] == -1 && Board[i+1][j+1]+Board[i+2][j+1] == -1 {
                    return true
                }
            }
            if Board[i][j] == -1 && Board[i+1][j] == -1 && Board[i+2][j] == -1 && Board[i][j+1] == -1 &&
             Board[i+2][j+1] == -1 && Board[i][j+2] == -1 && Board[i+1][j+2] == -1 && Board[i+2][j+2] == -1 && Board[i+1][j+1] == 0 {
                return true
            }
            if j < Column-3 && i < Row-3 {
                if Board[i][j] == -1 && Board[i+3][j] == -1 && Board[i][j+3] == -1 && Board[i+3][j+3] == -1 &&
                 Board[i+1][j+1]+Board[i+2][j+1] == -1 && Board[i+1][j+1]+Board[i+1][j+2] == -1 &&
                  Board[i+2][j+1]+Board[i+2][j+2] == -1 {
                    return true
                }
            }
        }
    }
    false
}

#[pyfunction]
fn py_unsolvableStructure(BoardCheck: Vec<Vec<i32>>) -> PyResult<bool> {
    Ok(unsolvableStructure(&BoardCheck))
}

fn isSolvable(Board: &Vec<Vec<i32>>, X0: usize, Y0: usize, enuLimit: usize) -> bool {
    // 从指定位置开始扫，判断局面是否无猜
    // 周围一圈都是雷，那么中间是雷不算猜，中间不是雷算猜
    if unsolvableStructure(&Board) {     //若包含不可判雷结构，则不是无猜
        return false
    }
    let Row = Board.len();
    let Column = Board[0].len();
    let mut BoardofGame = vec![vec![10; Column]; Row];
    // 10是未打开，11是标雷
    // 局面大小必须超过6*6
    refreshBoard(&Board, &mut BoardofGame, vec![(X0,Y0)]);
    if isVictory(&BoardofGame, &Board) {
        return true             // 暂且认为点一下就扫开也是可以的
    }
    let mut NotMine;
    let mut flag;
    loop {
        let (mut MatrixA, mut Matrixx, mut Matrixb) = refreshMatrix(&BoardofGame);
        let ans = SolveDirect(&mut MatrixA, &mut Matrixx, &mut Matrixb, &mut BoardofGame);
        NotMine = ans.0;
        flag = ans.1;
        if !flag {
            let ans = SolveMinus(&MatrixA, &Matrixx, &Matrixb, &mut BoardofGame);
            NotMine = ans.0;
            flag = ans.1;
            if !flag {
                let ans = SolveEnumerate(&MatrixA, &Matrixx, &Matrixb, &mut BoardofGame, enuLimit);
                NotMine = ans.0;
                flag = ans.1;
                if !flag {
                    return false
                }
            }
        }
        refreshBoard(&Board, &mut BoardofGame, NotMine);
        if isVictory(&BoardofGame, &Board) {
            return true
        }
    }
}

#[pyfunction(enuLimit = 30)]
fn py_isSolvable(Board: Vec<Vec<i32>>, X0: usize, Y0: usize, enuLimit: usize) -> PyResult<bool> {
    Ok(isSolvable(&Board, X0, Y0, enuLimit))
}

#[pyfunction(Min3BV = 0, Max3BV = 1000000, MaxTimes = 1000000, enuLimit = 30)]
fn layMineSolvable(Row: usize, Column: usize, MineNum: usize, X0: usize, Y0: usize, Min3BV: usize, Max3BV: usize,
                    MaxTimes: usize, enuLimit: usize) -> PyResult<(Vec<Vec<i32>>, Vec<usize>)> {
    // 3BV下限、上限，最大尝试次数，返回是否成功。
    // 若不成功返回最后生成的局面（不一定无猜），默认尝试十万次
    let mut Times = 0;
    let mut Parameters = vec![];
    let mut Board;
    let mut Num3BV;
    while Times < MaxTimes {
        Board = layMineOpNumber(Row, Column, MineNum, X0, Y0);
        Times += 1;
        if isSolvable(&Board, X0, Y0,enuLimit) {
            Num3BV = cal3BV(&Board);
            if Num3BV >= Min3BV && Num3BV <= Max3BV {
                Parameters.push(1);
                Parameters.push(Num3BV);
                Parameters.push(Times);
                return Ok((Board, Parameters))
            }
        }
    }
    Board = layMineOpNumber(Row, Column, MineNum, X0, Y0);
    Num3BV = cal3BV(&Board);
    Parameters.push(0);
    Parameters.push(Num3BV);
    Parameters.push(Times);
    Ok((Board, Parameters))
}

#[pyfunction(Min3BV = 0, Max3BV = 1000000, MaxTimes = 1000000, enuLimit = 30)]
fn layMineSolvable_thread(Row: usize, Column: usize, MineNum: usize, X0: usize, Y0: usize, Min3BV: usize, Max3BV: usize,
    mut MaxTimes: usize, enuLimit: usize) -> PyResult<(Vec<Vec<i32>>, [usize; 3])> {
    // 多线程埋雷无猜
    let mut parameters = [0, 0, 0];
    let mut game_board = vec![vec![0; Column]; Row];
    let mut handles = vec![];
    let flag_exit = Arc::new(Mutex::new(0));
    let (tx, rx) = mpsc::channel();// mpsc 是多个发送者，一个接收者
    for ii in (1..11).rev() {
        let tx_ = mpsc::Sender::clone(&tx);
        let max_time = MaxTimes/ii;
        MaxTimes -= max_time;
        let flag_exit = Arc::clone(&flag_exit);
        let handle = thread::spawn(move || {
            let mut Num3BV;
            let mut counter = 0;
            let mut Board = vec![vec![0; Column]; Row];
            let mut para = [0, 0, 0];
            while counter < max_time {
                {let f = flag_exit.lock().unwrap();
                if *f == 1 {
                    break;
                }} // 这块用花括号控制生命周期
                let Board_ = layMineOpNumber(Row, Column, MineNum, X0, Y0);
                counter += 1;
                if isSolvable(&Board_, X0, Y0,enuLimit) {
                    Num3BV = cal3BV(&Board_);
                    if Num3BV >= Min3BV && Num3BV <= Max3BV {
                        para[0] = 1;
                        para[1] = Num3BV;
                        para[2] = counter;
                        for i in 0..Row {
                            for j in 0..Column {
                                Board[i][j] = Board_[i][j];
                            }
                        }
                        let mut f = flag_exit.lock().unwrap();
                        *f = 1;
                        tx_.send((Board, para)).unwrap();
                        break;
                    }
                }
            }
            let Board_ = layMineOpNumber(Row, Column, MineNum, X0, Y0);
            Num3BV = cal3BV(&Board_);
            para[0] = 0;
            para[1] = Num3BV;
            para[2] = max_time + 1;
            tx_.send((Board_, para)).unwrap();
        });
        handles.push(handle);
    }
    for handle in handles {
        handle.join().unwrap();
    }
    let received = rx.recv().unwrap(); // 尝试次数仅仅为单个线程的次数，并不准
    parameters[0] = received.1[0];
    parameters[1] = received.1[1];
    parameters[2] = received.1[2];
    for i in 0..Row {
        for j in 0..Column {
            game_board[i][j] = received.0[i][j];
        }
    }
    Ok((game_board, parameters))
}

#[derive(Clone, Debug)]
struct big_number {
    // 科学计数法表示的大数字
    // 必定大于等于1，a必定满足小于10大于等于1
    a: f64,
    b: i32,
}

impl big_number {
    fn a_become_smaller_than(&mut self, thrd: f64) {
        // 如果big_number大于thrd
        // 把位数都放到指数上，使其满足a小于10大于等于1
        if self.a < thrd {
            return;
        }
        while self.a >= 10.0 {
            self.a /= 10.0;
            self.b += 1;
        }
    }
    fn mul_usize(&mut self, k: usize) {
        // 与usize相乘
        if k == 0 {
            self.a = 0.0;
            self.b = 1;
        } else {
            self.a *= k as f64;
            self.a_become_smaller_than(10.0);
        }
    }
    fn mul_big_number(&mut self, k: &big_number) {
        // 与big_number相乘, big_number必须至少为1
        self.a *= k.a;
        self.b += k.b;
        self.a_become_smaller_than(10.0);
    }
    fn add_big_number(&mut self, k: &big_number) {
        let mut ka = k.a;
        let mut kb = k.b;
        while self.b > kb {
            ka /= 10.0;
            kb += 1;
        }
        while self.b < kb {
            self.a /= 10.0;
            self.b += 1;
        }
        self.a += ka;
        self.a_become_smaller_than(10.0);
    }
    fn div_big_num(&mut self, k: &big_number) -> f64 {
        // 计算大数相除
        let mut ans = self.a / k.a;
        while self.b < k.b {
            ans /= 10.0;
            self.b += 1;
        }
        while self.b > k.b {
            ans *= 10.0;
            self.b -= 1;
        }
        ans
    }
    fn div_usize(&mut self, k: usize) {
        // 计算大数除以正整数。这里被除数大于等于0；除数大于等于1
        if self.a < 1e-8 && self.b == 1 {
            return
        } else {
            self.a /= k as f64;
            while self.a < 1.0 {
                self.a *= 10.0;
                self.b -= 1;
            }
        }
    }
}

fn C(n: usize, k: usize) -> big_number {
    // n不超过1e10
    if n < k + k {
        return C(n, n - k);
    };
    let maximum_limit: f64 = 1e208;
    let mut c = big_number { a: 1.0, b: 0 };
    for i in 0..k {
        c.a *= (n - i) as f64;
        c.a /= (i + 1) as f64;
        c.a_become_smaller_than(maximum_limit);
    }
    c.a_become_smaller_than(10.0);
    c
}

fn C_usize(n: usize, k: usize) -> usize {
    // 小数字的组合数计算
    if n < k + k {
        return C_usize(n, n - k);
    };
    let mut c = 1;
    for i in 0..k {
        c *= n - i;
    }
    for i in 0..k {
        c /= i + 1;
    }
    c
}

fn combine(
    MatrixA: Vec<Vec<i32>>,
    Matrixx: Vec<(usize, usize)>,
) -> (Vec<Vec<i32>>, Vec<(usize, usize)>, Vec<Vec<usize>>) {
    // 检查地位完全相同的格子，全部返回。例如[[3,1,2],[0,5],[4],[6]]
    // MatrixA不能为空
    // 并在内部更改矩阵，合并重复的列
    let mut matrixA_squeeze = MatrixA;
    let mut matrixx_squeeze = Matrixx;
    let mut pair_cells = vec![];
    let mut del_cells = vec![]; // 由于重复需要最后被删除的列
    for i in 0..matrixx_squeeze.len() {
        pair_cells.push(vec![i]);
        for j in i + 1..matrixA_squeeze[0].len() {
            if !matrixA_squeeze.iter().any(|x| x[i] != x[j]) {
                pair_cells[i].push(j);
                del_cells.push(j);
            }
        }
    }
    del_cells.sort_by(|a, b| b.cmp(&a));
    del_cells.dedup();
    for i in del_cells {
        for r in 0..matrixA_squeeze.len() {
            matrixA_squeeze[r].remove(i);
        }
        matrixx_squeeze.remove(i);
        pair_cells.remove(i);
    }
    let cell_squeeze_num = pair_cells.len();
    for i in 0..cell_squeeze_num {
        let k = pair_cells[i].len() as i32;
        for r in 0..matrixA_squeeze.len() {
            matrixA_squeeze[r][i] *= k;
        }
    }
    (matrixA_squeeze, matrixx_squeeze, pair_cells)
}

fn enum_comb(
    matrixA_squeeze: &Vec<Vec<i32>>,
    matrixx_squeeze: &Vec<(usize, usize)>,
    Matrixb: &Vec<i32>,
) -> Vec<Vec<usize>> {
    // 返回一个包含所有情况的表
    let Column = matrixx_squeeze.len();
    let Row = matrixA_squeeze.len();
    let mut enum_comb_table = vec![vec![0; Column]];
    let mut not_enum_cell: Vec<bool> = vec![true; Column]; // 记录每个位置是否被枚举过，true是没有被枚举过
    let mut enum_cell_table: Vec<Vec<usize>> = vec![];
    for row in 0..Row {
        let mut new_enum_cell = vec![]; // 当前条件涉及的新格子
        let mut enum_cell = vec![]; // 当前条件涉及的所有格子
        let mut new_enum_max = vec![];
        for j in 0..Column {
            if matrixA_squeeze[row][j] > 0 {
                enum_cell.push(j);
                if not_enum_cell[j] {
                    not_enum_cell[j] = false;
                    new_enum_cell.push(j);
                    new_enum_max.push(matrixA_squeeze[row][j]);
                }
            }
        }
        // 第一步，整理出当前条件涉及的所有格子，以及其中哪些是新格子
        let mut new_enum_table = (0..new_enum_cell.len())
            .map(|i| 0..new_enum_max[i] + 1)
            .multi_cartesian_product()
            .collect::<Vec<_>>();
        new_enum_table.retain(|x| x.iter().sum::<i32>() <= Matrixb[row]);
        // println!("{:?}", new_enum_table);
        // 第二步，获取这些新枚举到的格子的所有满足周围雷数约束的情况，即子枚举表
        if new_enum_table.is_empty() {
            enum_comb_table.retain(|item| {
                enum_cell
                    .iter()
                    .fold(0, |sum: usize, i: &usize| sum + item[*i])
                    == Matrixb[row] as usize
            });
        // 第三步，若子枚举表为空，不用将子枚举表与主枚举表合并；且只检查主枚举表是否满足当前这条规则，删除一些不满足的
        } else {
            let mut flag_1 = true; // 代表新枚举的格子是否需要新增情况
            let enum_comb_table_len = enum_comb_table.len();
            for item in new_enum_table {
                if flag_1 {
                    for m in 0..new_enum_cell.len() {
                        for n in 0..enum_comb_table_len {
                            enum_comb_table[n][new_enum_cell[m]] = item[m] as usize;
                        }
                    }
                    flag_1 = false;
                } else {
                    for n in 0..enum_comb_table_len {
                        let mut one_row_in_new_table = enum_comb_table[n].clone();
                        for m in 0..new_enum_cell.len() {
                            one_row_in_new_table[new_enum_cell[m]] = item[m] as usize;
                        }
                        enum_comb_table.push(one_row_in_new_table);
                    }
                }
            } // 第四步，若子枚举表非空，先将子枚举表与主枚举表合并
            let mut equations = vec![];
            for kk in &enum_cell {
                for rr in 0..row {
                    if matrixA_squeeze[rr][*kk] > 0 {
                        equations.push(rr);
                    }
                }
            }
            equations.dedup();
            // 第五步，再找出本条规则涉及的之前所有的规则的id
            for equ in equations {
                enum_comb_table.retain(|item| {
                    enum_cell_table[equ]
                        .iter()
                        .fold(0, |sum: usize, i: &usize| sum + item[*i])
                        == Matrixb[equ] as usize
                });
            }
            enum_comb_table.retain(|item| {
                enum_cell
                    .iter()
                    .fold(0, |sum: usize, i: &usize| sum + item[*i])
                    == Matrixb[row] as usize
            }); // 这段重复了，不过不影响性能，之后优化
                // 第六步，用本条规则、以及涉及的之前所有规则过滤所有情况
        }
        enum_cell_table.push(enum_cell);
    }
    enum_comb_table
}

fn refresh_matrixs(
    board_of_game: &Vec<Vec<i32>>,
) -> (
    Vec<Vec<Vec<i32>>>,
    Vec<Vec<(usize, usize)>>,
    Vec<Vec<i32>>,
    usize,
) {
    // 根据游戏局面分块生成矩阵。分块的数据结构是最外面再套一层Vec
    // board_of_game必须且肯定是正确标雷的游戏局面，但不需要标全
    // 矩阵的行和列都可能有重复
    // unknow_block是未知格子数量
    let Row = board_of_game.len();
    let Column = board_of_game[0].len();
    let mut unknow_block = 0;
    let mut matrix_as = vec![];
    let mut matrix_xs = vec![];
    let mut matrix_bs = vec![];
    let mut all_cell: Vec<(usize, usize)> = vec![]; // 记录所有周围有未打开格子的数字的位置
    for i in 0..Row {
        for j in 0..Column {
            if board_of_game[i][j] > 0 && board_of_game[i][j] < 10 {
                for m in max(1, i) - 1..min(Row, i + 2) {
                    for n in max(1, j) - 1..min(Column, j + 2) {
                        if board_of_game[m][n] == 10 {
                            if !all_cell.iter().any(|x| x.0 == i && x.1 == j) {
                                all_cell.push((i, j));
                            }
                        }
                    }
                }
            } else if board_of_game[i][j] == 10 {
                let mut flag = true;
                for m in max(1, i) - 1..min(Row, i + 2) {
                    for n in max(1, j) - 1..min(Column, j + 2) {
                        if board_of_game[m][n] < 10 {
                            flag = false;
                        }
                    }
                }
                if flag {
                    unknow_block += 1;
                }
            }
        }
    }
    let mut p = 0; //指针，代表第几块
    while !all_cell.is_empty() {
        matrix_xs.push(vec![]);
        matrix_bs.push(vec![]);
        let x_0 = all_cell[0].0;
        let y_0 = all_cell[0].1;
        let mut num_cells = vec![]; // 记录了当前块的数字格的坐标
        let mut temp_cells = vec![]; // 记录了待查找的数字格的坐标
        let mut flag_num = 0;
        for m in max(1, x_0) - 1..min(Row, x_0 + 2) {
            for n in max(1, y_0) - 1..min(Column, y_0 + 2) {
                if board_of_game[m][n] == 10 {
                    matrix_xs[p].push((m, n));
                }
                if board_of_game[m][n] == 11 {
                    flag_num += 1;
                }
            }
        }
        matrix_bs[p].push(board_of_game[x_0][y_0] - flag_num);
        num_cells.push((x_0, y_0));
        temp_cells.push((x_0, y_0));
        while !temp_cells.is_empty() {
            let x_e = temp_cells[0].0;
            let y_e = temp_cells[0].1;
            temp_cells.remove(0);
            for t in (1..all_cell.len()).rev() {
                // 从temp_cells中拿出一个格子，找出与其相邻的所有格子，加入temp_cells和matrix_bs、matrix_xs
                let x_t = all_cell[t].0;
                let y_t = all_cell[t].1;
                if x_t >= x_e + 3 || x_e >= x_t + 3 || y_t >= y_e + 3 || y_e >= y_t + 3 {
                    continue;
                }
                let mut flag_be_neighbor = false;
                for m in max(1, max(x_t, x_e)) - 1..min(Row, min(x_t + 2, x_e + 2)) {
                    for n in max(1, max(y_t, y_e)) - 1..min(Row, min(y_t + 2, y_e + 2)) {
                        if board_of_game[m][n] == 10 {
                            flag_be_neighbor = true;
                            break;
                        }
                    }
                } // 从局面上看，如果两个数字有相同的未知格子，那么就会分到同一块
                if flag_be_neighbor {
                    let mut flag_num = 0;
                    for m in max(1, x_t) - 1..min(Row, x_t + 2) {
                        for n in max(1, y_t) - 1..min(Column, y_t + 2) {
                            if board_of_game[m][n] == 10 {
                                if !matrix_xs[p].iter().any(|x| x.0 == m && x.1 == n) {
                                    matrix_xs[p].push((m, n));
                                }
                            }
                            if board_of_game[m][n] == 11 {
                                flag_num += 1;
                            }
                        }
                    }
                    matrix_bs[p].push(board_of_game[x_t][y_t] - flag_num);
                    num_cells.push((x_t, y_t));
                    temp_cells.push(all_cell[t]);
                    all_cell.remove(t);
                }
            }
        }
        matrix_as.push(vec![vec![0; matrix_xs[p].len()]; matrix_bs[p].len()]);
        for i in 0..num_cells.len() {
            for j in 0..matrix_xs[p].len() {
                if num_cells[i].0 <= matrix_xs[p][j].0 + 1
                    && matrix_xs[p][j].0 <= num_cells[i].0 + 1
                    && num_cells[i].1 <= matrix_xs[p][j].1 + 1
                    && matrix_xs[p][j].1 <= num_cells[i].1 + 1
                {
                    matrix_as[p][i][j] = 1;
                }
            }
        }
        all_cell.remove(0);
        p += 1;
    }
    (matrix_as, matrix_xs, matrix_bs, unknow_block)
}

#[pyfunction]
fn cal_possibility(
    board_of_game: Vec<Vec<i32>>,
    mine_num: usize,
) -> PyResult<(Vec<((usize, usize), f64)>, f64)> {
    // 输入局面、未知雷数，返回每一个未知的格子是雷的概率
    // 局面中可以标雷，但必须全部标对
    // 未知雷数为总雷数减去已经标出的雷
    // 若超出枚举长度，那些格子的概率不予返回
    // 输出所有边缘格子是雷的概率和内部未知格子是雷的概率
    // 若没有内部未知区域，返回NaN
    let mut p = vec![];
    let mut table_cell_minenum: Vec<Vec<Vec<usize>>> = vec![]; // 每块每格雷数表：记录了每块每格（或者地位等同的复合格）、每种总雷数下的是雷情况数
    let mut comb_relp_s = vec![]; // 记录了方格的组合关系
    let mut enum_comb_table_s = vec![];
    let mut table_minenum: Vec<[Vec<usize>; 2]> = vec![]; // 每块雷数分布表：记录了每块（不包括内部块）每种总雷数下的是雷总情况数
                                                          // let mut table_t: Vec<usize> = vec![]; // 每块情况总数表：记录了每块总共有几种可能的情况
    let (matrix_as, matrix_xs, matrix_bs, unknow_block) = refresh_matrixs(&board_of_game);
    let block_num = matrix_as.len(); // 整个局面被分成的块数

    for i in 0..block_num {
        let (matrixA_squeeze, matrixx_squeeze, combination_relationship) =
            combine(matrix_as[i].clone(), matrix_xs[i].clone());
        let enum_comb_table = enum_comb(&matrixA_squeeze, &matrixx_squeeze, &matrix_bs[i]);
        if matrixx_squeeze.len() > 60 {  // 这里就是考虑格子等同地位后的枚举极限
            return Ok((vec![], f64::NAN));
        }
        comb_relp_s.push(combination_relationship);
        enum_comb_table_s.push(enum_comb_table);
    }

    // 分块枚举后，根据雷数限制，删除某些情况
    for i in 0..block_num {
        table_cell_minenum.push(vec![]);
        table_minenum.push([vec![], vec![]]);
        for s in enum_comb_table_s[i].clone() {
            let s_sum = s.iter().sum::<usize>();
            let mut si_num = 1;  // 由于enum_comb_table中的格子每一个都代表了与其地位等同的所有格子，由此的情况数
            for s_i in 0..s.len() {
                si_num *= C_usize(comb_relp_s[i][s_i].len(), s[s_i]);
            }
            let fs = table_minenum[i][0].clone().iter().position(|x| *x == s_sum);
            match fs {
                None => {
                    table_minenum[i][0].push(s_sum);
                    table_minenum[i][1].push(si_num);
                    let mut ss = vec![];
                    for c in 0..s.len() {
                        if s[c] == 0 {
                            ss.push(0);
                        } else {
                            let mut sss = 1;
                            for d in 0..s.len() {
                                if c != d {
                                    sss *= C_usize(comb_relp_s[i][d].len(), s[d])
                                }
                            }
                            ss.push(sss);
                        }
                    }
                    table_cell_minenum[i].push(ss);
                }
                _ => {
                    table_minenum[i][1][fs.unwrap()] += si_num;
                    for c in 0..s.len() {
                        if s[c] == 0 {
                            continue;
                        } else {
                            let mut sss = 1;
                            for d in 0..s.len() {
                                if c != d {
                                    sss *= C_usize(comb_relp_s[i][d].len(), s[d])
                                }
                            }
                            table_cell_minenum[i][fs.unwrap()][c] += sss;
                        }
                    }
                }
            }
        }
    } // 第一步，整理出每块每格雷数情况表、每块雷数分布表、每块雷分布情况总数表
    let mut min_num = 0;
    let mut max_num = 0;
    for i in 0..block_num {
        min_num += table_minenum[i][0].iter().min().unwrap();
        max_num += table_minenum[i][0].iter().max().unwrap();
    }
    max_num = min(max_num, mine_num);
    let unknow_mine_num: Vec<usize> = (mine_num - max_num..min(mine_num - min_num, unknow_block) + 1).collect();
    
    // 这里的写法存在极小的风险，例如边缘格雷数分布是0，1，3，而我们直接认为了可能有2
    let mut unknow_mine_s_num = vec![];
    for i in &unknow_mine_num {
        unknow_mine_s_num.push(C(unknow_block, *i));
    }
    // 第二步，整理内部未知块雷数分布表，并筛选。这样内部未知雷块和边缘雷块的地位视为几乎等同，但数据结构不同
    table_minenum.push([unknow_mine_num.clone(), vec![]]);
    // 这里暂时不知道怎么写，目前这样写浪费了几个字节的内存
    // 未知区域的情况数随雷数的分布不能存在表table_minenum中，因为格式不一样，后者是大数类型
    let mut mine_in_each_block = (0..block_num + 1)
        .map(|i| 0..table_minenum[i][0].len())
        .multi_cartesian_product()
        .collect::<Vec<_>>();
    
    for i in (0..mine_in_each_block.len()).rev() {
        let mut total_num = 0;
        for j in 0..block_num + 1 {
            total_num += table_minenum[j][0][mine_in_each_block[i][j]];
        }
        if total_num != mine_num {
            mine_in_each_block.remove(i); 
        }
    }
    // 第三步，枚举每块雷数情况索引表：行代表每种情况，列代表每块雷数的索引，最后一列代表未知区域雷数
    let mut table_minenum_other: Vec<Vec<big_number>> = vec![];
    for i in 0..block_num + 1 {
        table_minenum_other.push(vec![big_number { a: 0.0, b: 0 }; table_minenum[i][0].len()]);
    } // 初始化
    for s in mine_in_each_block {
        for i in 0..block_num {
            let mut s_num = big_number { a: 1.0, b: 0 };
            let mut s_mn = mine_num; // 未知区域中的雷数
            for j in 0..block_num {
                if i != j {
                    s_num.mul_usize(table_minenum[j][1][s[j]]);
                }
                s_mn -= table_minenum[j][0][s[j]];
            }
            let ps = unknow_mine_num.iter().position(|x| *x == s_mn).unwrap();
            s_num.mul_big_number(&unknow_mine_s_num[ps]);
            table_minenum_other[i][s[i]].add_big_number(&s_num);
        }
        let mut s_num = big_number { a: 1.0, b: 0 };
        let mut s_mn = mine_num; // 未知区域中的雷数
        for j in 0..block_num {
            s_num.mul_usize(table_minenum[j][1][s[j]]);
            s_mn -= table_minenum[j][0][s[j]];
        }
        let ps = unknow_mine_num.iter().position(|x| *x == s_mn).unwrap();
        table_minenum_other[block_num][ps].add_big_number(&s_num);
    }
    // 第四步，计算每块其他雷数情况表
    let mut T = big_number { a: 0.0, b: 0 };
    for i in 0..unknow_mine_s_num.len() {
        let mut t = table_minenum_other[block_num][i].clone();
        t.mul_big_number(&unknow_mine_s_num[i]);
        T.add_big_number(&t);
    }
    // 第五步，计算局面总情况数

    for i in 0..block_num {
        for cells_id in 0..comb_relp_s[i].len() {
            let cells_len = comb_relp_s[i][cells_id].len();
            for cell_id in 0..cells_len {
                let mut s_cell = big_number { a: 0.0, b: 0 };
                for s in 0..table_minenum_other[i].len() {
                    let mut o = table_minenum_other[i][s].clone();
                    o.mul_usize(table_cell_minenum[i][s][cells_id]);
                    s_cell.add_big_number(&o);
                }
                let p_cell = s_cell.div_big_num(&T);
                let id = comb_relp_s[i][cells_id][cell_id];
                p.push((matrix_xs[i][id], p_cell));
            }
        }
    }
    
    // 第六步，计算边缘每格是雷的概率
    let mut u_s = big_number { a: 0.0, b: 0 };
    for i in 0..unknow_mine_num.len() {
        let mut u = table_minenum_other[block_num][i].clone();
        u.mul_big_number(&unknow_mine_s_num[i]);
        u.mul_usize(unknow_mine_num[i]);
        u_s.add_big_number(&u);
    }
    let p_unknow = u_s.div_big_num(&T) / unknow_block as f64;
    // 第七步，计算内部未知区域是雷的概率
    Ok((p, p_unknow))
}

#[pyclass]
struct minesweeperBoard {
    // 局面类，分析操作与局面的交互
    #[pyo3(get)]
    board: Vec<Vec<i32>>,
    gameBoard: Vec<Vec<i32>>,
    flagedList: Vec<(usize, usize)>,  //记录哪些雷曾经被标过，则再标这些雷不记为ce
    left: usize,
    right: usize,
    chording: usize,
    ces: usize,
    flag: usize,
    solved3BV: usize,
    Row: usize,
    Column: usize,
    rightFlag: bool,  // 若rightFlag=True，则如果紧接着再chording就要把right减去1
    chordingFlag: bool,  // chordingFlag=True，代表上一个时刻是双击弹起，此时再弹起左键或右键不做任何处理
}

#[pymethods]
impl minesweeperBoard {
    #[new]
    pub fn new(board: Vec<Vec<i32>>) -> minesweeperBoard {
        let Row = board.len();
        let Column = board[0].len();
        minesweeperBoard {
            board: board,
            Row: Row,
            Column: Column,
            gameBoard: vec![vec![10; Column]; Row],
            left: 0,
            right: 0,
            chording: 0,
            ces: 0,
            flag: 0,
            solved3BV: 0,
            rightFlag: false,
            chordingFlag: false,
            flagedList: vec![],
        }
    }
    fn leftClick(&mut self, x: usize, y: usize) {
        self.left += 1;
        if self.gameBoard[x][y] != 10 {
            return;
        }
        match self.board[x][y] {
            0 => {
                self.solved3BV += 1;
                self.ces += 1;
                refreshBoard(&self.board.clone(), &mut self.gameBoard.clone(), vec![(x, y)]);
                return;
            }
            -1 => {
                return;
            }
            _ => {
                refreshBoard(&self.board.clone(), &mut self.gameBoard.clone(), vec![(x, y)]);
                if self.numIs3BV(x, y) {
                    self.solved3BV += 1;
                    self.ces += 1;
                    return;
                }
                else {
                    self.ces += 1;
                    return;
                }
            }
        }
    }
    fn rightClick(&mut self, x: usize, y: usize) {
        self.right += 1;
        if self.gameBoard[x][y] < 10 {
            return;
        }
        else {
            if self.board[x][y] != -1 {
                match self.gameBoard[x][y] {
                    10 => {
                        self.gameBoard[x][y] = 11;
                        self.flag += 1;
                    },
                    11 => {
                        self.gameBoard[x][y] = 10;
                        self.flag -= 1;
                    },
                    _ => return,
                }
                return
            }
            else {
                match self.gameBoard[x][y] {
                    10 => {
                        self.gameBoard[x][y] = 11;
                        self.flag += 1;
                        self.flagedList.push((x, y));
                        let mut not_flag_flaged = true;
                        for flags in self.flagedList.clone() {
                            if x == flags.0 && y == flags.1 {
                                not_flag_flaged = false;
                                break;
                            }
                        }
                        if not_flag_flaged {
                            self.ces += 1;}
                    },
                    11 => {
                        self.gameBoard[x][y] = 10;
                        self.flag -= 1;
                    },
                    _ => return,
                }
                return
            }
        }
    }
    fn chordingClick(&mut self, x: usize, y: usize) {
        self.chording += 1;
        if self.gameBoard[x][y] == 0 || self.gameBoard[x][y] > 8 {
            return
        }
        let mut flagChordingUseful = false; // 双击有效的基础上，周围是否有未打开的格子
        let mut chordingCells = vec![];     // 未打开的格子的集合
        let mut flagedNum = 0;              // 双击点周围的标雷数
        let mut surround3BV = 0;            // 周围的3BV
        for i in max(1, x) - 1..min(self.Row, x + 2) {
            for j in max(1, y) - 1..min(self.Column, y + 2) {
                if i != x || j != y {
                    if self.gameBoard[i][j] == 11 {
                        flagedNum += 1
                    }
                    if self.gameBoard[i][j] == 10 {
                        flagChordingUseful = true;
                        chordingCells.push((i, j));
                        if self.numIs3BV(i, j) {
                            surround3BV += 1;
                        }
                    }
                }
            }
        }
        if flagedNum == self.gameBoard[x][y] && flagChordingUseful {
            self.ces += 1;
            self.solved3BV += surround3BV;
            refreshBoard(&self.board.clone(), &mut self.gameBoard.clone(), chordingCells);
        }
    }
    pub fn numIs3BV(&self, x: usize, y: usize) -> bool {
        // 判断该数字是不是3BV，0也可以
        if self.board[x][y] == 0 {
            return true;
        }
        for i in max(1, x) - 1..min(self.Row, x + 2) {
            for j in max(1, y) - 1..min(self.Column, y + 2) {
                if self.board[i][j] == 0 && (x != i || y != j) {
                    return false;
                }
            }
        }
        true
    }
    pub fn step(&mut self, operation: Vec<(&str, (usize, usize))>) {
        for op in operation {
            match op.0 {
                "c1" => {
                    if self.rightFlag {
                        self.rightFlag = false;
                        self.right -= 1;
                    }
                },
                "l2" => {
                    if self.chordingFlag {
                        self.chordingFlag = false;
                    }
                    else{
                        self.leftClick(op.1.0, op.1.1)
                    }
                },
                "r1" => self.rightClick(op.1.0, op.1.1),
                "c2" => {
                    self.chordingClick(op.1.0, op.1.1);
                    self.chordingFlag = true;
                },
                "r2" => {
                    if self.chordingFlag {
                        self.chordingFlag = false;
                    }
                    self.rightFlag = false;  // 若rightFlag=True，则如果紧接着再chording就要把right减去1
                },
                _ => continue,
            }
        }
    }
    // pub fn reset(&self) {
    //     // 重载，暂时没用不写
    // }
}

#[pyproto]
impl PyObjectProtocol for minesweeperBoard {
    fn __getattr__(&self, name: &str) -> PyResult<usize> {
        match name {
            "left" => return Ok(self.left),
            "right" => return Ok(self.right),
            "chording" => return Ok(self.chording),
            "solved3BV" => return Ok(self.solved3BV),
            "ces" => return Ok(self.ces),
            "flag" => return Ok(self.flag),
            _ => return Ok(999),
        }
    }
}

#[pymodule]
fn ms_toollib(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(py_refreshMatrix, m)?)?;
    m.add_function(wrap_pyfunction!(py_calOp, m)?)?;
    m.add_function(wrap_pyfunction!(py_cal3BV, m)?)?;
    m.add_function(wrap_pyfunction!(py_layMineNumber, m)?)?;
    m.add_function(wrap_pyfunction!(py_refreshBoard, m)?)?;
    m.add_function(wrap_pyfunction!(layMine, m)?)?;
    m.add_function(wrap_pyfunction!(py_SolveMinus, m)?)?;
    m.add_function(wrap_pyfunction!(py_layMineOpNumber, m)?)?;
    m.add_function(wrap_pyfunction!(layMineOp, m)?)?;
    m.add_function(wrap_pyfunction!(py_SolveDirect, m)?)?;
    m.add_function(wrap_pyfunction!(py_SolveEnumerate, m)?)?;
    m.add_function(wrap_pyfunction!(py_unsolvableStructure, m)?)?;
    m.add_function(wrap_pyfunction!(py_isSolvable, m)?)?;
    m.add_function(wrap_pyfunction!(py_enuOneStep, m)?)?;
    m.add_function(wrap_pyfunction!(layMineSolvable, m)?)?;
    m.add_function(wrap_pyfunction!(layMineSolvable_thread, m)?)?;
    m.add_function(wrap_pyfunction!(cal_possibility, m)?)?;
    m.add_class::<minesweeperBoard>()?;
    Ok(())
}
