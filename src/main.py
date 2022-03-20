# from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtWidgets
import sys
import mainWindowGUI as mainWindowGUI
import mineSweeperGUI as mineSweeperGUI
# import os
# sys.path.append(os.path.realpath('.'))


if __name__ == "__main__":
    # appctxt = ApplicationContext()   # 1. Instantiate ApplicationContext
    app = QtWidgets.QApplication (sys.argv)
    # app.aboutToQuit.connect(app.deleteLater)
    mainWindow = mainWindowGUI.MainWindow()
    ui = mineSweeperGUI.MineSweeperGUI(mainWindow)
    mainWindow.show()
    # exit_code = appctxt.app.exec_()  # 2. Invoke appctxt.app.exec_()
    sys.exit(app.exec_())

#    雷密度较大时，生成无猜局面采用自适应的鲁棒“快速模式”
#    生成极端bv局面时采用鲁棒的“快速模式”，仅对标准模式有效？
#    “高级设置”中增加可选择的无猜局面算法（筛选算法或修改算法）
#    快速给出多变量方程的一个解的算法
#    加入AI模式
#    自动重开、自动弹成绩、获胜弹成绩等可选的功能


# 局面标记的约定：
# 其中0代表空；1到8代表数字1到8；10代表未打开；11代表玩家或算法确定是雷；12代表算法确定不是雷；
# 14表示踩到了雷游戏失败以后显示的标错的雷对应叉雷，15表示踩到了雷游戏失败了对应红雷；
# 16表示白雷
# 18表示局面中，由于双击的高亮，导致看起来像0的格子

# 游戏模式的约定：
# 0，1，2，3，4，5，6，7代表：标准、win7、竞速无猜、强无猜、弱无猜、准无猜、强可猜、弱可猜

# 局面状态的约定：
# 'ready'：预备状态。表示局面完全没有左键点过，可能被右键标雷；刚打开或点脸时进入这种状态。
#         此时可以改雷数、改格子大小（ctrl+滚轮）、行数、列数（拖拉边框）。
# 'study': 研究状态。截图后进入。应该设计第二种方式进入研究状态，没想好。
# 'show': 展示智能分析结果，按住空格进入。
# 'modify': 调整状态。'ready'下，拖拉边框时进入，拖拉结束后自动转为'ready'。
# 'playing': 正在游戏状态、标准模式、不筛选3BV、且没有看概率计算结果，游戏结果是official的。 
# 'joking': 正在游戏状态，游戏中看过概率计算结果，游戏结果不是official的。
# 'fail': 游戏失败，踩雷了。
# 'win': 游戏成功。
# 'display':正在播放录像。 








