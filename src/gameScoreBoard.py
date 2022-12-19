# 左侧计时器
import configparser
import minesweeper_master as mm
import ms_toollib as ms
from ui.ui_score_board import Ui_Form
from ui.uiComponents import RoundQWidget
from safe_eval import safe_eval
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import QTimer

class ui_Form(Ui_Form):
    # barSetMineNum = QtCore.pyqtSignal(int)
    # barSetMineNumCalPoss = QtCore.pyqtSignal(int)
    def __init__(self, pix_size):
        self.pix_size = pix_size
        self.QWidget = RoundQWidget()
        self.setupUi(self.QWidget)
        
        self.tableWidget.setColumnWidth(0, 80)
        self.tableWidget.setColumnWidth(1, 120)
        self.tableWidget.verticalHeader().setDefaultSectionSize(24)
        # self.setParameter ()
    
    def show(self, index_value_list: list[str]):
        # 更新数值,指标数量不变
        for idx in range(self.tableWidget.rowCount()):
            self.tableWidget.setItem(idx, 1, QTableWidgetItem(index_value_list[idx]))
        
        
    def reshow(self, index_name_list: list[str], index_value_list: list[str]):
        # 更新数值、指标。指标数量可能变
        table_height = len(index_name_list)*24
        self.tableWidget.setRowCount(len(index_name_list))
        self.tableWidget.setGeometry(QtCore.QRect(12, 50, 200+2,
                                                  table_height+len(index_name_list)+2))
        self.QWidget.setMinimumSize(QtCore.QSize(224+2, table_height + 88))
        self.QWidget.setMaximumSize(QtCore.QSize(224+2, table_height + 88))
        for idx, i in enumerate(index_name_list):
            self.tableWidget.setItem(idx, 0, QTableWidgetItem(i))
        self.show(index_value_list)
        
    def setSignal(self):
        ...

    def setParameter(self):
        ...

    def processParameter(self):
        ...
        
        
        
