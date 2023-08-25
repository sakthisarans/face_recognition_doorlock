import time
import sys
import cv2
import pickle
import os,logging
import numpy as np



formating=logging.Formatter("%(asctime)s - %(name)s - %(pathname)s - %(threadName)s - %(message)s")
fh=logging.FileHandler("/home/pi/cam/log/lbp_errors.log")
fh.setFormatter(formating)
lbp_log=logging.getLogger("lbp_errorlog")
lbp_log.setLevel(logging.ERROR)
lbp_log.addHandler(fh)

formating=logging.Formatter('%(name)s - %(message)s')
fh=logging.FileHandler("/home/pi/cam/log/lbp_outputdata.log")
fh.setFormatter(formating)
lbp_out=logging.getLogger("lbp_outlog")
lbp_out.setLevel(logging.INFO)
lbp_out.addHandler(fh)
try:
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("/home/pi/cam/model/saves/lbp/face-trainner.yml")
except Exception as ex:
    lbp_log.error(ex)

img_path="/home/pi/cam/predicton_images"

try:
    face_cascade = cv2.CascadeClassifier("/home/pi/cam/recogniser/predict/frontal-face-data.xml")
except Exception as ex:
    print('==========================='+ex)


value=False

labels = {"person_name": 0}
with open("/home/pi/cam/model/saves/lbp/labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v: k for k, v in og_labels.items()}

print(labels)
# try:
#     cap = cv2.VideoCapture(0)
# except Exception as ex:
#     lbp_log.error(ex)
def predict():


    def face_cropped(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite("./img.jpg",gray)
        faces = face_cascade.detectMultiScale(gray, 1.5, 5)
        for (x, y, w, h) in faces:
            cropped_face = img[y:y + h, x:x + w]
        try:
            
            cropped_face = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2GRAY)
            # cv2.imwrite("./img1.jpg",cropped_face)
            return cropped_face
            
        except:
            # print('pass')
            pass
    
    print('lbp on')
    outname=[]
    count = 0
    pos=0
    neg=0
    name=""
    for root, dirs, files in (os.walk(img_path)):
        
        for img in files:
            path1 = os.path.join(root, img)
            # print(path1)
            frame = cv2.imread(path1)
            
            roi_gray=face_cropped(frame)
            if roi_gray is not None:
                id_, conf = recognizer.predict(roi_gray)
                
                # print(str(id_)+"---"+str(conf))
                if conf >= 30 and conf <= 56:
                    pos+=1
                    name=labels[id_]
                    name = labels[id_]
                    outname.append(name)
                    write=str('positive------->'+str(conf)+"==="+name)
                    lbp_out.info(write)
                else:
                    neg+=1
                    write=str('negative------->'+str(conf))
                    outname.append('unknown')
                    print('appended')
                    lbp_out.info(write)
        print(outname)
        print('lbp outttttt')        
        return outname;
        

# print(predict())