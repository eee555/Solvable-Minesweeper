extern crate ms_toollib;
use ms_toollib::cal_is_op_possibility_cells;


#[test]
fn cal_is_op_possibility_cells_works() {
    let game_board = vec![
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10,  3, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
        vec![10, 10, 10, 10, 10, 10, 10, 10],
    ];
    // let a = vec![[0usize, 0usize]];
    let ans = cal_is_op_possibility_cells(&game_board, 10.0, &vec![[0usize, 0usize]]);
    print!("{:?}", ans)
}


