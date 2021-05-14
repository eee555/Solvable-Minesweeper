use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
// use pyo3::PyTraverseError;
use pyo3::class::basic::PyObjectProtocol;
use std::cmp::{max, min};
// use rayon::prelude::*;

mod utils;
use utils::{
    cal3BV, calOp, enuOneStep, layMineNumber, layMineOpNumber, refreshBoard, refreshMatrix,
    unsolvableStructure,
};
mod algorithms;
use algorithms::{
    cal_possibility, isSolvable, layMineOp, layMineSolvable_thread, SolveDirect, SolveEnumerate,
    SolveMinus, layMine, layMineSolvable
};

// 负责rust和python之间的接口，类似文档

#[pyfunction]
fn py_refreshMatrix(
    BoardofGame: Vec<Vec<i32>>,
) -> PyResult<(Vec<Vec<i32>>, Vec<(usize, usize)>, Vec<i32>)> {
    Ok(refreshMatrix(&BoardofGame))
}

#[pyfunction]
fn py_calOp(mut Board: Vec<Vec<i32>>) -> PyResult<usize> {
    Ok(calOp(Board))
}

#[pyfunction]
fn py_layMineNumber(
    Row: usize,
    Column: usize,
    MineNum: usize,
    X0: usize,
    Y0: usize,
) -> PyResult<Vec<Vec<i32>>> {
    // 通用标准埋雷引擎
    // 输出为二维的局面
    Ok(layMineNumber(Row, Column, MineNum, X0, Y0))
}

#[pyfunction]
fn py_cal3BV(Board: Vec<Vec<i32>>) -> PyResult<usize> {
    Ok(cal3BV(&Board))
}

#[pyfunction]
fn py_SolveMinus(
    mut MatrixA: Vec<Vec<i32>>,
    mut Matrixx: Vec<(usize, usize)>,
    mut Matrixb: Vec<i32>,
    mut BoardofGame: Vec<Vec<i32>>,
) -> PyResult<(Vec<Vec<i32>>, Vec<(usize, usize)>, bool)> {
    let (notMine, flag) = SolveMinus(&mut MatrixA, &mut Matrixx, &mut Matrixb, &mut BoardofGame);
    Ok((BoardofGame, notMine, flag))
}

#[pyfunction]
fn py_refreshBoard(
    board: Vec<Vec<i32>>,
    mut BoardofGame: Vec<Vec<i32>>,
    ClickedPoses: Vec<(usize, usize)>,
) -> PyResult<Vec<Vec<i32>>> {
    refreshBoard(&board, &mut BoardofGame, ClickedPoses);
    Ok(BoardofGame)
}

#[pyfunction]
fn py_SolveDirect(
    mut MatrixA: Vec<Vec<i32>>,
    mut Matrixx: Vec<(usize, usize)>,
    mut Matrixb: Vec<i32>,
    mut BoardofGame: Vec<Vec<i32>>,
) -> PyResult<(Vec<Vec<i32>>, Vec<(usize, usize)>, bool)> {
    let (notMine, flag) = SolveDirect(&mut MatrixA, &mut Matrixx, &mut Matrixb, &mut BoardofGame);
    Ok((BoardofGame, notMine, flag))
}

#[pyfunction]
fn py_layMineOpNumber(
    Row: usize,
    Column: usize,
    MineNum: usize,
    X0: usize,
    Y0: usize,
) -> PyResult<Vec<Vec<i32>>> {
    Ok(layMineOpNumber(Row, Column, MineNum, X0, Y0))
}

#[pyfunction(enuLimit = 30)]
fn py_SolveEnumerate(
    MatrixA: Vec<Vec<i32>>,
    Matrixx: Vec<(usize, usize)>,
    Matrixb: Vec<i32>,
    mut BoardofGame: Vec<Vec<i32>>,
    enuLimit: usize,
) -> PyResult<(Vec<Vec<i32>>, Vec<(usize, usize)>, bool)> {
    let (notMine, flag) = SolveEnumerate(&MatrixA, &Matrixx, &Matrixb, &mut BoardofGame, enuLimit);
    Ok((BoardofGame, notMine, flag))
}

