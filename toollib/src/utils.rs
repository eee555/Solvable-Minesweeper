use std::cmp::{max, min};
use rand::thread_rng;
use rand::seq::SliceRandom;
use itertools::Itertools;

// 整个模块是最底层的一些小工具，如埋雷、局面分块、计算3BV等



pub fn calOp(mut Board: Vec<Vec<i32>>) -> usize {
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

fn infectBoard(mut Board: Vec<Vec<i32>>, x: usize, y: usize) -> Vec<Vec<i32>> {
    // Board(x, y)位置的整个空都用数字1填满，仅计算Op用
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

pub fn refreshMatrix(BoardofGame: &Vec<Vec<i32>>) -> (Vec<Vec<i32>>, Vec<(usize, usize)>, Vec<i32>) {
    // BoardofGame必须且肯定是正确标雷的游戏局面，但不需要标全
    // 根据游戏局面生成矩阵，不分块。效率低，待改进。
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

pub fn layMineNumber(Row: usize, Column: usize, MineNum: usize, X0: usize, Y0: usize) -> Vec<Vec<i32>> {
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

pub fn layMineOpNumber(Row: usize, Column: usize, MineNum: usize, X0: usize, Y0: usize) -> Vec<Vec<i32>> {
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

pub fn cal3BV(Board: &Vec<Vec<i32>>) -> usize {
    cal3BVonIsland(&Board) + calOp(Board.clone())
}

pub fn refreshBoard(Board: &Vec<Vec<i32>>, BoardofGame: &mut Vec<Vec<i32>>, mut ClickedPoses: Vec<(usize, usize)>) {
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

pub fn sum(v: &Vec<i32>) -> i32 {
    let mut ret = 0;
    for i in v {
        ret += *i;
    }
    ret
}

pub fn refresh_matrixs(
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
    // println!("{:?}", all_cell);
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
                for m in max(1, min(x_t, x_e)) - 1..min(Row, max(x_t + 2, x_e + 2)) {
                    for n in max(1, min(y_t, y_e)) - 1..max(Row, min(y_t + 2, y_e + 2)) {
                        // 貌似xy不对称，不知道为什么，md自己都看不懂
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

#[derive(Clone, Debug)]
pub struct big_number {
    // 科学计数法表示的大数字
    // 必定大于等于1，a必定满足小于10大于等于1
    pub a: f64,
    pub b: i32,
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
    pub fn mul_usize(&mut self, k: usize) {
        // 与usize相乘
        if k == 0 {
            self.a = 0.0;
            self.b = 1;
        } else {
            self.a *= k as f64;
            self.a_become_smaller_than(10.0);
        }
    }
    pub fn mul_big_number(&mut self, k: &big_number) {
        // 与big_number相乘, big_number必须至少为1
        self.a *= k.a;
        self.b += k.b;
        self.a_become_smaller_than(10.0);
    }
    pub fn add_big_number(&mut self, k: &big_number) {
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
    pub fn div_big_num(&mut self, k: &big_number) -> f64 {
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
    pub fn div_usize(&mut self, k: usize) {
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

pub fn C(n: usize, k: usize) -> big_number {
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

pub fn C_usize(n: usize, k: usize) -> usize {
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

pub fn combine(
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

pub fn enum_comb(
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

pub fn enuOneStep(mut AllTable: Vec<Vec<usize>>, TableId: Vec<usize>, b: i32) -> Vec<Vec<usize>> {
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

pub fn unsolvableStructure(BoardCheck: &Vec<Vec<i32>>) -> bool {
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

pub fn cal3BV_exp(Board: &Vec<Vec<i32>>) -> usize {
    // 用于高级局面的3BV
    let mut board = Board.clone();
    let mut op_id = 0;
    let mut op_list = [false; 200];
    let mut bv = 0;
    for x in 0..16 {
        for y in 0..30 {
            if board[x][y] > 0 {
                board[x][y] = 1000000;
                bv += 1;
            } else if board[x][y] == 0 {
                let mut min_op_id = 1000;
                let mut flag_op = false; // 该空周围有无空的标志位
                if x >= 1 {
                    for j in max(1, y) - 1..min(30, y + 2) {
                        if board[x - 1][j] > 999999 {
                            board[x - 1][j] = 1;
                            bv -= 1;
                        } else if Board[x - 1][j] == 0 {
                            if board[x - 1][j] < min_op_id {
                                if flag_op {
                                    op_list[min_op_id as usize] = false;
                                } else {
                                    flag_op = true;
                                }
                                min_op_id = board[x - 1][j];
                            }
                        }
                    }
                }
                if y >= 1 {
                    if board[x][y - 1] > 999999 {
                        board[x][y - 1] = 1;
                        bv -= 1;
                    } else if Board[x][y - 1] == 0 {
                        if board[x][y - 1] < min_op_id {
                            if flag_op {
                                op_list[min_op_id as usize] = false;
                            } else {
                                flag_op = true;
                            }
                            min_op_id = board[x][y - 1];
                        }
                    }
                }
                if !flag_op {
                    op_id += 1;
                    op_list[op_id as usize] = true;
                }
            }
        }
    }
    for x in (0..16).rev() {
        for y in (0..30).rev() {
            if board[x][y] == 0 {
                if x <= 14 {
                    for j in max(1, y) - 1..min(30, y + 2) {
                        if board[x + 1][j] > 999999 {
                            board[x + 1][j] = 1;
                            bv -= 1;
                        } else if Board[x + 1][j] == 0 {
                            if board[x + 1][j] < board[x][y] {
                                op_list[board[x][y] as usize] = false;
                                board[x][y] = board[x + 1][j];
                            }
                        }
                    }
                }
                if y <= 28 {
                    if board[x][y + 1] > 999999 {
                        board[x][y + 1] = 1;
                        bv -= 1;
                    } else if Board[x][y + 1] == 0 {
                        if board[x][y + 1] < board[x][y] {
                            op_list[board[x][y] as usize] = false;
                            board[x][y] = board[x][y + 1];
                        }
                    }
                }
            }
        }
    }
    for i in 0..op_id + 1 {
        if op_list[i] {
            bv += 1;
        }
    }
    bv
}














