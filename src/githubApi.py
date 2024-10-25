
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QUrl,QObject,pyqtSignal,QEventLoop,QCoreApplication,QThread,QElapsedTimer
import json
import re
import os
import tempfile
import subprocess


class PingThread(QThread):
    pingSignal = pyqtSignal(str,float)
    def __init__(self, name: str,url: str,parent : QObject | None = None) -> None:
        super().__init__(parent)
        self.reSet(name,url)
        
    def reSet(self,name: str,url: str):
        self.name = name
        self.url = url
        self.host = self.url.split("/")
        
    
    def ping(self):
        timer = QElapsedTimer()
        timer.start()
        try:
            nam = QNetworkAccessManager(self)
            request = QNetworkRequest(QUrl(self.url))
            
            reply = nam.get(request)
            loop = QEventLoop()
            reply.finished.connect(loop.quit)
            loop.exec_()
            
        except Exception as e:
            return float('inf')
        time = timer.elapsed()
        return time

    def run(self):
        responseTime = self.ping()
        self.pingSignal.emit(self.name, responseTime)


class SourceManager(QObject):
    quickSource = pyqtSignal(str,float)
    def __init__(self,sources:dict,parent=None):
        super().__init__()
        if not isinstance(sources,dict):
            raise TypeError
        if not sources:
            raise ValueError
        self.sources = sources
        # 第一个的key
        self.currentSource = list(sources.keys())[0]
        self.speedData = {}
        self.threads = []

    
    @property
    def sources(self):
        return self.__sources

    @sources.setter
    def sources(self,sources:dict):
        if not isinstance(sources,dict):
            raise TypeError
        if not sources:
            raise ValueError
        for key in sources:
            sources[key] = sources[key].strip('/')
        self.__sources = sources
        self.currentSource = list(sources.keys())[0]
    
    @property
    def currentSource(self):
        return self.__currentSource
    
    @currentSource.setter
    def currentSource(self,currentSource:str):
        if currentSource not in self.sources:
            raise ValueError
        self.__currentSource = currentSource

    @property
    def currentSourceUrl(self):
        return self.sources[self.currentSource]

    def checkSourceSpeed(self):
        self.threads.clear()
        self.speedData = {}
        for source in self.sources:
            thread = PingThread(source, self.sources[source])
            thread.pingSignal.connect(self.pingSignal)
            self.threads.append(thread)
            thread.start()

    def pingSignal(self,url: str, responseTime: float):
        self.speedData[url] = responseTime
        if len(self.speedData) == len(self.sources):
            quickTime = float('inf')
            quickKey = ''           
            for key,value in self.speedData.items():
                if value < quickTime:
                    quickTime = value
                    quickKey = key
            self.quickSource.emit(quickKey,quickTime)
    
class Release:
    def __init__(self,dict):
        self.tag_name = dict['tag_name']
        self.body = dict['body']
        self.html_url = dict['html_url']
        m_assert = dict['assets'][0]
        self.assets_name = m_assert['name']
        self.assets_content_type = m_assert['content_type']
        self.assets_size = m_assert['size']
        self.assets_download_count = m_assert['download_count']
        self.assets_created_at = m_assert['created_at']
        self.assets_browser_download_url = m_assert['browser_download_url']
