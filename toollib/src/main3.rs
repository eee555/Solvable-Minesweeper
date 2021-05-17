// 急速埋雷+算3BV，比较垃圾，304761局/s
use async_std::task::block_on;
use futures::join;
use rand::seq::SliceRandom;
use rand::thread_rng;
use std::cmp::{max, min};
use std::thread;
use std::time::Instant;

fn sample_3BVs_exp(X0: usize, Y0: usize, n: usize) -> [usize; 382] {
    // 适用范围：高级
    let n0 = n / 8;
    let mut threads = vec![];
    for i in 0..8 {
        let join_item = thread::spawn(move || -> [usize; 382] { lay_mine_number_study_exp(X0, Y0, n0) });
        threads.push(join_item);
    }

    let mut aa = [0; 382];
    for i in threads.into_iter().map(|c| c.join().unwrap()) {
        // aa.extend(i);
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
        bv_record[cal3BV(&Board)] += 1;
    }
    bv_record
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

fn cal3BV_old(Board: &Vec<Vec<i32>>) -> usize {
    cal3BVonIsland(&Board) + calOp(Board.clone())
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

fn cal3BV(Board: &Vec<Vec<i32>>) -> usize {
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
                if x <= 16 - 2 {
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
                if y <= 30 - 2 {
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
    // println!("{:?}", bv);
    for i in 0..op_id + 1 {
        if op_list[i] {
            bv += 1;
        }
    }
    // println!("{:?}", bv);
    // println!("{:?}", Board);
    bv
}

fn main() {
    let start = Instant::now();
    let ans = sample_3BVs_exp(5, 5, 800000);
    for i in 0..382 {
        println!("{}: {:?}", i, ans[i]);
    }
    println!("time cost: {:?} ms", start.elapsed().as_millis()); // ms
}
