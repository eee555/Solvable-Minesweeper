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
use rayon::prelude::*;
use std::sync::mpsc;


fn refreshMatrix(BoardofGame: &Vec<Vec<i32>>) -> (Vec<Vec<i32>>, Vec<(usize, usize)>, Vec<i32>) {
    // BoardofGame必须且肯定是正确标雷的游戏局面，但不需要标全
    // 根据游戏局面生成矩阵
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

fn quick_sort(cells: &mut Vec<usize>, left: usize, right: usize) {
    // Vec<usize>的快速排序，从大到小
    if left >= right {
        return;
    }
    let mut l = left;
    let mut r = right;
    while l < r {
        while l < r && cells[r] <= cells[left] {
            r -= 1;
        }
        
        while l < r && cells[l] >= cells[left] {
            l += 1;
        }
        cells.swap(l, r);
    }
    cells.swap(left, l);
    if l > 1 {
        quick_sort(cells, left, l - 1);
    }
    quick_sort(cells, r + 1, right);
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
    let len = max(IsMineRel.len(), 1) - 1;
    quick_sort(&mut IsMineRel, 0, len);
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
    let len = max(DelId.len(), 1) - 1;
    quick_sort(&mut DelId, 0, len);
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
    m.add_class::<minesweeperBoard>()?;
    Ok(())
}
