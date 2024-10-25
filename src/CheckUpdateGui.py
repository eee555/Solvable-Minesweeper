from PyQt5.QtWidgets import QWidget, QScrollArea, QLabel, QVBoxLayout, QApplication, QHBoxLayout, QSpacerItem,\
QSizePolicy, QPushButton,QFrame,QMessageBox,QFormLayout,QProgressDialog,QTextEdit,QComboBox
from githubApi import GitHub, Release,SourceManager,PingThread
from PyQt5.QtCore import QObject,pyqtSlot,Qt,pyqtSignal,QUrl
from PyQt5.QtGui import QDesktopServices,QFont



class ReleaseFrame(QFrame):
    downLoadFile = pyqtSignal(Release)
    def __init__(self, release: Release,mode = ">", parent=None):
        super().__init__(parent)
        self.release: Release = release
        self.showButton = QPushButton(QObject.tr(self, "Show"))
        self.showButton.setCheckable(True)
        self.formWidget = QWidget()
        self.downloadButton = QPushButton(QObject.tr(self, "Download"))
        self.formWidget.hide()
        self.bodyEdit = QTextEdit()
        self.mode = mode
        self.initUi()
        self.initConnect()

    def initUi(self):

        # self.setFrameShape(QFrame.StyledPanel)
        layout = QVBoxLayout()
        row1 = QHBoxLayout()
        row1.addWidget(self.showButton)
        row1.addWidget(QLabel(self.release.tag_name))
        row1.addItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.downloadButton.setEnabled(self.mode == ">")
        row1.addWidget(self.downloadButton)
        
        formLayout = QFormLayout()
        formLayout.setContentsMargins(0, 0, 0, 0)
        urlLabel = QLabel()
        urlLabel.setText("<a href='" + self.release.html_url + "'>" +  QObject.tr(self,"open external links")+ "</a>")
        urlLabel.setOpenExternalLinks(True)
        dataLayout = QVBoxLayout()
        dataLayout.setContentsMargins(0, 0, 0, 0)
        formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        formLayout.addRow(QObject.tr(self, "html_url"), urlLabel)
        formLayout.addRow(QObject.tr(self, "name"), QLabel(self.release.assets_name))
        formLayout.addRow(QObject.tr(self, "content_type"), QLabel(self.release.assets_content_type))
        formLayout.addRow(QObject.tr(self, "size"), QLabel(str(f"{self.release.assets_size / 1000000:.2f} MB")))
        formLayout.addRow(QObject.tr(self, "download_count"), QLabel(str(self.release.assets_download_count)))
        formLayout.addRow(QObject.tr(self, "created_at"), QLabel(self.release.assets_created_at))
        downloadUrlLabel = QLabel()
        downloadUrlLabel.setText("<a href='" + self.release.assets_browser_download_url + "'>" +  QObject.tr(self,"open download links")+ "</a>")
        downloadUrlLabel.setOpenExternalLinks(True)
        formLayout.addRow(QObject.tr(self, "browser_download_url"), downloadUrlLabel)
        dataLayout.addLayout(formLayout)
        self.bodyEdit.setMarkdown(self.release.body)
        self.bodyEdit.setReadOnly(True)
        font = QFont("Microsoft YaHei UI", 13)
        font.setBold(True)
        self.bodyEdit.setFont(font)
        self.bodyEdit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        dataLayout.addWidget(self.bodyEdit)
        self.formWidget.setLayout(dataLayout)

        layout.addLayout(row1)
        layout.addWidget(self.formWidget)    
        self.setLayout(layout)
        rgbStr = ""
        if self.mode == ">":
            # 样式表绿色
            rgbStr = "rgb(200,255,250)"
        elif self.mode == "=":
            # 样式表蓝色
            rgbStr = "rgb(200,216,230)"
        else:
            # 样式表红色背景
            rgbStr = "rgb(249, 179, 163)"
        # label字体微软雅黑Ui,大小13
        self.setStyleSheet(f"QFrame{{background-color:{rgbStr}; font-family:Microsoft YaHei UI; font-size:14px;}}") 
        
    def initConnect(self):
        self.showButton.clicked.connect(self.showButtonClicked)
        self.downloadButton.clicked.connect(self.downLoadButtonClicked)
    def showButtonClicked(self,checked:bool):
        if checked:
            self.formWidget.show()
        else:
            self.formWidget.hide()
    def downLoadButtonClicked(self):
        self.downLoadFile.emit(self.release)
        