#[pyfunction]
fn py_enuOneStep(
    AllTable: Vec<Vec<usize>>,
    TableId: Vec<usize>,
    b: i32,
) -> PyResult<Vec<Vec<usize>>> {
    Ok(enuOneStep(AllTable, TableId, b))
}

#[pyfunction]
fn py_unsolvableStructure(BoardCheck: Vec<Vec<i32>>) -> PyResult<bool> {
    Ok(unsolvableStructure(&BoardCheck))
}

#[pyfunction(enuLimit = 30)]
fn py_isSolvable(Board: Vec<Vec<i32>>, X0: usize, Y0: usize, enuLimit: usize) -> PyResult<bool> {
    Ok(isSolvable(&Board, X0, Y0, enuLimit))
}

#[pyfunction(Min3BV = 0, Max3BV = 1000_000, MaxTimes = 1000_000, method = 0)]
pub fn py_layMineOp(
    Row: usize,
    Column: usize,
    MineNum: usize,
    X0: usize,
    Y0: usize,
    Min3BV: usize,
    Max3BV: usize,
    MaxTimes: usize,
    method: usize,
) -> PyResult<(Vec<Vec<i32>>, Vec<usize>)> {
    Ok(layMineOp(
        Row, Column, MineNum, X0, Y0, Min3BV, Max3BV, MaxTimes, method,
    ))
}

#[pyfunction(Min3BV = 0, Max3BV = 1000000, MaxTimes = 1000000, enuLimit = 30)]
pub fn py_layMineSolvable(
    Row: usize,
    Column: usize,
    MineNum: usize,
    X0: usize,
    Y0: usize,
    Min3BV: usize,
    Max3BV: usize,
    MaxTimes: usize,
    method: usize,
) -> PyResult<(Vec<Vec<i32>>, Vec<usize>)> {
    Ok(layMineSolvable(
        Row, Column, MineNum, X0, Y0, Min3BV, Max3BV, MaxTimes, method,
    ))
}

#[pyfunction(Min3BV = 0, Max3BV = 1000_000, MaxTimes = 1000_000, method = 0)]
pub fn py_layMine(
    Row: usize,
    Column: usize,
    MineNum: usize,
    X0: usize,
    Y0: usize,
    Min3BV: usize,
    Max3BV: usize,
    MaxTimes: usize,
    method: usize,
) -> PyResult<(Vec<Vec<i32>>, Vec<usize>)> {
    Ok(layMine(
        Row, Column, MineNum, X0, Y0, Min3BV, Max3BV, MaxTimes, method,
    ))
}

#[pyfunction(Min3BV = 0, Max3BV = 1000000, MaxTimes = 1000000, enuLimit = 30)]
pub fn py_layMineSolvable_thread(
    Row: usize,
    Column: usize,
    MineNum: usize,
    X0: usize,
    Y0: usize,
    Min3BV: usize,
    Max3BV: usize,
    mut MaxTimes: usize,
    enuLimit: usize,
) -> PyResult<(Vec<Vec<i32>>, [usize; 3])> {
    Ok(layMineSolvable_thread(
        Row, Column, MineNum, X0, Y0, Min3BV, Max3BV, MaxTimes, enuLimit,
    ))
}

#[pyfunction]
fn py_cal_possibility(
    board_of_game: Vec<Vec<i32>>,
    mine_num: usize,
) -> PyResult<(Vec<((usize, usize), f64)>, f64)> {
    Ok(cal_possibility(board_of_game, mine_num))
}

