# MetaSweeper-v3.0 —— project with 8 modes of minesweeper, third generation minesweeper video player and high performance algorithm toolbox

# 元扫雷v3.0 —— 包含8种模式的扫雷项目、第三代扫雷录像播放器及高性能算法工具箱

[![SolvableMinesweeper](https://img.shields.io/badge/SolvableMinesweeper-v2.2.5-brightgreen.svg)](https://github.com/eee555/Solvable-Minesweeper)

## 简介(Introduction)

元扫雷v3.0是由热爱扫雷的玩家开发的扫雷游戏。这个项目并非简单重复已有的工作，而是集中了一批扫雷游戏的现代化设计。内部集成了三大判雷引擎+概率计算引擎+光学局面识别（Optical Board Recognition，OBR）引擎，具有全部6种无猜扫雷模式+标准+win7。采用Python/PyQt5及Rust编写，兼顾开发速度、内存安全与执行速度。不同于Arbiter的强调检查作弊、FreeSweeper的强调统计、Minesweeper X的小巧，元扫雷的开发人员希望制作出一款高度智能的扫雷。外观上它只是一款普通的标准扫雷，但它能通过按住ctrl并滚动滚轮任意调整大小，能调整窗口的透明度，能够计算局面中每一格是雷的概率，设置能截屏识别计算其他扫雷中每一格是雷的概率。其装载的录像播放器可以分析录像的高层抽象特征，并实时展示游戏局面中每一格是雷的概率。在游戏性方面，弱可猜、强可猜的模式都是独一无二的，也是唯一自带新手教程的扫雷。对于高玩来说，它又是专业的，能够计算3BV/s、STNB、RQP指标并展示。此外，它不会打扰玩家，当玩家不去主动打开时，就不会弹出任何窗口，且任何窗口都可以按下空格键快速关闭。

项目架构方面，游戏界面与算法高度分离，自研的工具箱同样开源，且遵循更为宽松的MIT协议，通过pip install ms_toollib命令即可安装。

目前属于漫长的开发阶段中，约1~3月更新一个版本，欢迎提意见。

MetaSweeper V3.0 is a minesweeper game developed by players who love minesweeper. Rather than simply repeating existing work, the project brought together a collection of modern designs for minesweeper games. Internal integration of three mine-detection engine + probability calculation engine + Optical Board Recognition (OBR) engine, with all six no guess mode + standard + Win7. Written in Python/PyQt5 and Rust, it gives consideration to development speed, memory safety and execution speed. Different from Arbiter's emphasis on checking cheating, FreeSweeper's emphasis on statistics, Minesweeper X's small, MetaSweeper developers hope to produce a highly intelligent Minesweeper. It looks like a normal standard minesweeper, but it can be resized by holding Down CTRL and scrolling through the wheel, it can adjust the transparency of the window, it can calculate the probability of whether each cell being a mine, and it can calculate the probability of whether each cell being a mine for other minesweeper by screen shot. The video player can analyze high-level abstract features of the video and show the probability of whether each cell being a mine in real time. In terms of gameplay, the weak guess and strong guess modes are unique and the only minesweeper with its own tutorial. For high play, it is also professional, able to calculate 3BV/s, STNB, RQP metrics and display. In addition, it doesn't bother the player, no window pops up when the player doesn't open it, and any window can be quickly closed by pressing the space bar.

### 开发计划

计划开发：

- 各种扫雷相关的算法，性能达到极佳。
- 智能的录像播放器、智能的局面数据导入导出工具。
- 能计算是雷概率、开空概率的局面分析工具。
- 用户体验好的全模式无猜扫雷。
- 多种语言的切换。

而不会开发：

- 移动端的扫雷。
- 在本地记录个人纪录的功能。
- 安装程序和启动界面。
- 扫雷游戏以外的游戏、无猜模式以外的扫雷模式。
- 非标准且花哨的ui、任何多余且匪夷所思的选项。
- 任何防止在本软件作弊以取得异常成绩的设计。
- 任何用于在其他软件作弊以取得异常短的时间的成绩的设计。
- 扫码收费以解锁某功能的功能。

+ 使用教程：[https://mp.weixin.qq.com/s/gh9Oxtv9eHaPTUMTDwX-fg](https://mp.weixin.qq.com/s/gh9Oxtv9eHaPTUMTDwX-fg)

+ 其他文档（施工中）：[https://eee555.github.io](https://eee555.github.io)
+ 算法工具箱地址：[https://github.com/eee555/ms_toollib](https://github.com/eee555/ms_toollib)
+ 算法工具箱文档：[https://docs.rs/ms_toollib](https://docs.rs/ms_toollib)

## 安装
建议在`Windows 10`下运行本游戏，其它操作系统未经测试，可能出现意想不到的问题。

### 通过网盘安装(推荐)
在下面的[下载链接](#下载链接)中找到最新的版本，然后下载，解压，直接运行`main.exe`文件，开箱即用。

### 通过Github Actions安装(最安全)
在[Github Actions](https://github.com/eee555/Solvable-Minesweeper/actions)找到构建成功的最近一次提交，点击更新内容，在Artifacts页面可以找到打包好的文件，后面步骤同上。这个方法可以体验最新功能，能保证软件绿色安全无毒，但未发布的版本都不能保证稳定性。

### 从源码安装(不推荐)
在编译之前，请确保自己拥有：
*   Python 3.7/Python 3.8
*   会用Powershell或者其它命令行工具的能力

以下为安装步骤：
*   克隆这个仓库到本地
```sh
    git clone https://github.com/eee555/Solvable-Minesweeper.git
```

*   安装Python依赖
```sh
    pip install -r requirements.txt # Windows
    pip3 install -r requirements.txt # *nix
```

*   运行程序，大功告成了~
```sh
    py -3 src/main.py # Windows
    python3 src/main.py # *nix
```

## 实现原理

（还没写，计划弄出3.5以后回头来写）

## 下载链接

### 正式版v3.0.1：
修复了两个bug。现在可以将元扫雷设置为arbiter的avf文件的默认打开方式。  
链接：[https://wwb.lanzouw.com/iHaNm02ane7c](https://wwb.lanzouw.com/iHaNm02ane7c)

### 正式版v3.0：
修复了一些bug。黑猫扫雷更名为元扫雷（MetaSweeper）。首次装载第三代录像播放器，能够播放avf录像。分析出并报告抽象的录像事件。录像播放时，按下空格键可以实时地展示每格是雷的概率。  
链接：[https://wwb.lanzouw.com/i8ypL026p1za](https://wwb.lanzouw.com/i8ypL026p1za)

### 正式版v2.4.2：
软件整体重构。修复了若干bug。ui界面开始采用矢量贴图。游戏开始前，按住ctrl并滚动滚轮可以缩放界面；对雷数滚动滚轮可以调整雷数。预告：即将升级到3.0，从3.0开始，黑猫扫雷将更名为元扫雷（Meta Sweeper）。  
链接：[https://wwb.lanzouw.com/i3Bpc01vfsab](https://wwb.lanzouw.com/i3Bpc01vfsab)

### 正式版v2.4.1：
修复了若干bug。部分优化的ui界面。光学局面识别引擎开始支持自定义局面。  
链接：[https://wwe.lanzoui.com/i5Sswsq0uva](https://wwe.lanzoui.com/i5Sswsq0uva)

### 正式版v2.3.1：
修复了若干bug。  
链接：[https://wwe.lanzoui.com/ifH4Cryp3aj](https://wwe.lanzoui.com/ifH4Cryp3aj)

### 正式版v2.3：
修复了若干bug。现在可以设置自动重开、自动弹窗、结束后标雷。按住空格键可以计算每格是雷的概率。组合键“Ctrl+空格”可以通过截图+光学局面识别（Optical Board Recognition，OBR）计算每格是雷的概率。  
链接：[https://wwe.lanzoui.com/i2axoq686kb](https://wwe.lanzoui.com/i2axoq686kb)

### 测试版v2.2.6-alpha：
修复了若干bug。算法优化：(16,16,72)无猜局面埋雷速度提高200%。新功能：快捷键4、5、6可以快速设置三种不同的自定义的自定义模式。对自定义模式的优化，提高了稳定性。对局面刷新的优化。  
链接：[https://wwe.lanzoui.com/igPFFo7mwxi](https://wwe.lanzous.com/igPFFo7mwxi)

### 正式版v2.2.5：
算法优化：高级无猜局面埋雷速度达到约252局/秒。修复了上一个版本的严重bug。  
链接：[https://wws.lanzoui.com/iS3wImv2y5e](https://wws.lanzous.com/iS3wImv2y5e)  

### 正式版v2.2：
算法优化：高级埋雷速度达到37525局/秒，相当于Arbiter的三倍左右，高级无猜局面埋雷速度15.7局/秒。游戏结束按空格可以显示实力指标的极坐标图。删去了一些无用的功能。  
链接：[https://wws.lanzoui.com/iq9Ocm8zdtc](https://wws.lanzous.com/iq9Ocm8zdtc)


