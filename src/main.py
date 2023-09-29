# from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtWidgets
import sys
import mainWindowGUI as mainWindowGUI
import mineSweeperGUI as mineSweeperGUI


if __name__ == "__main__":
    app = QtWidgets.QApplication (sys.argv)
    mainWindow = mainWindowGUI.MainWindow()
    ui = mineSweeperGUI.MineSweeperGUI(mainWindow, sys.argv)
    ui.mainWindow.show()
    ui.mainWindow.game_setting_path = ui.game_setting_path
    sys.exit(app.exec_())
    ...
    

# 最高优先级
# 校验校验和模块
# 计时器快捷键切换
# 可信的历史记录
# 选择某些国家报错，布维岛(难复现)
# self.label.ms_board.step('rr', (i, j))报错
# 强可猜点之间位置出错（不确定，需要跟踪）
# self.predefinedBoardPara相关的设计还不够好
# OBR修改局面还会报错的情况（不确定，需要跟踪）
# 将鼠标速度调成小数倍

# 次优先级
# 自定义模式弹窗
# 有概率没扫完就win(难复现)
# 记录pop的读写改到ui后

# 最低优先级
# 优化判雷引擎


# 局面标记的约定：
# 其中0代表空；1到8代表数字1到8；10代表未打开；11代表玩家或算法确定是雷；12代表算法确定不是雷；
# 14表示踩到了雷游戏失败以后显示的标错的雷对应叉雷，15表示踩到了雷游戏失败了对应红雷；
# 16表示白雷
# 18表示局面中，由于双击的高亮，导致看起来像0的格子

# 游戏模式的约定：
# 0，4, 5, 6, 7, 8, 9, 10代表：标准0、win74、竞速无猜5、强无猜6、弱无猜7、准无猜8、强可猜9、弱可猜10

# 局面状态的约定：
# 'ready'：预备状态。表示局面完全没有左键点过，可能被右键标雷；刚打开或点脸时进入这种状态。
#         此时可以改雷数、改格子大小（ctrl+滚轮）、行数、列数（拖拉边框）。
# 'study': 研究状态。截图后进入。应该设计第二种方式进入研究状态，没想好。
# 'show': 游戏中，展示智能分析结果，按住空格进入。
# 'modify': 调整状态。'ready'下，拖拉边框时进入，拖拉结束后自动转为'ready'。
# 'playing': 正在游戏状态、标准模式、不筛选3BV、且没有看概率计算结果，游戏结果是official的。
# 'joking': 正在游戏状态，游戏中看过概率计算结果，游戏结果不是official的。
# 'fail': 游戏失败，踩雷了。
# 'win': 游戏成功。
# 'jofail': 游戏失败，游戏结果不是official的。
# 'jowin': 游戏成功，游戏结果不是official的。
# 'display':正在播放录像。
# 'showdisplay':正在一边播放录像、一边看概率。播放录像时按空格进入。

# 指标命名：
# 游戏静态类：race_designator, mode
# 游戏动态类：rtime, left, right, double，cl，left_s，right_s, double_s, cl_s, path, 
#           flag, flag_s
# 录像动态类：etime, stnb, rqp, qg, ioe, thrp, corr, ce, ce_s, bbbv_solved, 
#           bbbv_s, (op_solved), (isl_solved)
# 录像静态类：bbbv，op, isl, cell0, cell1, cell2, cell3, cell4, cell5, cell6,
#           cell7, cell8, fps, (hizi)
# 其他类：checksum_ok, race_designator, mode