#[pyclass]
struct minesweeperBoard {
    // 局面类，分析操作与局面的交互
    #[pyo3(get)]
    board: Vec<Vec<i32>>,
    gameBoard: Vec<Vec<i32>>,
    flagedList: Vec<(usize, usize)>, //记录哪些雷曾经被标过，则再标这些雷不记为ce
    left: usize,
    right: usize,
    chording: usize,
    ces: usize,
    flag: usize,
    solved3BV: usize,
    Row: usize,
    Column: usize,
    rightFlag: bool,    // 若rightFlag=True，则如果紧接着再chording就要把right减去1
    chordingFlag: bool, // chordingFlag=True，代表上一个时刻是双击弹起，此时再弹起左键或右键不做任何处理
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
                refreshBoard(
                    &self.board.clone(),
                    &mut self.gameBoard.clone(),
                    vec![(x, y)],
                );
                return;
            }
            -1 => {
                return;
            }
            _ => {
                refreshBoard(
                    &self.board.clone(),
                    &mut self.gameBoard.clone(),
                    vec![(x, y)],
                );
                if self.numIs3BV(x, y) {
                    self.solved3BV += 1;
                    self.ces += 1;
                    return;
                } else {
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
        } else {
            if self.board[x][y] != -1 {
                match self.gameBoard[x][y] {
                    10 => {
                        self.gameBoard[x][y] = 11;
                        self.flag += 1;
                    }
                    11 => {
                        self.gameBoard[x][y] = 10;
                        self.flag -= 1;
                    }
                    _ => return,
                }
                return;
            } else {
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
                            self.ces += 1;
                        }
                    }
                    11 => {
                        self.gameBoard[x][y] = 10;
                        self.flag -= 1;
                    }
                    _ => return,
                }
                return;
            }
        }
    }
    fn chordingClick(&mut self, x: usize, y: usize) {
        self.chording += 1;
        if self.gameBoard[x][y] == 0 || self.gameBoard[x][y] > 8 {
            return;
        }
        let mut flagChordingUseful = false; // 双击有效的基础上，周围是否有未打开的格子
        let mut chordingCells = vec![]; // 未打开的格子的集合
        let mut flagedNum = 0; // 双击点周围的标雷数
        let mut surround3BV = 0; // 周围的3BV
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
            refreshBoard(
                &self.board.clone(),
                &mut self.gameBoard.clone(),
                chordingCells,
            );
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
                }
                "l2" => {
                    if self.chordingFlag {
                        self.chordingFlag = false;
                    } else {
                        self.leftClick(op.1 .0, op.1 .1)
                    }
                }
                "r1" => self.rightClick(op.1 .0, op.1 .1),
                "c2" => {
                    self.chordingClick(op.1 .0, op.1 .1);
                    self.chordingFlag = true;
                }
                "r2" => {
                    if self.chordingFlag {
                        self.chordingFlag = false;
                    }
                    self.rightFlag = false; // 若rightFlag=True，则如果紧接着再chording就要把right减去1
                }
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
    m.add_function(wrap_pyfunction!(py_layMine, m)?)?;
    m.add_function(wrap_pyfunction!(py_SolveMinus, m)?)?;
    m.add_function(wrap_pyfunction!(py_layMineOpNumber, m)?)?;
    m.add_function(wrap_pyfunction!(py_layMineOp, m)?)?;
    m.add_function(wrap_pyfunction!(py_SolveDirect, m)?)?;
    m.add_function(wrap_pyfunction!(py_SolveEnumerate, m)?)?;
    m.add_function(wrap_pyfunction!(py_unsolvableStructure, m)?)?;
    m.add_function(wrap_pyfunction!(py_isSolvable, m)?)?;
    m.add_function(wrap_pyfunction!(py_enuOneStep, m)?)?;
    m.add_function(wrap_pyfunction!(py_layMineSolvable, m)?)?;
    m.add_function(wrap_pyfunction!(py_layMineSolvable_thread, m)?)?;
    m.add_function(wrap_pyfunction!(py_cal_possibility, m)?)?;
    m.add_class::<minesweeperBoard>()?;
    Ok(())
}
