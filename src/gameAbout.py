from PyQt5 import QtCore, QtGui, QtWidgets
from ui.ui_about import Ui_Form
from ui.uiComponents import RoundQDialog

class ui_Form(Ui_Form):
    def __init__(self):
        # 关于界面，继承一下就好
        self.Dialog = RoundQDialog()
        self.setupUi (self.Dialog)
        self.Dialog.setWindowIcon (QtGui.QIcon ("media/cat.ico"))

    


