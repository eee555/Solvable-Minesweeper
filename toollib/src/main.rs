// 测试判雷引擎、分块算法

use std::cmp::{max, min};
mod OBR;
mod algorithms;
use algorithms::{
    cal_possibility, isSolvable, layMineOp, layMineSolvable_thread, SolveDirect,
    SolveMinus, layMine, layMineSolvable, sample_3BVs_exp, OBR_board,
};
mod utils;
use crate::utils::{
    big_number, cal3BV, cal3BV_exp, combine, enuOneStep, enum_comb, layMineNumber, layMineOpNumber,
    refreshBoard, refreshMatrix, sum, unsolvableStructure, C_usize, C,
};

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
                            all_cell.push((i, j));
                        }
                    }
                }
            } else if board_of_game[i][j] == 10 {  // 数内部有几个格子
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
                for m in max(1, max(x_t, x_e)) - 1..min(Row, min(x_t + 2, x_e + 2)) {
                    for n in max(1, max(y_t, y_e)) - 1..min(Column, min(y_t + 2, y_e + 2)) {
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

pub fn SolveEnumerate(
    matrix_as: &Vec<Vec<Vec<i32>>>,
    matrix_xs: &Vec<Vec<(usize, usize)>>,
    matrix_bs: &Vec<Vec<i32>>,
    BoardofGame: &mut Vec<Vec<i32>>,
    enuLimit: usize,
) -> (Vec<(usize, usize)>, bool) {
    // 第二代枚举法判雷引擎
    // 输入的矩阵都是分块好的
    // 只判断哪些不是雷，不判断哪些是雷，不修改输入进来的局面
    let mut flag = false;
    let mut NotMine = vec![];
    let block_num = matrix_xs.len();
    for i in 0..block_num {
        let a = enum_comb(&matrix_as[i], &matrix_xs[i], &matrix_bs[i]); // a记录了当前块的所有情况
        let cell_num = matrix_xs[i].len();
        'outer: for j in (0..cell_num).rev() {
            for k in 0..a.len() {
                if a[k][j] == 1 {
                    continue'outer;
                }
            }
            NotMine.push(matrix_xs[i][j]);
        }
    }
    (NotMine, flag)
}

fn main() {
    // let game_board = vec![
    //     vec![ 0,  0,  1,  1,  1,  0,  1, -1],
    //     vec![ 0,  1,  2, -1,  2,  1,  1,  1],
    //     vec![ 0,  2, -1,  4,  3, -1,  1,  0],
    //     vec![ 0,  3, -1, -1,  2,  1,  1,  0],
    //     vec![ 0,  3, -1,  4,  2,  1,  1,  0],
    //     vec![ 0,  3, -1,  3,  2, -1,  2,  0],
    //     vec![ 0,  2, -1,  2,  2, -1,  2,  0],
    //     vec![ 0,  1,  1,  1,  1,  1,  1,  0],
    // ];
    let mut game_board = vec![
        vec![ 0,  0,  1, 10, 10, 10, 10, 10],
        vec![ 0,  1,  2, 10, 10, 10, 10, 10],
        vec![ 0,  2, 11, 10, 10, 10, 10, 10],
        vec![ 0,  3, 11, 10, 10, 10, 10, 10],
        vec![ 0,  3, 11,  4,  2, 10, 10, 10],
        vec![ 0,  3, 11,  3,  2, 10, 10, 10],
        vec![ 0,  2, 11,  2,  2, 10, 10, 10],
        vec![ 0,  1,  1,  1,  1, 10, 10, 10],
    ];
   
    let (mut MatrixA, mut Matrixx, mut Matrixb, _) = refresh_matrixs(&game_board);
    let m = SolveEnumerate(&MatrixA, &Matrixx, &Matrixb, &mut game_board, 30);
    println!("{:?}", m);
}


