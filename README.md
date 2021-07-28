# Solvable-Minesweeper

# 黑猫扫雷v2.2.5——包含8种模式的扫雷项目及高性能算法工具箱

[![SolvableMinesweeper](https://img.shields.io/badge/SolvableMinesweeper-v2.2.5-brightgreen.svg)](https://github.com/eee555/Solvable-Minesweeper)

黑猫扫雷v2.2.5是由真正擅长扫雷的玩家开发的扫雷游戏，集中了扫雷游戏的一些现代化设计。内部集成了三大判雷引擎+概率计算引擎，具有全部6种无猜扫雷模式+标准+win7。采用Python/PyQt5及Rust编写，具有很高的内存安全性及速度。不同于Arbiter的专业、Minesweeper X的小巧，黑猫扫雷的开发人员希望制作出一款高度智能的扫雷。外观上它只是一款普通的标准扫雷，但它能任意调大小，能调整窗口的透明度，具有光学局面识别（Optical Board Recognition，OBR）功能。在游戏性方面，弱可猜、强可猜的模式都是独一无二的，也是唯一自带新手教程的扫雷。对于高玩来说，它又是专业的，能够计算3BV/s、STNB、RQP指标并展示。此外，它不会打扰玩家，当玩家不去主动打开时，就不会弹出任何窗口，且任何窗口都可以按下空格键快速关闭。

项目架构方面，游戏与算法高度分离，工具箱同样开源，通过pip install ms_toollib命令即可安装。

目前还在开发过程中，欢迎提意见。

Black Cat Minesweeper v2.2.5, which integrates three major internal mine detection engines, with all six kinds of no-guess minesweeper mode + standard + Win7. Using Python/PyQt5 and Rust, has high safety in memory and speed is different from the Arbiter of professional Minesweeper X of small, black cats demining developers hope to create a cool mine clearance Appearance, it is only a common standard mine, but it can adjust the size at will, can adjust the transparency of the window In terms of gameplay, weak can guess the strong can guess the mode is unique, and the only one of mine own tutorials For high play, it is professional, can calculate 3 bv/s STNBIn addition, it doesn't bother the player, no window pops up when the player doesn't open it, and any window can be quickly closed by pressing the space bar.

+ 使用教程：[https://mp.weixin.qq.com/s/gh9Oxtv9eHaPTUMTDwX-fg](https://mp.weixin.qq.com/s/gh9Oxtv9eHaPTUMTDwX-fg)

+ 其他文档（施工中）：[https://eee555.github.io](https://eee555.github.io)

## 安装
建议在`Windows 10`下运行本游戏，其它操作系统未经测试，可能出现意想不到的问题。

### 通过网盘安装(推荐)
在下面的[下载链接](#下载链接)中找到最新的版本，然后下载，解压，直接运行`main.exe`文件，开箱即用。

### 通过Github Actions安装
在[Github Actions](https://github.com/eee555/Solvable-Minesweeper/actions)找到构建成功的最近一次提交，点击更新内容，在Artifacts页面可以找到打包好的文件，后面步骤同上。这个方法可以体验最新功能，但不保证稳定性。

### 从源码安装(不推荐)
在编译之前，请确保自己拥有：
*   Python 3.7/Python 3.8（**Python 3.9会找不到ms_toollib.pyd**，原因不明）
*   Rust
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

*   用Rust编译扫雷核心引擎
```sh
    cd toollib
    cargo build --release
    cd ..
    cp toollib/target/release/ms_toollib.dll src/ms_toollib.pyd
```

*   将toollib/下的神经网络模型参数文件params.onnx复制、粘贴到main.py同一级目录，即src/

*   运行程序，大功告成了~
```sh
    py -3 src/main.py # Windows
    python3 src/main.py # *nix
```

## 实现原理

（还没写，计划弄出3.5以后回头来写）

## 下载链接

### 正式版v2.2：

算法优化：高级埋雷速度达到37525局/秒，相当于Arbiter的三倍左右，高级无猜局面埋雷速度15.7局/秒。游戏结束按空格可以显示实力指标的极坐标图。删去了一些无用的功能。

链接：[https://wws.lanzoui.com/iq9Ocm8zdtc](https://wws.lanzous.com/iq9Ocm8zdtc)

### 正式版v2.2.5：

算法优化：高级无猜局面埋雷速度达到约252局/秒。修复了上一个版本的严重bug。

链接：[https://wws.lanzoui.com/iS3wImv2y5e](https://wws.lanzous.com/iS3wImv2y5e)

### 测试版v2.2.6-alpha：

修复了若干bug。算法优化：(16,16,72)无猜局面埋雷速度提高200%。新功能：快捷键4、5、6可以快速设置三种不同的自定义的自定义模式。对自定义模式的优化，提高了稳定性。对局面刷新的优化。

链接：[https://wwe.lanzoui.com/igPFFo7mwxi](https://wwe.lanzous.com/igPFFo7mwxi)

### 正式版v2.3：

修复了若干bug。现在可以设置自动重开、自动弹窗、结束后标雷。按住空格键可以计算每格是雷的概率。组合键“Ctrl+空格”可以通过截图+光学局面识别（Optical Board Recognition，OBR）计算每格是雷的概率。

链接：[https://wwe.lanzoui.com/i2axoq686kb](https://wwe.lanzoui.com/i2axoq686kb)

### 正式版v2.3.1：

修复了若干bug。

链接：[https://wwe.lanzoui.com/ifH4Cryp3aj](https://wwe.lanzoui.com/ifH4Cryp3aj)
