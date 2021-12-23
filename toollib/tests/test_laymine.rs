use ms_toollib::refresh_matrixs;
use ms_toollib::{layMineSolvable_thread, layMineSolvable};

// 测试各种埋雷类的函数

#[test]
fn layMineSolvable_thread_works() {
    // 测试多线程筛选法无猜埋雷
    let game_board = layMineSolvable_thread(16, 30, 99, 0, 0, 0, 1000, 100000, 40);
    game_board.0.iter().for_each(|i| println!("{:?}", i));
    print!("{:?}", game_board.1);
}

#[test]
fn layMineSolvable_works() {
    // 测试筛选法无猜埋雷
    let game_board = layMineSolvable(8, 8, 20, 0, 0, 0, 1000, 100000, 40);
    game_board.0.iter().for_each(|i| println!("{:?}", i));
    print!("{:?}", game_board.1);
}



