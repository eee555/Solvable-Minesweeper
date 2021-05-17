use crate::utils::{
    big_number, cal3BV, combine, enuOneStep, enum_comb, layMineNumber, layMineOpNumber,
    refreshBoard, refreshMatrix, refresh_matrixs, sum, unsolvableStructure, C_usize, C, cal3BV_exp
};
use itertools::Itertools;
use std::cmp::{max, min};
use std::sync::mpsc;
use std::sync::{Arc, Mutex};
use std::thread;
use rand::seq::SliceRandom;
use rand::thread_rng;

// 中高级的算法，例如无猜埋雷、判雷引擎、计算概率
// 文件结构是algorithms单方面引用utils，但暂时把所有文件写在同一个目录内，以后分开

pub fn SolveMinus(
    MatrixA: &Vec<Vec<i32>>,
    Matrixx: &Vec<(usize, usize)>,
    Matrixb: &Vec<i32>,
    BoardofGame: &mut Vec<Vec<i32>>,
) -> (Vec<(usize, usize)>, bool) {
    let mut flag = false;
    let mut NotMine = vec![];
    let mut NotMineRel = vec![];
    let mut IsMineRel = vec![];
    let mut MatrixColumn = Matrixx.len();
    let mut MatrixRow = Matrixb.len();
    if MatrixRow <= 1 {
        return (NotMine, false);
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
                } else if MatrixA[i][k] - MatrixA[j][k] == -1 {
                    ADvaln1.push(k)
                }
            }
            if FlagAdj {
                let bDval = Matrixb[i] - Matrixb[j];
                if ADval1.len() as i32 == bDval {
                    IsMineRel.append(&mut ADval1);
                    NotMineRel.append(&mut ADvaln1);
                } else if ADvaln1.len() as i32 == -bDval {
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

pub fn SolveDirect(
    MatrixA: &mut Vec<Vec<i32>>,
    Matrixx: &mut Vec<(usize, usize)>,
    Matrixb: &mut Vec<i32>,
    BoardofGame: &mut Vec<Vec<i32>>,
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
                        } else {
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
        if Matrixb[i] == 0 {
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

pub fn cal_possibility(
    board_of_game: Vec<Vec<i32>>,
    mine_num: usize,
) -> (Vec<((usize, usize), f64)>, f64) {
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
        if matrixx_squeeze.len() > 60 {
            // 这里就是考虑格子等同地位后的枚举极限
            return (vec![], f64::NAN);
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
            let mut si_num = 1; // 由于enum_comb_table中的格子每一个都代表了与其地位等同的所有格子，由此的情况数
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
    let unknow_mine_num: Vec<usize> =
        (mine_num - max_num..min(mine_num - min_num, unknow_block) + 1).collect();
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
    (p, p_unknow)
}


pub fn layMineOp(
    Row: usize,
    Column: usize,
    MineNum: usize,
    X0: usize,
    Y0: usize,
    Min3BV: usize,
    Max3BV: usize,
    MaxTimes: usize,
    method: usize,
) -> (Vec<Vec<i32>>, Vec<usize>) {
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
            return (Board, Parameters);
        }
    }
    Parameters.push(0);
    Parameters.push(Num3BV);
    Parameters.push(Times);
    (Board, Parameters)
}

pub fn SolveEnumerate(
    MatrixA: &Vec<Vec<i32>>,
    Matrixx: &Vec<(usize, usize)>,
    Matrixb: &Vec<i32>,
    BoardofGame: &mut Vec<Vec<i32>>,
    enuLimit: usize,
) -> (Vec<(usize, usize)>, bool) {
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
            } else {
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

fn isVictory(BoardofGame: &Vec<Vec<i32>>, Board: &Vec<Vec<i32>>) -> bool {
    // 判断当前是否获胜
    // 游戏局面中必须没有标错的雷
    // 这个函数不具备普遍意义
    let Row = BoardofGame.len();
    let Col = BoardofGame[0].len();
    for i in 0..Row {
        for j in 0..Col {
            if BoardofGame[i][j] == 10 && Board[i][j] != -1 {
                return false;
            }
        }
    }
    return true;
}

pub fn isSolvable(Board: &Vec<Vec<i32>>, X0: usize, Y0: usize, enuLimit: usize) -> bool {
    // 从指定位置开始扫，判断局面是否无猜
    // 周围一圈都是雷，那么中间是雷不算猜，中间不是雷算猜
    if unsolvableStructure(&Board) {
        //若包含不可判雷结构，则不是无猜
        return false;
    }
    let Row = Board.len();
    let Column = Board[0].len();
    let mut BoardofGame = vec![vec![10; Column]; Row];
    // 10是未打开，11是标雷
    // 局面大小必须超过6*6
    refreshBoard(&Board, &mut BoardofGame, vec![(X0, Y0)]);
    if isVictory(&BoardofGame, &Board) {
        return true; // 暂且认为点一下就扫开也是可以的
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
                    return false;
                }
            }
        }
        refreshBoard(&Board, &mut BoardofGame, NotMine);
        if isVictory(&BoardofGame, &Board) {
            return true;
        }
    }
}

pub fn layMineSolvable_thread(
    Row: usize,
    Column: usize,
    MineNum: usize,
    X0: usize,
    Y0: usize,
    Min3BV: usize,
    Max3BV: usize,
    mut MaxTimes: usize,
    enuLimit: usize,
) -> (Vec<Vec<i32>>, [usize; 3]) {
    // 多线程埋雷无猜
    let mut parameters = [0, 0, 0];
    let mut game_board = vec![vec![0; Column]; Row];
    let mut handles = vec![];
    let flag_exit = Arc::new(Mutex::new(0));
    let (tx, rx) = mpsc::channel(); // mpsc 是多个发送者，一个接收者
    for ii in (1..11).rev() {
        let tx_ = mpsc::Sender::clone(&tx);
        let max_time = MaxTimes / ii;
        MaxTimes -= max_time;
        let flag_exit = Arc::clone(&flag_exit);
        let handle = thread::spawn(move || {
            let mut Num3BV;
            let mut counter = 0;
            let mut Board = vec![vec![0; Column]; Row];
            let mut para = [0, 0, 0];
            while counter < max_time {
                {
                    let f = flag_exit.lock().unwrap();
                    if *f == 1 {
                        break;
                    }
                } // 这块用花括号控制生命周期
                let Board_ = layMineOpNumber(Row, Column, MineNum, X0, Y0);
                counter += 1;
                if isSolvable(&Board_, X0, Y0, enuLimit) {
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
    (game_board, parameters)
}

pub fn layMineSolvable(
    Row: usize,
    Column: usize,
    MineNum: usize,
    X0: usize,
    Y0: usize,
    Min3BV: usize,
    Max3BV: usize,
    MaxTimes: usize,
    enuLimit: usize,
) -> (Vec<Vec<i32>>, Vec<usize>) {
    // 3BV下限、上限，最大尝试次数，返回是否成功。
    // 若不成功返回最后生成的局面（不一定无猜），默认尝试十万次
    let mut Times = 0;
    let mut Parameters = vec![];
    let mut Board;
    let mut Num3BV;
    while Times < MaxTimes {
        Board = layMineOpNumber(Row, Column, MineNum, X0, Y0);
        Times += 1;
        if isSolvable(&Board, X0, Y0, enuLimit) {
            Num3BV = cal3BV(&Board);
            if Num3BV >= Min3BV && Num3BV <= Max3BV {
                Parameters.push(1);
                Parameters.push(Num3BV);
                Parameters.push(Times);
                return (Board, Parameters);
            }
        }
    }
    Board = layMineOpNumber(Row, Column, MineNum, X0, Y0);
    Num3BV = cal3BV(&Board);
    Parameters.push(0);
    Parameters.push(Num3BV);
    Parameters.push(Times);
    (Board, Parameters)
}


pub fn layMine(
    Row: usize,
    Column: usize,
    MineNum: usize,
    X0: usize,
    Y0: usize,
    Min3BV: usize,
    Max3BV: usize,
    MaxTimes: usize,
    method: usize,
) -> (Vec<Vec<i32>>, Vec<usize>) {
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
            return (Board, Parameters);
        }
    }
    Parameters.push(0);
    Parameters.push(Num3BV);
    Parameters.push(Times);
    (Board, Parameters)
}

pub fn sample_3BVs_exp(X0: usize, Y0: usize, n: usize) -> [usize; 382] {
    // 从标准高级中采样计算3BV
    // 16线程计算
    let n0 = n / 16;
    let mut threads = vec![];
    for i in 0..16 {
        let join_item = thread::spawn(move || -> [usize; 382] { lay_mine_number_study_exp(X0, Y0, n0) });
        threads.push(join_item);
    }
    let mut aa = [0; 382];
    for i in threads.into_iter().map(|c| c.join().unwrap()) {
        for ii in 0..382 {
            aa[ii] += i[ii];
        }
    }
    aa
}

fn lay_mine_number_study_exp(X0: usize, Y0: usize, n: usize) -> [usize; 382] {
    // 专用埋雷并计算3BV引擎，用于研究
    let mut rng = thread_rng();
    // let area: usize = 16 * 30 - 1;
    let pointer = X0 + Y0 * 16;
    let mut bv_record = [0; 382];
    for id in 0..n {
        let mut Board1Dim = [0; 479];
        for i in 380..479 {
            Board1Dim[i] = -1;
        }

        Board1Dim.shuffle(&mut rng);
        let mut Board1Dim_2 = [0; 480];
        // Board1Dim_2.reserve(area + 1);

        for i in 0..pointer {
            Board1Dim_2[i] = Board1Dim[i];
        }
        Board1Dim_2[pointer] = 0;
        for i in pointer..479 {
            Board1Dim_2[i + 1] = Board1Dim[i];
        }
        let mut Board: Vec<Vec<i32>> = vec![vec![0; 30]; 16];
        for i in 0..480 {
            if Board1Dim_2[i] < 0 {
                let x = i % 16;
                let y = i / 16;
                Board[x][y] = -1;
                for j in max(1, x) - 1..min(16, x + 2) {
                    for k in max(1, y) - 1..min(30, y + 2) {
                        if Board[j][k] >= 0 {
                            Board[j][k] += 1;
                        }
                    }
                }
            }
        }
        bv_record[cal3BV_exp(&Board)] += 1;
    }
    bv_record
}








