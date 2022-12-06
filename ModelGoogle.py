
from threading import *
import os
import time
from oauth2client.file import Storage
from oauth2client import client
from oauth2client import tools
import httplib2
from apiclient import discovery
import json
from googleapiclient.http import MediaFileUpload
import mimetypes

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

from ModelCollection import ModelCollection as Collection
from IView import IView
from IController import IController
from IMediator import IMediator
from ModelVideo import ModelVideo

DEBUG = 1

cGoogleParam = {
    'SCOPES': 'https://www.googleapis.com/auth/drive',
    'CLIENT_SECRET_FILE': 'client_secrets.json',
    'CREDENTIONS_FILE': 'credentions.json',
    'APPLICATION_NAME': 'Drive API Python Quickstart',
    'CREDENTIALS':'',
    'SERVICE':'',
    'NAME_FOLDER':'0'
}

CAMERA_ADDRESS_FILE = 'camera_address.json'

class ModelGoogle:
    params = ['']
    t = Thread

class ControllerGoogle(IController):
    google = ModelGoogle()
    mediator = IMediator()
    data = any
    folder_google = any
    service = any
    name_file = ""
    numVideo = 0
    nextNumVideo = 0
    mVideo = ModelVideo(0)
    listModelVideo = [ModelVideo]
    state = "Wait"

    def __init__(self):
        self.listModelVideo.clear()
        self.google = ModelGoogle()
        self.google.params = cGoogleParam
        with open(CAMERA_ADDRESS_FILE, 'r') as file_json:
            data = json.loads(file_json.read())

    def AddMediator(self,imediator):
        self.mediator = imediator

    def ParamGoogle(self,params=['']):
        self.google.params = params

    def CredentialGoogle(self):
        if(DEBUG==1):print("Begin CredentialGoogle/ControllerGoogle",time.ctime())
        #credential_dir = os.path.join('', '.credentials')
        credential_dir = os.path.join(os.path.expanduser('~'), '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,Collection.get_value(self.google.params,'CREDENTIONS_FILE'))
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            print("credentials.invalide")
            flow = client.flow_from_clientsecrets(Collection.get_value(self.google.params,'CLIENT_SECRET_FILE'), Collection.get_value(self.google.params,'SCOPES'))
            flow.user_agent = Collection.get_value(self.google.params,'APPLICATION_NAME')
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: 
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        self.google.params.update({'CREDENTIALS': credentials})
        if(DEBUG==1):print("End CredentialGoogle/ControllerGoogle",time.ctime())

    def ServiceGoogle(self):
        if(DEBUG==1):print("Begin ServiceGoogle/ControllerGoogle",time.ctime())
        credantials = Collection.get_value(self.google.params,'CREDENTIALS')
        http = credantials.authorize(httplib2.Http())
        self.service = discovery.build('drive', 'v3', http=http)
        self.google.params.update({'SERVICE': self.service})
        if(DEBUG==1):print("End ServiceGoogle/ControllerGoogle",time.ctime())

    def FindFolderGoogle(self):
        if(DEBUG==1):print("Begin FindFolderGoogle/ControllerGoogle",time.ctime())
        #service = Collection.get_value(self.google.params,'SERVICE')
        try:
            results = self.service.files().list(pageSize=1000,fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])
            if not items:
                print('No files found.')
            else:
                for item in items:
                    #print(item['name'])
                    if item['name'] == Collection.get_value(self.google.params,'NAME_FOLDER'):
                        #print('{0} ({1})'.format(item['name'], item['id']))
                        self.folder_google = item
                        #return item
        except Exception as _ex:
            print(_ex)
        if(DEBUG==1):print("End FindFolderGoogle/ControllerGoogle ",time.ctime())

    def FindVideoPC(self):
        path_folder_pc = os.path.exists(self.data['NAME_FOLDER'])
        if path_folder_pc:
            print("0")
            
    def UploadVideo(self):
        try:
            if(DEBUG==1):print("Begin UploadVideo/ControllerGoogle")
            if(len(self.listModelVideo)==0): return 1 
            #for i in listModelVideo:
            #name_file = str(numVideo)+'.avi'
            name_file = str(self.listModelVideo[0].number)+'.avi'
            self.mVideo = self.listModelVideo[0]
            self.listModelVideo.remove(self.listModelVideo[0])
            path_folder_pc = 'video_folder'#os.path.exists(self.data['NAME_FOLDER'])
            #file_metadata = {'name': name_file, 'parents': [folder['id']]}
            for root, _, files in os.walk(path_folder_pc, topdown=True):
            #for name_file in files:
                file_metadata = {'name': name_file, 'parents': [self.folder_google['id']]}
                media = MediaFileUpload(
                    os.path.join(root, name_file),
                    mimetype=mimetypes.MimeTypes().guess_type(name_file)[0])
                self.service.files().create(body=file_metadata,media_body=media,fields='id').execute()
                #self.mVideo.state="Remove"
                self.mediator.notify("StateRemove",self.mVideo);
                print('SUCCESS UPLOAD FILE: ',name_file)
                self.state = "Update"
            if(DEBUG==1):print("End UploadVideo/ControllerGoogle")
        except Exception as _ex:
            print("Exception UploadVideo: ",_ex)

    def UpdateGoogle(self):
        while(1):
            time.sleep(1)
            if(self.state=="Update"):
                if(DEBUG==1):print("Update/ControllerGoogle begin")
                self.CredentialGoogle()
                self.ServiceGoogle()
                self.FindFolderGoogle()
                self.state = "Wait"
                self.UploadVideo()
                if(DEBUG==1):print("Update/ControllerGoogle end")

    ################################################
    def ThreadCreate(self):
        self.google.t = Thread(target = self.UpdateGoogle)
        #print('ThreadCreate: mCamera')
    def TreadStart(self):
        try:
            self.google.t.start()
            #print('TreadStart: mCamera')
        except Exception as _ex:
            print('Error TreadStart Google: ')
            print(_ex)
    def ThreadJoin(self):
        self.google.t.join();
    ################################################

class ViewGoogle(IView):
    controller = ControllerGoogle()

    def __init__(self):
        self.controller.ThreadCreate()
        self.controller.TreadStart()
        if(DEBUG==1):print("ViewGoogle init");

    def AddMediator(self,imediator):
        self.controller.AddMediator(imediator)

    def CommandMediator(self,msg,mVideo:ModelVideo):
        if(msg=="StateUploadGoogle"):
            #print("___________mVideo: ",mVideo.number)
            if(len(self.controller.listModelVideo)==0):
                self.controller.state = "Update"
            self.controller.listModelVideo.append(mVideo)

    def End(self):
        self.controller.ThreadJoin()
