use std::cmp::{max, min};

// Optical Cell Recognition

pub struct ImageBoard {
    data_vec: Vec<usize>,
    height: usize,
    width: usize,
    data: [Vec<Vec<f32>>; 3],
    r_1: usize,
    r_2: usize,
    c_1: usize,
    c_2: usize,
    r0: usize,
    c0: usize,
    pixelr: f32,
    pixelc: f32,
    pub c: usize,
    pub r: usize,
}
impl ImageBoard {
    pub fn new(data_vec: Vec<usize>, height: usize, width: usize) -> ImageBoard {
        let mut d: [Vec<Vec<f32>>; 3] = [
            vec![vec![0.0; width]; height],
            vec![vec![0.0; width]; height],
            vec![vec![0.0; width]; height],
        ];
        let c: [usize; 3] = [2, 1, 0];
        for k in 0..3 {
            for i in 0..height {
                for j in 0..width {
                    d[k][i][j] = data_vec[(i * width + j) * 4 + c[k]] as f32 / 255.0;
                }
            }
        }
        ImageBoard {
            data_vec: data_vec,
            height: height,
            width: width,
            data: d,
            r_1: 0,
            r_2: 0,
            c_1: 0,
            c_2: 0,
            r0: 0,
            c0: 0,
            pixelr: 0.0,
            pixelc: 0.0,
            c: 0,
            r: 0,
        }
    }
    pub fn extra_save_cell(&self, x: usize, y: usize, size: usize) -> Vec<f32> {
        // 抽取每个cell的彩色像素数据，size为边长
        let mut cell: Vec<f32> = vec![0.0; size * size * 3];
        for k in 0..3 {
            for i in 0..size {
                for j in 0..size {
                    cell[k * size * size + i * size + j] = self.data[k][(self.r_1 as f32
                        + self.r0 as f32
                        + self.pixelr * x as f32
                        + self.pixelr / 2.0 / size as f32 * (i as f32 * 2.0 + 1.0))
                        as usize][(self.c_1 as f32
                        + self.c0 as f32
                        + self.pixelc * y as f32
                        + self.pixelc / 2.0 / size as f32 * (j as f32 * 2.0 + 1.0))
                        as usize];
                }
            }
        }
        cell
    }
    pub fn get_gradient(&self) -> Vec<Vec<f32>> {
        // println!("{:?}", self.data[0].len());
        let row = self.data[0].len() - 2;
        let column = self.data[0][0].len() - 2;
        let mut x_bw = vec![vec![0.0; column]; row];
        // println!("{:?}", self.data[0].len());
        for i in 0..row {
            for j in 0..column {
                for k in 0..3 {
                    let g = -self.data[k][i][j] - self.data[k][i][j + 1] - self.data[k][i][j + 2]
                        + self.data[k][i + 2][j]
                        + self.data[k][i + 2][j + 1]
                        + self.data[k][i + 2][j + 2];
                    x_bw[i][j] = if x_bw[i][j] > g.abs() {
                        x_bw[i][j]
                    } else {
                        g.abs()
                    };
                    let g = -self.data[k][i][j] - self.data[k][i + 1][j] - self.data[k][i + 2][j]
                        + self.data[k][i][j + 2]
                        + self.data[k][i + 1][j + 2]
                        + self.data[k][i + 2][j + 2];
                    x_bw[i][j] = if x_bw[i][j] > g.abs() {
                        x_bw[i][j]
                    } else {
                        g.abs()
                    };
                }
            }
        }
        x_bw
    }
    fn get_r12c12(&self, x_bw2: &Vec<Vec<bool>>) -> [usize; 8] {
        let row = x_bw2.len();
        let column = x_bw2[0].len();
        let mut r_1 = row / 2;
        let mut r_2 = row / 2;
        let mut c_1 = column / 2;
        let mut c_2 = column / 2;
        let c_p_1 = column / 3;
        let c_p_2 = column * 2 / 3;
        let r_p_1 = row / 3;
        let r_p_2 = row * 2 / 3;
        let mut c = c_1;
        let mut flag_break = false;
        let mut r_pos = r_p_1;
        loop {
            if c == 0 {
                c_1 = 0;
                break;
            }
            if x_bw2[r_pos][c - 1] {
                c -= 1;
                continue;
            } else {
                let mut flag_continue = false;
                for skip in 1..4 {
                    if c <= skip {
                        c_1 = c;
                        flag_break = true; // 发现都是0了
                        break;
                    }
                    let mut ss = 0;
                    for n in r_p_1..r_p_2 {
                        if x_bw2[n][c - skip] {
                            ss += 1;
                            if ss >= 5 {
                                c -= skip;
                                r_pos = n;
                                flag_continue = true;
                                break; // 跨到一半发现了两个1，就跨过去
                            }
                        }
                    }
                    if flag_continue {
                        break;
                    }
                }
                if flag_continue {
                    continue;
                }
                if flag_break {
                    break;
                } else {
                    c_1 = c; // 顺利跨完5格
                    break;
                }
            }
        }

        c = c_2;
        flag_break = false;
        r_pos = r_p_1;
        while c <= column - 1 {
            if c == column - 1 {
                c_2 = column - 1;
                break;
            }
            if x_bw2[r_pos][c + 1] {
                c += 1;
                continue;
            } else {
                let mut flag_continue = false;
                for skip in 1..4 {
                    if c + skip == column - 1 {
                        c_2 = c;
                        flag_break = true; // 发现都是0了
                        break;
                    }
                    let mut ss = 0;
                    for n in r_p_1..r_p_2 {
                        if x_bw2[n][c + skip] {
                            ss += 1;
                            if ss >= 5 {
                                c += skip;
                                r_pos = n;
                                flag_continue = true;
                                break; // 跨到一半发现了两个1，就跨过去
                            }
                        }
                    }
                    if flag_continue {
                        break;
                    }
                }
                if flag_continue {
                    continue;
                }
                if flag_break {
                    break;
                } else {
                    c_2 = c; // 顺利跨完5格
                    break;
                }
            }
        }
        //////////

        let mut r = r_1;
        flag_break = false;
        let mut c_pos = c_p_1;
        loop {
            if r == 0 {
                r_1 = 0;
                break;
            }
            if x_bw2[r - 1][c_pos] {
                r -= 1;
                continue;
            } else {
                let mut flag_continue = false;
                for skip in 1..4 {
                    if r <= skip {
                        r_1 = r;
                        flag_break = true; // 发现都是0了
                        break;
                    }
                    let mut ss = 0;
                    for n in c_p_1..c_p_2 {
                        if x_bw2[r - skip][n] {
                            ss += 1;
                            if ss >= 5 {
                                r -= skip;
                                c_pos = n;
                                flag_continue = true;
                                break; // 跨到一半发现了两个1，就跨过去
                            }
                        }
                    }
                    if flag_continue {
                        break;
                    }
                }
                if flag_continue {
                    continue;
                }
                if flag_break {
                    break;
                } else {
                    r_1 = r; // 顺利跨完5格
                    break;
                }
            }
        }

        r = r_2;
        flag_break = false;
        c_pos = c_p_1;
        while r <= row - 1 {
            if r == row - 1 {
                r_2 = row - 1;
                break;
            }
            if x_bw2[r + 1][c_pos] {
                r += 1;
                continue;
            } else {
                let mut flag_continue = false;
                for skip in 1..4 {
                    if r + skip == row - 1 {
                        r_2 = r;
                        flag_break = true; // 发现都是0了
                        break;
                    }
                    let mut ss = 0;
                    for n in c_p_1..c_p_2 {
                        if x_bw2[r + skip][n] {
                            ss += 1;
                            if ss >= 5 {
                                r += skip;
                                c_pos = n;
                                flag_continue = true;
                                break; // 跨到一半发现了两个1，就跨过去
                            }
                        }
                    }
                    if flag_continue {
                        break;
                    }
                }
                if flag_continue {
                    continue;
                }
                if flag_break {
                    break;
                } else {
                    r_2 = r; // 顺利跨完5格
                    break;
                }
            }
        }
        [r_1, r_2, c_1, c_2, r_p_1, r_p_2, c_p_1, c_p_2]
    }

