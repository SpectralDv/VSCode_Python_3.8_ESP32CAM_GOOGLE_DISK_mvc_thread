
import cv2
from threading import *
import os

from ModelCollection import ModelCollection as Collection
from IModel import IModel
from IController import IController
from StateMashine import StateMashine
from State import *
from IView import IView
from IMediator import IMediator
from ModelVideo import ModelVideo

DEBUG = 1

cParams = {
    'name': 'camera',
    'height': 320,
    'width': 240,
    'path_stream':'http://0.0.0.0:0/',
    'count_frame_video':200,
    'fps_video': 30.0,
    'format_video':'.avi',
    'path_video_folder':'0',
    'event_move':1,
    'countVideo':0,
    'countMove':0,
    'countFrame':0,
    'framePred': '',
    'frameCur': '',
    'frameNext': '',
    'step_del_video':3,
}

cParams2 = {
    'name': 'video',
    'height': 360,
    'width': 240,
    'path_cap':'video.mp4',
}

class ModelCamera(IModel):
    params = {'':''}
    #params = ['']
    capture = cv2.VideoCapture()
    framePred = ""
    frameCur = ""
    frameNext = ""
    countMove = 0
    countFrame = 0
    countVideo = 0
    outVID = any
    eventInit = True 
    eventWriteVideo = False
    eventRemoveVideo = False
    eventUploadVideo = False
    t = Thread()

