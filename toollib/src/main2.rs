// 测试神经网络

use rand::seq::SliceRandom;
use rand::thread_rng;
// use pyo3::PyTraverseError;
use itertools::Itertools;
use std::cmp::max;
use std::cmp::min;
use std::sync::mpsc;
use std::sync::{Arc, Mutex};
use std::thread;
mod algorithms;
use algorithms::{
    cal_possibility, isSolvable, layMineOp, layMineSolvable_thread, SolveDirect, SolveEnumerate,
    SolveMinus, layMine, layMineSolvable, sample_3BVs_exp, OBR_board,
};
use std::fs::File;
use std::io::{BufReader,BufRead};
use std::io::prelude::*;
use std::{error, result};
mod utils;
mod OBR;

type AError = Box<dyn error::Error>;
type TResult<T> = result::Result<T, AError>;
fn get_csv(s: &String) -> TResult<Vec<f64>> {
    s.split(',').map(|x|x.parse::<f64>().map_err(|e|e.into())).collect()
}
fn example() -> Vec<usize> {
    let mut data = vec![];
    let file = File::open("frame.csv").unwrap();
    for line in BufReader::new(file).lines() {
        data.push(get_csv(&line.unwrap()).unwrap());
    }
    let mut datas = vec![];
    for i in 0..data.len() {
        datas.push(data[i][0] as usize);
    }
    // println!("{:?}", datas);
    datas
    
}

// #[allow(clippy::upper_case_acronyms)]
fn main() {
   
    let data_vec = example();

    // println!("{:?}", ans.0);
    // println!("{:?}", ans.1);
    let m = OBR_board(data_vec, 306, 673).unwrap();
    println!("{:?}", m);
}
