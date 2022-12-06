
import time
import os
import json
from threading import *

from ModelCamera import ViewCamera
from ModelGoogle import ViewGoogle
from ModelThread import ViewThread
from Mediator import ViewMediator
from ModelDeleteFile import ViewDeleteFile

#threadView = ViewThread()

#threadView.AddModel(googleView)
#threadView.Update()
#threadView.Join()
#threadView.Start()


CAMERA_ADDRESS_FILE = 'camera_address.json'

def main():
    with open(CAMERA_ADDRESS_FILE, 'r') as file_json:
        data = json.loads(file_json.read())
    
    path_folder = os.path.exists(data['name_folder'])
    if path_folder:
        for file in os.scandir(data['name_folder']):
            if file.name.endswith(".avi"):
                os.unlink(file.path)

    if(os.path.exists(data['name_folder'])):
       os.rmdir(data['name_folder'])
    
    os.mkdir(data['name_folder'])
    
    time.sleep(1)

    viewMediator = ViewMediator()
    viewCamera = ViewCamera()
    viewGoogle = ViewGoogle()
    viewDeleteFile = ViewDeleteFile()

    viewMediator.AddViewCamera(viewCamera)
    viewMediator.AddViewGoogle(viewGoogle)
    viewMediator.AddViewDeleteFile(viewDeleteFile)

    #viewCamera.AddViewMediator(viewMediator)
    viewCamera.AddMediator(viewMediator)
    #viewGoogle.AddViewMediator(viewMediator)
    viewGoogle.AddMediator(viewMediator)
    
    while True:
        #print(enumerate())
        time.sleep(2)

    #viewCamera.End()
    #viewGoogle.End()

if __name__ == '__main__':
    main()



