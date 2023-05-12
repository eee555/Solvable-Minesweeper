from PyQt5 import QtCore, QtGui
from ui.ui_record_pop import Ui_Form
from ui.uiComponents import RoundQDialog

class ui_Form(Ui_Form):
    def __init__(self, r_path, del_items: list, pb_bbbv):
        # 关于界面，继承一下就好
        self.Dialog = RoundQDialog()
        self.setupUi (self.Dialog)
        self.Dialog.setWindowIcon (QtGui.QIcon (str(r_path.with_name('media').joinpath('cat.ico'))))
        
        for i in del_items:
            eval("self.widget" + str(i) + ".setHidden(True)")
            
        # self.verticalLayout = QtWidgets.QVBoxLayout(self.Dialog)
        # self.verticalLayout.setObjectName("verticalLayout")
            
        
        self.label1.setStyleSheet("border-image: url(" +\
                                  str(r_path.with_name('media').\
                                      joinpath('rtime.svg')).replace("\\", "/") + ");")
        self.label2.setStyleSheet("border-image: url(" +\
                                  str(r_path.with_name('media').\
                                      joinpath('rtime.svg')).replace("\\", "/") + ");")
        self.label3.setStyleSheet("border-image: url(" +\
                                  str(r_path.with_name('media').\
                                      joinpath('bbbv_s.svg')).replace("\\", "/") + ");")
        self.label4.setStyleSheet("border-image: url(" +\
                                  str(r_path.with_name('media').\
                                      joinpath('bbbv_s.svg')).replace("\\", "/") + ");")
        self.label5.setStyleSheet("border-image: url(" +\
                                  str(r_path.with_name('media').\
                                      joinpath('stnb.svg')).replace("\\", "/") + ");")
        self.label6.setStyleSheet("border-image: url(" +\
                                  str(r_path.with_name('media').\
                                      joinpath('stnb.svg')).replace("\\", "/") + ");")
        self.label7.setStyleSheet("border-image: url(" +\
                                  str(r_path.with_name('media').\
                                      joinpath('ioe.svg')).replace("\\", "/") + ");")
        self.label8.setStyleSheet("border-image: url(" +\
                                  str(r_path.with_name('media').\
                                      joinpath('ioe.svg')).replace("\\", "/") + ");")
        self.label9.setStyleSheet("border-image: url(" +\
                                  str(r_path.with_name('media').\
                                      joinpath('path.svg')).replace("\\", "/") + ");")
        self.label10.setStyleSheet("border-image: url(" +\
                                  str(r_path.with_name('media').\
                                      joinpath('path.svg')).replace("\\", "/") + ");")
        self.label11.setStyleSheet("border-image: url(" +\
                                  str(r_path.with_name('media').\
                                      joinpath('rqp.svg')).replace("\\", "/") + ");")
        self.label12.setStyleSheet("border-image: url(" +\
                                  str(r_path.with_name('media').\
                                      joinpath('rqp.svg')).replace("\\", "/") + ");")
        self.label13.setStyleSheet("border-image: url(" +\
                                  str(r_path.with_name('media').\
                                      joinpath('pb.svg')).replace("\\", "/") + ");")
        self.label14.setStyleSheet("border-image: url(" +\
                                  str(r_path.with_name('media').\
                                      joinpath('pb.svg')).replace("\\", "/") + ");")
        self.label15.setStyleSheet("border-image: url(" +\
                                  str(r_path.with_name('media').\
                                      joinpath('pb.svg')).replace("\\", "/") + ");")
            
        self.pushButton.setStyleSheet("border-image: url(" + str(r_path.with_name('media').joinpath('button.png')).replace("\\", "/") + ");\n"
"font: 16pt \"黑体\";\n"
"color:white;font: bold;")
        self.label__13.setText(str(pb_bbbv))
        self.label__14.setText(str(pb_bbbv))
        self.label__15.setText(str(pb_bbbv))

        # self.Dialog.setFixedSize(self.Dialog.minimumSize())