    fn binarize_gradient(&self, x: &Vec<Vec<f32>>) -> Vec<Vec<bool>> {
        let row = x.len();
        let column = x[0].len();
        let mut xx = vec![vec![false; column]; row];
        let mut ss = vec![];
        for i in (row / 4)..(row * 3 / 4) {
            for j in (column / 4)..(column * 3 / 4) {
                ss.push(x[i][j]);
            }
        }
        ss.sort_by(|a, b| a.partial_cmp(b).unwrap()); // 浮点数从小到大排序
        let mut th1 = ss[(ss.len() as f32 * 0.55) as usize];
        if th1 > 1.0 {
            th1 = 1.0;
        } else if th1 < 0.01 {
            th1 = 0.01;
        }
        for i in 0..row {
            for j in 0..column {
                if x[i][j] >= th1 {
                    xx[i][j] = true;
                }
            }
        }
        xx
    }

    fn narrow(&mut self, K: usize) {
        // 用中值滤波，按比例缩小self.data（因为过高的分辨率影响识别）,K为2、3等
        let row = self.data[0].len() / K;
        let column = self.data[0][0].len() / K;
        let mut x_bw: [Vec<Vec<f32>>; 3] = [
            vec![vec![0.0; column]; row],
            vec![vec![0.0; column]; row],
            vec![vec![0.0; column]; row],
        ];
        let mut KK = vec![0.0; K * K];
        let MID = (K * K) / 2;
        for k in 0..3 {
            for i in 0..row {
                for j in 0..column {
                    let mut pos = 0;
                    for ii in i * K..(i + 1) * K {
                        for jj in j * K..(j + 1) * K {
                            KK[pos] = self.data[k][ii][jj];
                            pos += 1;
                        }
                    }
                    KK.sort_by(|a, b| a.partial_cmp(b).unwrap());
                    x_bw[k][i][j] = KK[MID];
                }
            }
        }
        self.data = x_bw;
        self.height = self.data[0].len();
        self.width = self.data[0][0].len();
    }

