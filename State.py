
from IState import IState
from IController import IController


class StateWait(IState):
    controller = IController()
    def __init__(self,icontroller):
        self.controller = icontroller
    def Enter(self):
        print("StateWait Enter")
    def Exit(self):
        print("StateWait Exit")
 
class StateUploadGoogle(IState):
    controller = IController()
    def __init__(self,icontroller):
        self.controller = icontroller
    def Enter(self):
        self.controller.UploadFile()
        print("StateUploadGoogle Enter")
    def Exit(self):
        print("StateUploadGoogle Exit")
