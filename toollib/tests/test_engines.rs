use ms_toollib::refresh_matrixs;
use ms_toollib::{cal_is_op_possibility_cells, SolveEnumerate, cal_possibility_onboard, cal_possibility};

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
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 1, 1, 1, 10, 10, 10],
        vec![10, 10, 1, 0, 1, 10, 10, 10],
        vec![10, 10, 1, 1, 1, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 11, 10, 10, 10, 10, 10],
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