    fn get_c_sum(
        &self,
        data: &Vec<Vec<bool>>,
        mut dis: [usize; 5],
        c_1: usize,
        c_2: usize,
        r_1: usize,
        r_2: usize,
    ) -> [usize; 5] {
        // c_1, c_2左闭右闭
        let mut dis_ = dis;
        for i in r_1 + 1..r_2 + 1 {
            dis_ = dis;
            dis_[0] = min(
                dis[0] + (1 - data[i][c_1] as usize),
                dis[1] + (1 - data[i][c_1 + 1] as usize) + 1,
            );
            for j in c_1 + 1..c_2 {
                dis_[j - c_1] = min(
                    min(
                        dis[j - c_1] + (1 - data[i][j] as usize),
                        dis[j - c_1 - 1] + (1 - data[i][j - 1] as usize) + 1,
                    ),
                    dis[j - c_1 + 1] + (1 - data[i][j + 1] as usize) + 1,
                );
            }
            dis_[c_2 - c_1] = min(
                dis[c_2 - c_1] + (1 - data[i][c_2] as usize),
                dis[c_2 - c_1 - 1] + (1 - data[i][c_2 - 1] as usize) + 1,
            );
            dis = dis_
        }
        dis_
    }

    fn get_r_sum(
        &self,
        data: &Vec<Vec<bool>>,
        mut dis: [usize; 5],
        c_1: usize,
        c_2: usize,
        r_1: usize,
        r_2: usize,
    ) -> [usize; 5] {
        // r_1, r_2左闭右闭
        let mut dis_ = dis;
        for i in c_1 + 1..c_2 + 1 {
            dis_ = dis;
            dis_[0] = min(
                dis[0] + (1 - data[r_1][i] as usize),
                dis[1] + (1 - data[r_1 + 1][i] as usize) + 1,
            );
            for j in r_1 + 1..r_2 {
                dis_[j - r_1] = min(
                    min(
                        dis[j - r_1] + (1 - data[j][i] as usize),
                        dis[j - r_1 - 1] + (1 - data[j - 1][i] as usize) + 1,
                    ),
                    dis[j - r_1 + 1] + (1 - data[j + 1][i] as usize) + 1,
                );
            }
            dis_[r_2 - r_1] = min(
                dis[r_2 - r_1] + (1 - data[r_2][i] as usize),
                dis[r_2 - r_1 - 1] + (1 - data[r_2 - 1][i] as usize) + 1,
            );
            dis = dis_;
        }
        return dis_;
    }