class CheckUpdateGui(QWidget):
    def __init__(self,github:GitHub, parent=None):
        super().__init__(parent)
        self.github: GitHub = github
        self.github.setParent(self)
        self.checkUpdateButton = QPushButton(
            QObject.tr(self, "CheckUpdate"), self)
        self.releaseArea = QScrollArea()
        self.releaseArea.setWidgetResizable(True)
        # 禁用横向滚动条
        self.releaseArea.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.sourceCombo = QComboBox()
        self.sourceCombo.addItems(self.github.sourceManager.sources.keys())
        self.sourceCombo.setCurrentText(self.github.sourceManager.currentSource)
        self.currentVersionLabel = QLabel(f"Current Version:{self.github.version}")
        self.processDialog = None
        self.initUi()
        self.initConnect()
        self.resize(450, 600)
        self.checkUpdateButton.click()
    def initUi(self):
        font = QFont("Microsoft YaHei UI", 13)
        font.setBold(True)
        self.currentVersionLabel.setFont(font)
        layout = QVBoxLayout()

        row1 = QHBoxLayout()
        row1.setContentsMargins(0, 0, 0, 0)
        row1.addWidget(self.currentVersionLabel)
        row1.addItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        row1.addWidget(self.sourceCombo)
        row1.addWidget(self.checkUpdateButton)

        row2 = QHBoxLayout()
        row2.setContentsMargins(0, 0, 0, 0)

        row2.addWidget(self.releaseArea)


        layout.addLayout(row1)
        layout.addLayout(row2)

        self.setLayout(layout)

    def initConnect(self):
        self.checkUpdateButton.clicked.connect(lambda: self.github.releases())    
        self.github.releasesAsyncSignal.connect(self.checkUpdate)
        self.github.errorSignal.connect(self.showError)
        self.github.downloadReleaseAsyncStartSignal.connect(self.showDownloadDialog)
        self.github.downloadReleaseAsyncProgressSignal.connect(self.updateDownloadDialog)
        self.github.downloadReleaseAsyncFinishSignal.connect(self.hideDownloadDialog)
        
    @pyqtSlot(list)
    def checkUpdate(self,releases:list):
        widget = self.releaseArea.widget()
        if widget is not None:
            widget.deleteLater()
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        for release in releases:
            frame = ReleaseFrame(release,self.github.compareVersion(release.tag_name))
            layout.addWidget(frame)
            frame.downLoadFile.connect(self.github.downloadRelease)
        # 底部加一个空白区域
        panel = QWidget()
        panel.setContentsMargins(0, 0, 0, 0)
        panel.setFixedHeight(100)
        layout.addWidget(panel)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        widget.setLayout(layout)
        self.releaseArea.setWidget(widget)
    def showError(self,msg:str):
        QMessageBox.critical(self,QObject.tr(self, "Error"),msg)

    def showDownloadDialog(self,release:Release):
        if self.processDialog is not None:
            self.processDialog.close()
        self.processDialog = QProgressDialog(self)
        self.processDialog.setWindowTitle(QObject.tr(self, f"{release.tag_name} Downloading..."))
    def updateDownloadDialog(self,a:int,b:int):
        if self.processDialog is not None:
            self.processDialog.setValue(a)
            self.processDialog.setMaximum(b)
            self.processDialog.setLabelText(f'{a/1000000 : .2f}/{b/1000000 : .2f} MB')
    def hideDownloadDialog(self,path:str):
        if self.processDialog is not None:
            self.processDialog.close()
            self.processDialog = None
        # 使用系统默认方式打开文件
        QDesktopServices.openUrl(QUrl.fromLocalFile(path))

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    data = {
        "Github": "https://api.github.com/repos/",
        "fff666": "https://fff666.top/",
    }
    w = CheckUpdateGui(GitHub(SourceManager(data),"eee555", "Solvable-Minesweeper", "3.1.9", "(\d+\.\d+\.\d+)"))
    w.show()
    sys.exit(app.exec_())
