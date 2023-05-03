# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 16:01:56 2022

@author: jia32
"""

from PyQt5 import QtCore
from ui.uiComponents import RoundQWidget, CommentLabel
from ui.ui_video_control import Ui_Form
from PyQt5.QtCore import Qt

class ui_Form(Ui_Form):
    # barSetMineNum = QtCore.pyqtSignal(int)
    # barSetMineNumCalPoss = QtCore.pyqtSignal(int)
    # time_current = 0.0
    
    def __init__(self, r_path, time, comments):
        self.QWidget = RoundQWidget()
        self.setupUi(self.QWidget)
        self.horizontalSlider_time.setMaximum(int(time * 100 + 1))
        
        self.horizontalSlider_time.valueChanged[int].connect(self.set_double_spin_box_time)
        self.doubleSpinBox_time.valueChanged[float].connect(self.set_horizontal_slider_time)
        
        self.comments_labels = []
        comment_row = 1
        for comment in comments:
            # print(comment)
            c1 = CommentLabel(self.scrollAreaWidgetContents, comment[0], int(comment[0] * 100))
            c1.setGeometry(QtCore.QRect(0, 42 * comment_row, 68, 42))
            for list_ in comment[1]:
                # if len(list_) == 1:
                #     list_ = ['luck'] + list_
                c2 = CommentLabel(self.scrollAreaWidgetContents, list_[0], int(comment[0] * 100))
                c2.setGeometry(QtCore.QRect(68, 42 * comment_row, 90, 42))
                c3 = CommentLabel(self.scrollAreaWidgetContents, list_[1], int(comment[0] * 100))
                c3.setGeometry(QtCore.QRect(158, 42 * comment_row, 300, 42))
                c3.setWordWrap(True)
                self.comments_labels.append([c1, c2, c3])
                comment_row += 1
        self.scrollAreaWidgetContents.setFixedHeight(42 * (comment_row + 1))
        self.pushButton_replay.setStyleSheet("border-image: url(" + str(r_path.with_name('media').joinpath('replay.svg')).replace("\\", "/") + ");")
        self.pushButton_play.setStyleSheet("border-image: url(" + str(r_path.with_name('media').joinpath('play.svg')).replace("\\", "/") + ");")
        self.label_speed.setStyleSheet("border-image: url(" + str(r_path.with_name('media').joinpath('speed.svg')).replace("\\", "/") + ");\n"
"font: 12pt \"微软雅黑\";\n"
"color: #50A6EA;")
        self.label_2.setStyleSheet("border-image: url(" + str(r_path.with_name('media').joinpath('mul.svg')).replace("\\", "/") + ");\n"
"font: 12pt \"微软雅黑\";\n"
"color: #50A6EA;")
        
        
    def set_double_spin_box_time(self, int_time):
        self.doubleSpinBox_time.setValue(int_time / 100)
        # self.time_current = int_time / 100
        
    def set_horizontal_slider_time(self, float_time):
        self.horizontalSlider_time.setValue(int(float_time * 100))
        # self.time_current = float_time
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
        