    fn get_line(&self, x: Vec<usize>) -> (f32, usize, usize) {
        // 找线
        let lenx = x.len();
        let mut xsort = x.clone();
        xsort.sort();
        let th = (xsort[(0.85 * lenx as f32) as usize] as f32 + xsort[lenx - 1] as f32 * 0.75) / 2.0;

        let mut xx = vec![0; lenx];
        xx[0] = x[0];
        xx[1] = x[1];
        xx[2] = x[2];
        xx[3] = x[3];
        xx[lenx - 1] = x[lenx - 1];
        xx[lenx - 2] = x[lenx - 2];
        xx[lenx - 3] = x[lenx - 3];
        xx[lenx - 4] = x[lenx - 4];
        for i in 4..lenx - 4 {
            xx[i] = max(
                x[i],
                min(
                    max(max(x[i - 4], x[i - 3]), max(x[i - 2], x[i - 1])),
                    max(max(x[i + 1], x[i + 2]), max(x[i + 3], x[i + 4])),
                ),
            );
        }
        let mut lines = vec![];
        for i in 0..lenx {
            if xx[i] as f32 >= th {
                let mut left = 0;
                let mut right = 0;
                let mut max_flag = true;
                let mut max_num = xx[i];
                for j in max(7, i)-7..i {
                    if xx[j] >= xx[i] {
                        left += 1;
                    }
                    if xx[j] > max_num {
                        max_flag = false;
                        break;
                    }
                }
                for j in i + 1..min(lenx, i + 8) {
                    if xx[j] >= xx[i] {
                        right += 1;
                    }
                    if xx[j] > max_num {
                        max_flag = false;
                        break;
                    }
                }
                if max_flag && (left == right || left == right - 1) {
                    lines.push(i)
                }
            }
        }
        let mut delta = vec![];
        let lineslen = lines.len();
        for i in 1..lineslen {
            let dd = lines[i] - lines[i - 1];
            if dd > 5 {
                delta.push(dd);
            }
        }
        delta.sort();
        let size_est = delta[(delta.len() as f32 * 0.4) as usize];

        if (lines[1] - lines[0]) as f32 <= size_est as f32 * 0.8 {
            lines.remove(0);
        }
        let lineslen = lines.len();
        if (lines[lineslen - 1] - lines[lineslen - 2]) as f32 <= size_est as f32 * 0.8 {
            lines.remove(lineslen - 1);
        }
        let lineslen = lines.len();

        // 针对清晰度高的大图，采用霍夫变换定位
        let max_size = min(200, size_est + 5);
        let min_size = max(8, size_est - 5);

        let max_x = lines[0] + 7; // 最大的空的格子像素数
        let mut hough = vec![vec![0; max_size * 4 + 1]; max_x + 1];
        // 方格边长精度为像素的1/4
        for L in &lines {
            for y in min_size * 4..max_size * 4 + 1 {
                for n in L / max_size..L / min_size + 1 {
                    // let x_ = L - n * y / 4;
                    if n * y / 4 <= *L  && *L <= max_x + n * y / 4 {
                        // let x_ = L - n * y / 4;
                        hough[L - n * y / 4][y] += 1;
                    }
                    if n * y / 4 <= *L + 1 && *L + 1 <= max_x + n * y / 4 {
                        // let x_ = L - n * y / 4;
                        // println!("{:?}", *L);
                        // println!("{:?}", n * y / 4);
                        hough[*L + 1 - n * y / 4][y] += 1;
                    }
                }
            }
        }
        let mut max_num = 0;
        let mut max_i = 0;
        let mut max_j = 0;
        for i in 0..max_x + 1 {
            for j in min_size * 4..max_size * 4 + 1 {
                if hough[i][j] > max_num {
                    max_i = i;
                    max_j = j;
                    max_num = hough[i][j];
                }
            }
        }
        let N = ((lines[lineslen - 1] - lines[0] + 2) as f32 / (max_j as f32 / 4.0)) as usize;
        (max_j as f32 / 4.0, max_i, N)
    }

