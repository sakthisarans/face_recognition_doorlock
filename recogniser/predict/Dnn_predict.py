import time,cv2
import numpy as np
import logging,os,sys
import Dnn_predict as dp

img_path='/home/pi/cam/data/images'

formating=logging.Formatter("%(asctime)s - %(name)s - %(pathname)s - %(threadName)s - %(message)s")
fh=logging.FileHandler("/home/pi/cam/log/Dnn_errors.log")
fh.setFormatter(formating)
log=logging.getLogger("Dnn_errorlog")
log.setLevel(logging.ERROR)
log.addHandler(fh)

formating=logging.Formatter('%(name)s - %(message)s')
fh=logging.FileHandler("/home/pi/cam/log/Dnn_outputdata.log")
fh.setFormatter(formating)
out=logging.getLogger("Dnn_outlog")
out.setLevel(logging.INFO)
out.addHandler(fh)



try:
    face_classifier = cv2.CascadeClassifier("/home/pi/cam/recogniser/predict/frontal-face-data.xml")
except Exception as ex:
    print('error'+ex)
def face_cropped(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.5, 5)
        for (x, y, w, h) in faces:
            cropped_face = img[y:y + h, x:x + w]
        try:
            # print('val')
            return cropped_face
        except:
            # print('none')
            pass


# try:
#     cap1=cv2.VideoCapture(0)
# except Exception as ex:
#     logi.error(ex)


def Dnn_predict(model):
    try:
        list=[]
        print(str(model))     
        count=0
        img_path="/home/pi/cam/predicton_images"
        for root, dirs, files in (os.walk(img_path)):
            for img in files:
                path1 = os.path.join(root, img)
                frame = cv2.imread(path1)
                # print(path1)
                des=dp.face_cropped(frame)
                # print("crop")
                # print(des)
                if des is not None:
                    face = cv2.resize(face_cropped(frame), (200,200))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    img_data = cv2.resize(face, (50,50))
                    data = img_data.reshape(50,50,1)
                    
                    model_out=model.predict([data])[0]
                    count+=1
                    write=str(np.argmax(model_out))+"-----"+str(model_out)
                    index=np.argmax(model_out)
                    # print(write+'='+str(np.max(model_out)))
                    lable=dir=os.listdir("/home/pi/cam/data/images")
                    if ((np.max(model_out)>0.9995 and np.max(model_out)<1.00) or (np.max(model_out)>0.85 and np.max(model_out)<0.95) ):
                        my_label=lable[index]
                        write=str(write+"-----"+my_label)
                        out.info(write)
                        # print(str(index)+"-"+str(my_label))
                        list.append(str(my_label))
                    else:
                        out.info(write+"-----unknown")
                        list.append('unknown')

                    
        return list
    except Exception as ex:
        log.error(ex)
