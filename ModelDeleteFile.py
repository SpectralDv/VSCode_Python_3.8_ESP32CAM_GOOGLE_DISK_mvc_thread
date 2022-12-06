
import os
from threading import *
import time

from ModelCollection import ModelCollection as Collection
from IView import IView
from IController import IController
from ModelVideo import ModelVideo

#записывает в список файлы которые можно удалить
#сканирует папку и удалят старые файлы

cParams = {
    'format_video':'.avi',
    'path_video_folder':'0',
}

class ModelDeleteFile:
    t = Thread()
    params = {'':''}

class ControllerDeleteFile(IController):
    mDeleteFile = ModelDeleteFile()
    countFile = 0
    #listModelVideo = [ModelVideo]
    mVideo = ModelVideo(0)
    delNumVideo = 0
    state = "Wait"

    def __init__(self): 
        self.mDeleteFile.params = cParams 

    def getParam(self,key):
        return Collection.get_value(self.mDeleteFile.params,key)

    def RemoveVideo(self):
        try:
            #for i in self.listModelVideo:
            #    self.delNumVideo=i.number
            #    if self.delNumVideo < 0: return 0
            #    break;
            if(self.state!="Remove"):return 1
            self.delNumVideo = self.mVideo.number
            self.state="Wait"
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), str(self.getParam('path_video_folder'))+'/'+str(self.delNumVideo)+str(self.getParam('format_video')))
            if path:
                os.remove(path)
                print('RemoveVideo: ',path)
        except Exception as _ex:
            print("Exception RemoveVideo ",_ex)
        return 0

    def ScanerFolder(self):
        self.countFile=0
        for file in os.listdir("0/"):
            if file.endswith(".avi"):
                self.countFile+=1

    def UpdateRemove(self):
        while(1):
            time.sleep(1)
            #self.ScanerFolder()
            self.RemoveVideo()

    ################################################
    def ThreadCreate(self):
        self.mDeleteFile.t = Thread(target = self.UpdateRemove)
    def TreadStart(self):
        try:
            self.mDeleteFile.t.start()
        except Exception as _ex:
            print('Exception TreadStart UpdateRemove: ',_ex)
    def ThreadJoin(self):
        self.t.join();
    ################################################

class ViewDeleteFile(IView):
    controller = ControllerDeleteFile()

    def __init__(self):
        self.controller.ThreadCreate()
        self.controller.TreadStart()

    def CommandMediator(self,msg,mVideo:ModelVideo):
        if(msg=="StateRemove"):
            self.controller.mVideo=mVideo
            self.controller.state="Remove"