    pub fn get_pos_pixel(&mut self) {
        let mut x = self.data.clone();
        let mut row = x[0].len() - 2;
        let mut column = x[0][0].len() - 2;
        // LoG算子,Prewitt算子,Sobel算子
        let mut x_bw2 = self.get_gradient();
        let x_bw3 = self.binarize_gradient(&x_bw2);

        let [mut r_1, mut r_2, mut c_1, mut c_2, mut r_p_1, mut r_p_2, mut c_p_1, mut c_p_2] =
            self.get_r12c12(&x_bw3);
        while r_2 - r_1 <= row / 3 || c_2 - c_1 <= column / 3 {
            self.narrow(3);
            x_bw2 = self.get_gradient();
            let x_bw3 = self.binarize_gradient(&x_bw2);
            let [r_1_, r_2_, c_1_, c_2_, r_p_1_, r_p_2_, c_p_1_, c_p_2_] = self.get_r12c12(&x_bw3);
            r_1 = r_1_;
            r_2 = r_2_;
            c_1 = c_1_;
            c_2 = c_2_;
            r_p_1 = r_p_1_;
            r_p_2 = r_p_2_;
            c_p_1 = c_p_1_;
            c_p_2 = c_p_2_;
            row = self.data[0].len() - 2;
            column = self.data[0][0].len() - 2;
            if row <= 64 || column <= 64 {
                return;
            }
        }

        // println!("{:?}", self.data[0].len());
        // println!("{:?}", self.data[0][0].len());
        // println!("{:?}", x_bw2.len());
        // println!("{:?}", x_bw2[0].len());
        // println!("{:?}", x_bw3.len());
        // println!("{:?}", x_bw3[0].len());

        for c in (1..c_1 + 1).rev() {
            let mut ss = 0;
            for r in r_p_1..r_p_2 {
                ss += x_bw3[r][c] as i32;
                ss += x_bw3[r - 1][c] as i32;
                if ss > 2 {
                    break;
                }
            }
            if ss <= 2 {
                c_1 = c;
                break;
            }
            c_1 = c;
        }

        for c in c_2..column - 1 {
            let mut ss = 0;
            for r in r_p_1..r_p_2 {
                ss += x_bw3[r][c] as i32;
                ss += x_bw3[r][c + 1] as i32;
                if ss > 2 {
                    break;
                }
            }
            if ss <= 2 {
                c_2 = c;
                break;
            }
            c_2 = c;
        }

        for r in (1..r_1 + 1).rev() {
            let mut ss = 0;
            for c in c_p_1..c_p_2 {
                ss += x_bw3[r][c] as i32;
                ss += x_bw3[r - 1][c] as i32;
                if ss > 2 {
                    break;
                }
            }
            if ss <= 2 {
                r_1 = r;
                break;
            }
            r_1 = r
        }

        for r in r_2..row - 1 {
            let mut ss = 0;
            for c in c_p_1..c_p_2 {
                ss += x_bw3[r][c] as i32;
                ss += x_bw3[r + 1][c] as i32;
                if ss > 2 {
                    break;
                }
            }
            if ss <= 2 {
                r_2 = r;
                break;
            }
            r_2 = r;
        }

        let mut c_sum = vec![];
        c_sum.push(r_2 - r_1 - self.get_c_sum(&x_bw3, [0, 1, 2, 3, 4], c_1, c_1 + 4, r_1, r_2)[0]);
        c_sum.push(r_2 - r_1 - self.get_c_sum(&x_bw3, [1, 0, 1, 2, 3], c_1, c_1 + 4, r_1, r_2)[1]);
        for c in c_1..c_2 - 4 {
            c_sum.push(r_2 - r_1 - self.get_c_sum(&x_bw3, [2, 1, 0, 1, 2], c, c + 4, r_1, r_2)[2]);
        }
        c_sum.push(r_2 - r_1 - self.get_c_sum(&x_bw3, [3, 2, 1, 0, 1], c_2 - 4, c_2, r_1, r_2)[3]);
        c_sum.push(r_2 - r_1 - self.get_c_sum(&x_bw3, [4, 3, 2, 1, 0], c_2 - 4, c_2, r_1, r_2)[4]);

        let mut r_sum = vec![];
        r_sum.push(c_2 - c_1 - self.get_r_sum(&x_bw3, [0, 1, 2, 3, 4], c_1, c_2, r_1, r_1 + 4)[0]);
        r_sum.push(c_2 - c_1 - self.get_r_sum(&x_bw3, [1, 0, 1, 2, 3], c_1, c_2, r_1, r_1 + 4)[1]);
        for r in r_1..r_2 - 4 {
            r_sum.push(c_2 - c_1 - self.get_r_sum(&x_bw3, [2, 1, 0, 1, 2], c_1, c_2, r, r + 4)[2]);
        }
        r_sum.push(c_2 - c_1 - self.get_r_sum(&x_bw3, [3, 2, 1, 0, 1], c_1, c_2, r_2 - 4, r_2)[3]);
        r_sum.push(c_2 - c_1 - self.get_r_sum(&x_bw3, [4, 3, 2, 1, 0], c_1, c_2, r_2 - 4, r_2)[4]);

        let (pixelc, c0, c) = self.get_line(c_sum);
        let (pixelr, r0, r) = self.get_line(r_sum);
        self.pixelc = pixelc;
        self.c0 = c0;
        self.c = c;
        self.pixelr = pixelr;
        self.r0 = r0;
        self.r = r;
        self.c_1 = c_1;
        self.r_1 = r_1;
    }
}
