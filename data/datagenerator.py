
import sys
sys.path.insert(1,'/home/pi/cam/recogniser/train')
import Dnn_train as dt
import lbp_trainer as lt

import cv2
import os
import time

import datagenerator as dataset




def datagenerator(name):
    path='/home/pi/cam/data/images/'+str(name)
    if os.path.exists(path):
        print('user already exists')
        return False
    else:
        os.mkdir(path)
        print('directory created')
        dataset.generate_dataset(path,name)
        return True



def generate_dataset(name,pname):
    cap = cv2.VideoCapture(0)
    face_classifier = cv2.CascadeClassifier("/home/pi/cam/data/frontal-face-data.xml")

    def face_cropped(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.5, 5)
        for (x, y, w, h) in faces:
            cropped_face = img[y:y + h, x:x + w]
        try:
            return cropped_face
        except:
            pass

    
    img_id = 0

    while True:
        ret, frame = cap.read()
        if face_cropped(frame) is not None:
            img_id += 1
            print('photo no '+str(img_id))
            face = cv2.resize(face_cropped(frame), (200, 200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            file_name_path = str(name)+'/'+pname+'.'+ str(img_id) + '.jpg'
            cv2.imwrite(file_name_path, face)
            cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            if int(img_id) == 200:
                break
        else:
            pass
    cap.release()
    print("Collecting samples is completed !!!")
    if(dt.train() and lt.train()):
        return True
    else:
        return False

datagenerator('sakthi')