class ControllerCamera(IController):
    mCamera = ModelCamera()
    stateMashine = StateMashine()
    nameCommand = "StateWait"
    mediator = IMediator()
    mVideo = ModelVideo(0)
    listModelVideo = [ModelVideo]
    numVideo = 0
    delNumVideo = 0

    def SetParam(self,key,value):
        self.mCamera.params.setdefault(key,value)

    def getParam(self,key):
        return Collection.get_value(self.mCamera.params,key)

    def __init__(self): 
        self.listModelVideo.clear()
        self.mCamera = ModelCamera()
        self.mCamera.params = cParams 
        self.stateMashine.Initialize(StateWait(self))

    def AddMediator(self,imediator):
        self.mediator = imediator

    #def CommandMediator(self):
    #    self.mediator.notify(self,"StateUploadGoogle")

    def ParamCamera(self,params=['']):
        self.mCamera.params = params 
    def StartCamera(self):
        try:
            self.mCamera.capture = cv2.VideoCapture(self.getParam('path_stream'))
        except Exception as _ex:
            print('Error GetCamera: ')
            print(_ex)
    ######################################
    def UpdateCamera(self):
        try:
            ret, self.mCamera.frameNext = self.mCamera.capture.read()
            while self.mCamera.capture.isOpened():
                
                self.Move()
                self.WinShow()
                self.EventMashine()
                self.InitVideo()
                self.WriteWideo()
                #self.RemoveVideo()
                self.UploadVideo()

                if cv2.waitKey(1) == 27:
                    break
        except Exception as _ex:
            print('Exception UpdateCamera: ',_ex)
            self.Release()
    ###################################
    def Release(self):
        try:
            self.mCamera.capture.release()
            cv2.destroyWindow(Collection.get_value(self.mCamera.params,'name'))
        except Exception as _ex:
            print('Exception Release: ',_ex)
    #######

    def WinShow(self):
        try:
            cv2.imshow(Collection.get_value(self.mCamera.params,'name'), self.mCamera.frameCur)
            self.SetParam('countMove',1)
            #print(self.getParam('countMove'))
        except Exception as _ex:
            print('Exception WinShow: ',_ex)
            self.Release()

    def Move(self):
        try:
            self.mCamera.frameCur = self.mCamera.frameNext
            ret, self.mCamera.frameNext = self.mCamera.capture.read()
            diff = cv2.absdiff(self.mCamera.frameCur,self.mCamera.frameNext)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0) #фильтрация лишних контуров
            a,thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY) #метод для выделения кромки объекта белым цветом
            dilated = cv2.dilate(thresh, None, iterations = 3) #расширяет выделенную на предыдущем этапе область
            сontours,b = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #нахождение массива контурных точек

            for contour in сontours:
                (x, y, w, h) = cv2.boundingRect(contour) # преобразование массива из предыдущего этапа в кортеж из четырех координат

                if cv2.contourArea(contour) < 100: # условие при котором площадь выделенного объекта меньше 700 px
                    self.mCamera.countMove = 0;
                    continue
                        
                cv2.rectangle(self.mCamera.frameCur, (x, y), (x+w, y+h), (0, 255, 0), 2) # получение прямоугольника из точек кортежа
                #cv2.putText(self.mCamera.frameCur, "Status: {}".format("Dvigenie"), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA) #текст
                self.mCamera.countMove += 1
        except Exception as _ex:
            print('Exception Move: ',_ex)
            self.Release()

    def CreateVideo(self):
        if self.mCamera.countFrame > self.getParam('count_frame_video'):
            """
            name_file = str(pred_count)+'.avi'
            eventUpload = True
            #google_upoload(str(pred_count)+'.avi',name_folder)
            """

    def UploadVideo(self):
        try:
            if not(self.mCamera.eventUploadVideo): return 1
            #self.numVideo = self.mCamera.countVideo - 1
            #if (self.numVideo < 0): return 1
            #if (len(self.listModelVideo) == 0): return 1
            #for i in self.listModelVideo:
                #if(i.state=="Remove"):
                #    self.numVideo = i.number+1
                    #self.listModelVideo.remove(i)
                #    break
                #if(i.number==0):
                #    self.numVideo = i.number
                #    #self.listModelVideo.remove(i)
                #    break
                #else: return 1
            if(DEBUG==1):print("UploadVideo/ControllerCamera, number: ", self.mCamera.countVideo-1)
            #self.listModelVideo[self.numVideo].state = "Upload"
            #self.mediator.notify("StateUploadGoogle",self.listModelVideo[self.numVideo])
            self.mediator.notify("StateUploadGoogle",ModelVideo(self.mCamera.countVideo-1))
            self.mCamera.eventUploadVideo = False
        except Exception as _ex:
            print('Exception UploadVideo: ',_ex)
            self.Release()
        return 0

    def InitVideo(self):
        if not(self.mCamera.eventInit):return 0
        if(DEBUG==1):print('Begin InitVideo/ControllerCamera')
        #name_video_file = str('video_folder')+'/'+str(self.mCamera.countVideo)+'.avi'
        #self.mCamera.outVID = cv2.VideoWriter(name_video_file, cv2.VideoWriter_fourcc(*'XVID'), 30, (320,240))
        name_video_file = str(self.getParam('path_video_folder'))+'/'+str(self.mCamera.countVideo)+str(self.getParam('format_video'))
        self.mCamera.outVID = cv2.VideoWriter(name_video_file, cv2.VideoWriter_fourcc(*'XVID'), self.getParam('fps_video'), (self.getParam('height'),self.getParam('width')))  
        self.listModelVideo.append(ModelVideo(self.mCamera.countVideo))
        self.mCamera.eventInit = False
        if(DEBUG==1):print('End InitVideo/ControllerCamera')

    def WriteWideo(self):
        if self.mCamera.eventWriteVideo:
            self.mCamera.outVID.write(self.mCamera.frameCur)
            self.mCamera.countFrame += 1
            #print(self.mCamera.countFrame)
            #ret, frame = self.mCamera.capture.read()
            #outVID.write(frame)

    def RemoveVideo(self):
        try:
            #if not(self.mCamera.eventRemoveVideo): return 0
            #print("len: ",len(self.listModelVideo))
            if(len(self.listModelVideo)<2):return 0
            for i in self.listModelVideo:
                if(i.number==self.mVideo.number):
                    i.state=self.mVideo.state
                    if(i.state=="Remove"):
                        self.delNumVideo=i.number
                        if self.delNumVideo < 0: return 0
                        break;
                return 0
            #self.delNumVideo = self.mCamera.countVideo - self.getParam('step_del_video')
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), str(self.getParam('path_video_folder'))+'/'+str(self.delNumVideo)+str(self.getParam('format_video')))
            if path:
                print('Begin RemoveVideo/ControllerCamera: ',self.listModelVideo[self.delNumVideo].state)
                os.remove(path)
            #self.mCamera.eventRemoveVideo = False
            print('End RemoveVideo/ControllerCamera')
        except Exception as _ex:
            print("Exception RemoveVideo ",_ex)
        return 0

    def EventMashine(self):
        #WriteBegin
        if self.mCamera.countMove > 1:
            self.mCamera.eventWriteVideo = True
        #WriteEnd
        if self.mCamera.countFrame > self.getParam('count_frame_video'):
            self.mCamera.countVideo += 1
            self.mCamera.countFrame = 0
            self.mCamera.eventWriteVideo = False
            self.mCamera.eventInit = True
            self.mCamera.eventRemoveVideo = True
            self.mCamera.eventUploadVideo = True
            if(DEBUG==1):print("EventMashine/ControllerCamera countVideo: "+str(self.mCamera.countVideo))

    ################################################
    def ThreadCreate(self):
        self.StartCamera()
        self.mCamera.t = Thread(target = self.UpdateCamera)
        #print('ThreadCreate: mCamera')
    def TreadStart(self):
        try:
            self.mCamera.t.start()
            #print('TreadStart: mCamera')
        except Exception as _ex:
            print('Error TreadStart: ')
            print(_ex)
    def ThreadJoin(self):
        self.mCamera.t.join();
    ################################################
        
class ViewCamera(IView):
    controller = ControllerCamera()
    viewMediator = IView()

    def __init__(self):
        self.controller.ParamCamera(cParams)
        self.controller.ThreadCreate()
        self.controller.TreadStart()
        if(DEBUG==1):print("ViewCamera init");
    
    def AddMediator(self,imediator):
        self.controller.AddMediator(imediator)

    def End(self):
        #self.controller.ThreadJoin()
        self.controller.Release()
        cv2.destroyAllWindows()
    
    def CommandMediator(self,msg,mVideo:ModelVideo):
        if(msg=="StateRemove"):
            for i in self.controller.listModelVideo:
                if(i.number == mVideo.number):
                    i.state = mVideo.state
                    

            

    
