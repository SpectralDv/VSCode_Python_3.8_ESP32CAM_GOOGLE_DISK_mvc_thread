

from IController import IController
from StateMashine import StateMashine
from State import *
from IView import IView
from IMediator import IMediator
from ModelVideo import ModelVideo


class Mediator(IMediator):
    nameCommand = "StateWait"
    controllerGoogle = IController()
    controllerCamera = IController()
    def AddControllerCamera(self,icontroller):
        self.controllerCamera = icontroller
    def AddControllerGoogle(self,icontroller):
        self.controllerGoogle = icontroller

    def notify(self,msg,mVideo:ModelVideo):
        if msg == "StateWait":
            pass
        if msg == "StateUploadGoogle":
            self.controllerGoogle.CommandMediator("StateUploadGoogle",mVideo)

class ControllerMediator(IController):
    nameCommand = "StateWait"
    stateMashine = StateMashine()
    controllerGoogle = IController()
    controllerCamera = IController()

    def AddControllerCamera(self,icontroller):
        self.controllerCamera = icontroller
    def AddControllerGoogle(self,icontroller):
        self.controllerGoogle = icontroller

    def Update(self):
        if self.nameCommand == "StateWait":
            self.stateMashine(StateWait(self.controllerGoogle))
        if self.nameCommand == "StateUploadGoogle":
            self.stateMashine(StateUploadGoogle(self.controllerGoogle))


class ViewMediator(IView):
    mediator = Mediator()
    controllerMediator = ControllerMediator()
    viewCamera = IView()
    viewGoogle = IView()
    viewDeleteFile = IView()

    def AddViewCamera(self,iview):
        self.viewCamera = iview
    def AddViewGoogle(self,iview):
        self.viewGoogle = iview
    def AddViewDeleteFile(self,iview):
        self.viewDeleteFile = iview
    def notify(self,msg,mVideo:ModelVideo):
        if msg == "StateWait":
            pass
        if msg == "StateUploadGoogle":
            self.viewGoogle.CommandMediator("StateUploadGoogle",mVideo)
        if msg == "StateRemove":
            self.viewCamera.CommandMediator("StateRemove",mVideo)
            self.viewDeleteFile.CommandMediator("StateRemove",mVideo)