class gameScoreBoardManager():
    # 管理精确定时器
    # 5种表达式
    # game_static = ["race_designator", "mode"]
    # game_dynamic = ["rtime", "left", "right", "double", "cl", "left_s", 
    #                 "right_s", "double_s", "path", "flag", "flag_s"]
    # video_static = ["bbbv", "op", "isl", "cell0", "cell1", "cell2", "cell3",
    #                 "cell4", "cell5", "cell6", "cell7", "cell8", "fps"]
    # video_dynamic = ["etime", "stnb", "rqp", "qg", "ioe", "thrp", "corr", "ce",
    #                  "ce_s", "bbbv_solved", "bbbv_s", "op_solved", "isl_solved"]
    game_index = ["race_designator", "mode", "rtime", "left", "right", "double",
                  "cl", "left_s", "right_s", "double_s", "path", "flag", "flag_s"]
    video_index = ["bbbv", "op", "isl", "cell0", "cell1", "cell2", "cell3",
                    "cell4", "cell5", "cell6", "cell7", "cell8", "fps", "etime",
                    "stnb", "rqp", "qg", "ioe", "thrp", "corr", "ce",
                     "ce_s", "bbbv_solved", "bbbv_s", "op_solved", "isl_solved"]
    visible = False
    # 5、错误的表达式，一旦算出报错，永远不再算，显示error
    def __init__(self, score_board_path, pix_size):
        # 从文件中读取指标并设置
        # self.ms_board = None
        self.pix_size = pix_size
        self.namespace = {}
        
        # 时间与定时器
        self.total_time = 0.0 # total_time = delta_time + rtime
        self.delta_time = 0.0
        # self.rtime = 0.0
        # self.timer_time = QTimer()
        # self.timer_time.timeout.connect(self.time_step)
        # self.timer_time.setSingleShot(False)
        # self.timer_time.start(1)
        
        self.initialized = False
        self.score_board_path = score_board_path
        config_score_board = configparser.ConfigParser()
        if config_score_board.read(self.score_board_path):
            # 计时器配置list[tuple(str, str)]
            _score_board_items = config_score_board.items('DEFAULT')
        else:
            config_score_board["DEFAULT"] = {
                "游戏模式": "mode",
                "RTime": "f'{time:.3f}'",
                "Est RTime": "f'{etime:.3f}'",
                "3BV": "bbbv",
                "3BV/s": "f'{solved_bbbv / time:.3f}'",
                "Ops": "op",
                "Isls": "isl",
                "Left": "f'{left}@{left_s:.3f}'",
                "Right": "f'{right}@{right_s:.3f}'",
                "Double": "f'{chording}@{chording_s:.3f}'",
                "IOE": "f'{ioe:.3f}'",
                "Thrp": "f'{thrp:.3f}'",
                "Corr": "f'{corr:.3f}'",
                "Path": "f'{path:.1f}'",
                }
            _score_board_items = list(config_score_board.items('DEFAULT'))
            with open(self.score_board_path, 'w') as configfile:
                config_score_board.write(configfile)  # 将对象写入文件
        self.score_board_items = [[i[0], mm.trans_expression(i[1])] for\
                                  i in _score_board_items]
        self.score_board_items_type = []
        # 整理出计时器上各指标的类型，1表示游戏时更新，2表示录像、游戏时更新
        for i in self.score_board_items:
            expression_i = i[1]
            for j in self.video_index:
                if j in expression_i:
                    self.score_board_items_type.append(2)
                    break
            else:
                self.score_board_items_type.append(1)
        self.ui = ui_Form(pix_size)
        self.index_num = len(self.score_board_items_type)
                    
    def with_namespace(self, namespace: dict):
        # 埋雷结束后调用，固化参数
        # self.pix_size = pix_size
        # self.board = board
        self.namespace.update(namespace)
        # race_designator, mode .etc
        # self.ms_board = ms.BaseVideo(board, pix_size)
        # self.initialized = True
        ...
        
    def reset(self):
        # 清零到默认
        ...
        
    def cal_index_value(self, ms_board, index_type):
        # 原地修改指标数值         
        self.update_namespace(ms_board, index_type)
        index_value = []
        for (_, expression), _type in zip(self.score_board_items, self.score_board_items_type):
            if _type <= index_type:
                index_value.append(str(safe_eval(expression, self.namespace)))
            else:
                index_value.append('--')
        return index_value
        
    # def set_current_time(self, current_time):
    #     # 
    #     self.current_time = current_time
    #     self.ms_board.set_current_time(current_time)
    
    def __visible(self):
        # 仅控制可见性
        # index_value_list = self.cal_index_value()
        # self.ui.reshow([i[0] for i in self.score_board_items], index_value_list)
        if not self.visible:
            self.ui.QWidget.show()
            self.visible = True
        
    def __invisible(self):
        # 仅控制可见性
        ...
        
    
    def update_namespace(self, ms_board, index_type):
        # 全部更新，以后优化就是部分更新, index_type现在没用
        if index_type == 1:
            self.namespace.update({
                "time": ms_board.time,
                "left": ms_board.left,
                "right": ms_board.right,
                "double": ms_board.double,
                "cl": ms_board.cl,
                "left_s": ms_board.left_s,
                "right_s": ms_board.right_s,
                "double_s": ms_board.double_s,
                "path": ms_board.path,
                "flag": ms_board.flag,
                "flag_s": ms_board.flag_s,
                })
        else:
            self.namespace.update({
                "rtime": ms_board.rtime,
                "etime": ms_board.etime,
                "bbbv": ms_board.bbbv,
                "op": ms_board.op,
                })
        
        
    def show(self, ms_board, index_type):
        # 刷新，指标数量不变。游戏过程中用。index_type是2
        # race_designator", "mode"]
        # game_dynamic = ["rtime", "left", "right", "double", "cl", "left_s", 
        #                 "right_s", "double_s", "path", "flag", "flag_s"]
        # video_static = ["bbbv", "op", "isl", "cell0", "cell1", "cell2", "cell3",
        #                 "cell4", "cell5", "cell6", "cell7", "cell8", "fps"]
        # video_dynamic = ["etime", "stnb", "rqp", "qg", "ioe", "thrp", "corr", "ce",
        #                  "ce_s", "bbbv_solved", "bbbv_s", "op_solved", "isl_solved
        # self.ms_board = ms_board
        index_value_list = self.cal_index_value(ms_board, index_type)
        self.ui.show(index_value_list)
        self.__visible()
        
    def reshow(self, ms_board, index_type):
        # 指标数量有变。增删指标用。游戏开始前。index_type是2
        # self.ms_board = ms_board
        index_value_list = self.cal_index_value(ms_board, index_type)
        self.ui.reshow([i[0] for i in self.score_board_items], index_value_list)
        self.__visible()
        ...
        
    def time_step(self):
        # 游戏过程中时间步进
        self.total_time += 0.001
        
        
        self.show()
        
    def step(self, time, e, pos: (int, int)):
        # 接受从局面传过来的参数。单位像素。
        ...
        
        
            
        











