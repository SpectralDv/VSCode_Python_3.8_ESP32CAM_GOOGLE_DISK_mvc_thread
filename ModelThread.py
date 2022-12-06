
from threading import *
from IModel import IModel


class ModelThread:
    t = Thread

class ControllerThread:
    listModel = []

    def AddModel(self,model):
        #добовляет модель и функцию апдейт
        print("Start AddModel")
        self.listModel.append(model)
        print(self.listModel.count(model))
        
    def ThreadCreate(self):
        #перебирает список и присваивает в поток метод апдейт у каждой модели
        #self.listModel.t = Thread(target = model.updateView())
        #for i in self.listModel.copy():
        #    i.t.start()
        pass

    def ThreadJoin(self):
        #self.listModel.t.join()
        for i in self.listModel.copy():
            self.listModel[i].t.join()

    def TreadStart(self):
        #self.listModel.t.start()
        print("Start TreadStart")
        for i in self.listModel.copy():
            i.t.start()
            print("Start thread: ",self.listModel[i].t)
        print("End TreadStart")

class ViewThread:
    controllerThread = ControllerThread()

    def AddModel(self,model):
        self.controllerThread.AddModel(model)

    def Update(self):
        self.controllerThread.ThreadCreate()

    def Join(self):
        self.controllerThread.ThreadJoin()

    def Start(self):
        self.controllerThread.TreadStart()


#Thread(target = self.UpdateCamera)
#Thread = Timer(0,self.UpdateCamera)
#main_thread().SetName("New name")
#print(main_thread()) #выводит главный поток
#print(active_count()) #выводит количество активных потоков
#print(current_thread()) #выводит текущий поток
#print(enumerate()) #возвращает все активные потоки с именами