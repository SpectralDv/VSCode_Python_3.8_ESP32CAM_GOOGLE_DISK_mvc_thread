

import cv2
import time
import google_disk 
import os
import json
import httplib2
from apiclient import discovery
from threading import *
from ModelCamera import ControllerCamera


CAMERA_ADDRESS_FILE = 'camera_address.json'

eventUpload = False
name_file = ''

def camera_move(path_cap,name_folder):

    print('Start Programm')

    capController = ControllerCamera()
    cap = cv2.VideoCapture(path_cap)

    time.sleep(1)

    print("Start Cap")

    eventStart = True
    eventVideo = False
    countVideo = 0
    frameVideo = 100
    fps = 30.0
    image_size = (320,240)
    video_file = str(name_folder)+'/res.avi'

    out = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'XVID'), fps, image_size) 
    
    #ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    time.sleep(1)

    countMove = 0
    countFrame = 0
    
    while cap.isOpened():

        global name_file
        global eventUpload

        frame1 = frame2 
        ret, frame2 = cap.read() 

        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0) # фильтрация лишних контуров
        a,thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY) # метод для выделения кромки объекта белым цветом
        dilated = cv2.dilate(thresh, None, iterations = 3) #расширяет выделенную на предыдущем этапе область
        сontours,b = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # нахождение массива контурных точек

        for contour in сontours:
            (x, y, w, h) = cv2.boundingRect(contour) # преобразование массива из предыдущего этапа в кортеж из четырех координат

            if cv2.contourArea(contour) < 700: # условие при котором площадь выделенного объекта меньше 700 px
                countMove = 0;
                continue
                
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2) # получение прямоугольника из точек кортежа
            cv2.putText(frame1, "Status: {}".format("Dvigenie"), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA) #текст
            countMove += 1;

        #print(count)
        cv2.imshow("frame1", frame1)

        if countMove > 1:
            eventVideo = True

        if countFrame > frameVideo:
            video_file = str(name_folder)+'/res'+str(countVideo)+'.avi'
            out = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'XVID'), fps, image_size)   

            pred_count = countVideo-1
            if (pred_count<0): pred_count=0
            pred_pred_count = pred_count - 1
            if (pred_pred_count<0): pred_pred_count=0
            
            if eventStart == False and pred_pred_count >= 0:
                path = os.path.join(os.path.abspath(os.path.dirname(__file__)), str(name_folder)+'/res'+str(pred_pred_count)+'.avi')
                if path:
                    try:
                        os.remove(path)
                    except Exception as _ex:
                        print("remove ",'/res'+str(pred_pred_count)+'.avi ',_ex)

            if eventStart:
                path = os.path.join(os.path.abspath(os.path.dirname(__file__)), str(name_folder)+'/res.avi')
                if path:
                    os.remove(path)
                    eventStart = False

            name_file = 'res'+str(pred_count)+'.avi'
            eventUpload = True
            #google_upoload('res'+str(pred_count)+'.avi',name_folder)

            countVideo += 1
            print(str(countVideo) + ".Change count video")
            countFrame = 0
            eventVideo = False
        
        if eventVideo == True:
            countFrame += 1
            #ret, frame = cap.read()
            out.write(frame1)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


#def google_upoload(name_file,name_folder):
def google_upoload():
    global name_file
    global eventUpload
    name_folder = "video_folder"
    print('Start Google')
    credentials = google_disk.get_credentials()
    print(credentials)
    http = credentials.authorize(httplib2.Http())
    
    while(True):
        if eventUpload == True:
            try:
                service = discovery.build('drive', 'v3', http=http)
                google_folder = google_disk.find_folder(name_folder=name_folder,service=service)
                google_disk.file_upload(service=service,google_folder=google_folder,path_folder=name_folder,name_file=name_file)
                eventUpload = False
            except Exception as _ex:
                eventUpload = False
                print(_ex)
        if eventUpload == False:
            time.sleep(0.5)

def main():

    with open(CAMERA_ADDRESS_FILE, 'r') as file_json:
        data = json.loads(file_json.read())

    path_folder = os.path.exists(data['name_folder'])
    if path_folder:
        for file in os.scandir(data['name_folder']):
            print(file.name)
            if file.name.endswith(".avi"):
                os.unlink(file.path)

    if(os.path.exists(data['name_folder'])):
        os.rmdir(data['name_folder'])
    os.mkdir(data['name_folder'])

    time.sleep(1)

    t1 = Thread(target = camera_move,args = (data['camera_address'],data['name_folder']))
    #t2 = Thread(target = google_upoload)

    t1.start();
    time.sleep(1)
    #t2.start();

    t1.join();
    #t2.join();

    #camera_move(data['camera_address'],data['name_folder'])

if __name__ == '__main__':
    main()