class GitHub(QObject):
    isNeedUpdateAsyncSignal = pyqtSignal(bool)
    latestReleaseAsyncSignal = pyqtSignal(Release)
    releasesAsyncSignal = pyqtSignal(list)
    downloadReleaseAsyncStartSignal = pyqtSignal(Release)
    downloadReleaseAsyncProgressSignal = pyqtSignal(int,int)
    downloadReleaseAsyncFinishSignal = pyqtSignal(str)
    errorSignal = pyqtSignal(str)
    def __init__(self,sourcemanager:SourceManager,owner:str,repo:str,version:str,versionReStr:str,parent=None):
        super().__init__(parent)
        self.__sourcemanager = sourcemanager
        self.__owner = owner
        self.__repo = repo
        self.__version = version
        self.__versionReStr = versionReStr
    
    @property
    def sourceManager(self):
        return self.__sourcemanager 

    @sourceManager.setter
    def sourceManager(self,sourcemanager:SourceManager):
        self.__sourcemanager = sourcemanager
    
    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self,owner:str):
        self.__owner = owner

    @property
    def repo(self):
        return self.__repo

    @repo.setter
    def repo(self,repo:str):
        self.__repo = repo

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self,version:str):
        self.__version = version

    @property
    def versionReStr(self):
        return self.__versionReStr

    @versionReStr.setter
    def versionReStr(self,versionReStr:str):
        self.__versionReStr = versionReStr
    @property
    def latestReleaseUrl(self) -> str:
        return f'{self.sourceManager.currentSourceUrl}/{self.__owner}/{self.__repo}/releases/latest'
    @property
    def releasesUrl(self) -> str:
        return f'{self.sourceManager.currentSourceUrl}/{self.__owner}/{self.__repo}/releases'
    @property
    def header(self) -> dict:
        return {
            'Accept':'application/vnd.github.v3+json',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        }
    def isNeedUpdate(self,isAsync:bool = True) -> bool | None:
        nam = QNetworkAccessManager(self)
        request = QNetworkRequest(QUrl(self.latestReleaseUrl))
        reply = nam.get(request)
        if not isAsync:
            loop = QEventLoop()
            reply.finished.connect(loop.quit)
            loop.exec()
            if reply.error() != QNetworkReply.NoError:
                self.error(reply.errorString())
                return None
            data = reply.readAll().data().decode('utf-8')
            reply.deleteLater()
            return self.__isNeedUpdate(data)
        else:
            nam.finished.connect(self.__isNeedUpdateAsync)
            return None
            
    def __isNeedUpdate(self,data)->bool:
        release = Release(json.loads(data))
        current = re.findall(self.__versionReStr,release.tag_name)
        if len(current) == 0:
            return False
        new = re.findall(self.__versionReStr,self.__version)
        if len(new) == 0:
            return False
        if new[0] > current[0]:
            return True
    
    def __isNeedUpdateAsync(self,reply:QNetworkReply):
        if reply.error() != QNetworkReply.NoError:
            self.error(reply.errorString())
            return
        self.isNeedUpdateAsyncSignal.emit(self.__isNeedUpdate(reply.readAll().data().decode('utf-8')))
        reply.deleteLater()

    def latestRelease(self,isAsync:bool = True) -> Release | None:
        nam = QNetworkAccessManager(self)
        request = QNetworkRequest(QUrl(self.latestReleaseUrl))
        reply = nam.get(request)
        if not isAsync:
            loop = QEventLoop()
            reply.finished.connect(loop.quit)
            loop.exec()
            if reply.error() != QNetworkReply.NoError:
                self.error(reply.errorString())
                return None
            data = reply.readAll().data().decode('utf-8')
            reply.deleteLater()
            return Release(json.loads(data))
        else:
            nam.finished.connect(self.__lastReleaseAsync)
            return None
    
    def __lastReleaseAsync(self,reply:QNetworkReply):
        if reply.error() != QNetworkReply.NoError:
            self.error(reply.errorString())
            return
        self.latestReleaseAsyncSignal.emit(Release(json.loads(reply.readAll().data().decode('utf-8'))))
        
    
    def releases(self,isAsync:bool = True) -> list | None:
        nam = QNetworkAccessManager(self)
        request = QNetworkRequest(QUrl(self.releasesUrl))
        reply = nam.get(request)
        if not isAsync:
            loop = QEventLoop()
            reply.finished.connect(loop.quit)
            loop.exec()
            if reply.error() != QNetworkReply.NoError:
                self.error(reply.errorString())
                return None
            data = reply.readAll().data().decode('utf-8')
            reply.deleteLater()
            return self.__releases(data)
        else:
            nam.finished.connect(self.__releasesAsync)
            return None
        
        
    def __releases(self,data) -> list | None:
        return [Release(x) for x in json.loads(data)]
        
    def __releasesAsync(self,reply:QNetworkReply):
        if reply.error() != QNetworkReply.NoError:
            self.error(reply.errorString())
            return
        releases = self.__releases(reply.readAll().data().decode('utf-8'))
        reply.deleteLater()
        self.releasesAsyncSignal.emit(releases)    

    def downloadRelease(self,release:Release):
        nam = QNetworkAccessManager(self)
        self.downloadReleaseAsyncStartSignal.emit(release)
        request = QNetworkRequest(QUrl(release.assets_browser_download_url))
        request.setAttribute(QNetworkRequest.Attribute.FollowRedirectsAttribute,True)
        reply = nam.get(request)
        reply.downloadProgress.connect(self.downloadProgress)
        reply.finished.connect( lambda : self.saveFile(release))
     
    def downloadProgress(self,bytesReceived:int,bytesTotal:int):
        self.downloadReleaseAsyncProgressSignal.emit(bytesReceived,bytesTotal)
    def saveFile(self,release:Release):
        reply:QNetworkReply = self.sender()
        if reply.error() != QNetworkReply.NoError:
            self.error(reply.errorString())
            return
        # 临时文件夹
        tempDir = tempfile.gettempdir()
        path = os.path.join(tempDir,release.assets_name)
        # 判断是否存在
        if os.path.exists(path):
            os.remove(path)
        with open(path,'wb') as f:
            f.write(reply.readAll())
        reply.deleteLater()
        self.downloadReleaseAsyncFinishSignal.emit(path)
        
    def compareVersion(self,v2) -> str:
        v = re.findall(self.__versionReStr,self.__version)
        if len(v) == 0:
            return '<'
        v1 = new = re.findall(self.__versionReStr,v2)
        if len(v1) == 0:
            return '<'
        v1 = v1[0]
        v = v[0]
        vlist = v.split('.')
        v1list = v1.split('.')
        for i in range(len(vlist)):
            if int(vlist[i]) > int(v1list[i]):
                return '<'
            elif int(vlist[i]) < int(v1list[i]):
                return '>'
        return '='
    
    def error(self,errorStr:str):
        self.errorSignal.emit(errorStr)
    
    

if __name__ == '__main__':
    app = QCoreApplication([])
    data = {
        "Github": "https://api.github.com/repos/",
        "fff666": "https://fff666.top/",
    }
    github = GitHub(SourceManager(data),"eee555","Solvable-Minesweeper","3.1.9","(\d+\.\d+\.\d+)")
    github.releasesAsyncSignal.connect(lambda x:print(x))
    github.releases()
    # manager = SourceManager(data)
    # manager.quickSource.connect(lambda x,y:print(x,y))
    # manager.checkSourceSpeed()
    app.exec_()
    