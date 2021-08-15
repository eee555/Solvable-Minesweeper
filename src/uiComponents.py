# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 20:04:25 2021

@author: jia32
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QWidget, QDialog
from PyQt5.QtCore import Qt, QRectF
from PyQt5.Qt import  QApplication, QDialog
from PyQt5.QtGui import QPainter, QPainterPath, QCursor
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont, QImage, QPainterPath
# ui相关的小组件，非窗口

class RoundQDialog(QDialog):
    def __init__(self, parent=None):
        # 可以随意拖动的圆角、阴影对话框
        super(RoundQDialog, self).__init__(parent)
        self.border_width = 5
        self.m_drag = False
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

    def paintEvent(self, event):
   	# # 阴影
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)

        pat = QPainter(self)
        pat.setRenderHint(pat.Antialiasing)
        pat.fillPath(path, QBrush(Qt.white))

        color = QColor(192, 192, 192, 50)

        for i in range(10):
            i_path = QPainterPath()
            i_path.setFillRule(Qt.WindingFill)
            ref = QRectF(10-i, 10-i, self.width()-(10-i)*2, self.height()-(10-i)*2)
            # i_path.addRect(ref)
            i_path.addRoundedRect(ref, self.border_width, self.border_width)
            color.setAlpha(150 - i**0.5*50)
            pat.setPen(color)
            pat.drawPath(i_path)

        # 圆角
        pat2 = QPainter(self)
        pat2.setRenderHint(pat2.Antialiasing)  # 抗锯齿
        pat2.setBrush(QtGui.QColor(242, 242, 242, 255))
        pat2.setPen(Qt.transparent)

        rect = self.rect()
        rect.setLeft(9)
        rect.setTop(9)
        rect.setWidth(rect.width()-9)
        rect.setHeight(rect.height()-9)
        pat2.drawRoundedRect(rect, 10, 10)
        
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = e.globalPos() - self.pos()
            e.accept()
            # self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.m_drag = False
            # self.setCursor(QCursor(Qt.ArrowCursor))

    def mouseMoveEvent(self, e):
        if Qt.LeftButton and self.m_drag:
            self.move(e.globalPos() - self.m_DragPosition)
            e.accept()
            
            
            



