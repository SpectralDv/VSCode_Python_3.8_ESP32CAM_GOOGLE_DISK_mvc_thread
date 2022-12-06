
from threading import *

from IMediator import IMediator
from ModelVideo import ModelVideo

class IController:
    #t = Thread;
    name = ""
    mediator = IMediator()

    #def __init__(self,imediator):
    #    self.mediator = imediator

    def CommandMediator(mVideo:ModelVideo):
        pass
    


