
from __future__ import print_function
from fileinput import filename
import httplib2
import os

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient import discovery

import mimetypes
from googleapiclient.http import MediaFileUpload

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secrets.json'
CREDENTIONS_FILE = 'credentions.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    print("Start get_credentials")
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,CREDENTIONS_FILE)
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


#google_disk.file_upload(service=service,google_folder=google_folder,path_folder=name_folder,name_file=name_file)
def file_upload(service,google_folder,path_folder,name_file):
    print('Start file_upload')
    for root, _, files in os.walk(path_folder, topdown=True):
        #for name_file in files:
            #print(name_file)
            file_metadata = {'name': name_file, 'parents': [google_folder['id']]}
            media = MediaFileUpload(
                os.path.join(root, name_file),
                mimetype=mimetypes.MimeTypes().guess_type(name_file)[0])
            service.files().create(body=file_metadata,media_body=media,fields='id').execute()
            print('Success upload file')
                                   

def find_folder(name_folder,service):
    print("Start find_folder")
    results = service.files().list(pageSize=100,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        #print('Files:')
        for item in items:
            if item['name'] == name_folder: 
                #print('{0} ({1})'.format(item['name'], item['id']))
                return item

#def main():
#    credentials = get_credentials()
#    http = credentials.authorize(httplib2.Http())
#    service = discovery.build('drive', 'v3', http=http)

#    try:
#        google_folder = find_folder(name_folder='video_folder',service=service)
#        file_upload(service=service,google_folder=google_folder,path_volder='video_folder')
#    except Exception as _ex:
#        print(_ex)
    

#if __name__ == '__main__':
#    main()