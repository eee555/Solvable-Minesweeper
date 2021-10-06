use ms_toollib::{refresh_matrixs, refresh_matrix, combine, cal_table_minenum_recursion};
use ms_toollib::{cal_is_op_possibility_cells, SolveEnumerate, cal_possibility_onboard, cal_possibility, isSolvable};

// 测试各种引擎类的函数

#[test]
fn cal_is_op_possibility_cells_works() {
    // 测试开空概率计算函数
    let game_board = vec![
        vec![10, 10,  1,  1, 10,  1,  0,  0],
        vec![10, 10,  1, 10, 10,  3,  2,  1],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10,  2, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
    ];
    let ans = cal_is_op_possibility_cells(&game_board, 20.0, &vec![[0, 0], [1, 1], [1, 6], [7, 2]]);
    print!("{:?}", ans)
}

#[test]
fn solve_enumerate_works() {
    // 测试枚举判雷引擎
    let mut game_board = vec![
        vec![0, 0, 1, 10, 10, 10, 10, 10],
        vec![0, 0, 2, 10, 10, 10, 10, 10],
        vec![1, 1, 3, 11, 10, 10, 10, 10],
        vec![10, 10, 4, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
    ];
    let (matrix_as, matrix_xs, matrix_bs, _, _) = refresh_matrixs(&game_board);
    let ans = SolveEnumerate(&matrix_as, &matrix_xs, &matrix_bs, &mut game_board, 30);
    print!("{:?}", ans)
}


#[test]
fn cal_possibility_onboard_works() {
    // 测试概率计算引擎
    let game_board = vec![
        vec![10, 10,  1,  1, 10,  1,  0,  0],
        vec![10, 10,  1, 10, 10,  3,  2,  1],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10,  2, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
    ];
    let ans = cal_possibility(&game_board, 10.0);
    let ans = cal_possibility(&game_board, 0.15625);
    print!("{:?}", ans)
}

#[test]
fn cal_table_minenum_recursion_works() {
    // 测试递归枚举引擎
//     [[0, 0, 1, -1, 2, 1, 1, -1], [0, 0, 2, 3, -1, 3, 3, 2], [1, 1, 3, -1, 4, -1, -1, 2], [2, -1, 4, -1, 3, 4, -1, 4], [3, -1, 5, 2, 1, 3, -1, -1], [3, -1, -1, 2, 1, 2, -1, 3], [-1, 5, 4, -1, 
// 1, 1, 2, 2], [-1, 3, -1, 2, 1, 0, 1, -1]]
    let board = vec![
        vec![0, 0, 1, -1, 2, 1, 1, -1],
        vec![0, 0, 2, 3, -1, 3, 3, 2],
        vec![1, 1, 3, -1, 4, -1, -1, 2],
        vec![2, -1, 4, -1, 3, 4, -1, 4],
        vec![3, -1, 5, 2, 1, 3, -1, -1],
        vec![3, -1, -1, 2, 1, 2, -1, 3],
        vec![-1, 5, 4, -1, 1, 1, 2, 2],
        vec![-1, 3, -1, 2, 1, 0, 1, -1],
    ];
    let game_board = vec![
        vec![0, 0, 1, 10, 10, 10, 10, 10],
        vec![0, 0, 2, 10, 10, 10, 10, 10],
        vec![1, 1, 3, 11, 10, 10, 10, 10],
        vec![10, 10, 4, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
    ];
    // let a = isSolvable(&board, 0, 0, 40);
    // print!("{:?}", a);
    let (matrix_a, matrix_x, matrix_b) = refresh_matrix(&game_board);
    let (matrix_a_s, matrix_x_s, combination_relationship) = combine(&matrix_a, &matrix_x);
    let table = cal_table_minenum_recursion(&matrix_a_s, &matrix_x_s, &matrix_b, &combination_relationship);
    println!("table的结果为：{:?}", table);
}
