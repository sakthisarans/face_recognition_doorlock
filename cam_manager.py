# print('hello')
import sys,os,time,cv2,glob
from threading import Thread
sys.path.insert(0,'/home/pi/cam/model')
sys.path.insert(1,'/home/pi/cam/recogniser/predict')
sys.path.insert(2,'/home/pi/cam/telebot')
sys.path.insert(3,'/home/pi/cam/gpiocontrol')
sys.path.insert(3,'/home/pi/cam')
import db_manager as dbm
import warner
import pincontrol as pc
import dateandtime as dtm
import Dnn_model as Dnn
import Dnn_predict as pred
import lbp
import imutils
import cam_manager as cm
import RPi.GPIO as gpio


pir=10
gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
gpio.setup(pir,gpio.IN)


 
img_path='/home/pi/cam/data/images'

dir=os.listdir(img_path)
person_count=(dir.__len__())
try:
    model=Dnn.model_generate(person_count)
    model.load("/home/pi/cam/model/saves/Dnn/Dnnmodel.h5")
except Exception as ex:
    print(ex)

def face_cropped(img):
        face_classifier = cv2.CascadeClassifier("/home/pi/cam/data/frontal-face-data.xml")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.5, 5)
        for (x, y, w, h) in faces:
            cropped_face = img[y:y + h, x:x + w]
        try:
            return cropped_face
        except:
            pass
def prepare():
    i=1
    cap=cv2.VideoCapture(0)
    face_classifier = cv2.CascadeClassifier("/home/pi/cam/data/frontal-face-data.xml")
    while(i<11): 
        ret, frame = cap.read()
        val=face_cropped(frame)
        if val is not None:
            print(str(i)+"=========================================")
            path=f"/home/pi/cam/predicton_images/image{i}.jpg"
            cv2.imwrite(path,frame)
            i+=1
        else:
            pass
    cap.release()

dnn_out=''
lbp_out=''
class camera():

    def Dnn(self):
        res=''
        dnn_out=(pred.Dnn_predict(model))
        try:
            res = max(set(dnn_out), key = dnn_out.count)
        except Exception as ex:
            print('by-dnn')
            print(ex)
            cm.dnn_out='dnn-sss'
        cm.dnn_out=res
        # cm.dnn_out='dnn-sss'
        # print('dnn-sss')

    def lbp(self):
        res=''
        lbp_out=lbp.predict()
        try:
            res = max(set(lbp_out), key = lbp_out.count)
        except Exception as ex:
            print('by-lbp')
            print(ex)
            cm.lbp_out='sss'
        cm.lbp_out=res
        # cm.lbp_out='sss'
        # print('sss')

    def eigen(self):
        print('eigen')

def main():
    try:
        while(True):
            pir_val=gpio.input(pir)
            print(cm.lbp_out+"--"+cm.dnn_out)
            print(pir_val)
            if(pir_val):
                cm.prepare()
                Yep = camera()
                thread1 = Thread(target = Yep.Dnn)
                thread2 = Thread(target = Yep.lbp)
                thread3 = Thread(target = Yep.eigen)
                thread1.start()
                thread2.start()
                thread3.start()
                b=True
                while(b):
                    if((not thread1.is_alive()) and (not thread2.is_alive()) and (not thread3.is_alive())):
                        # cm.lbp_out='sss'
                        # cm.dnn_out='dnn-sss'

                        print(cm.lbp_out+"=="+cm.dnn_out)
                        if(cm.lbp_out!='unknown' and cm.dnn_out!='unknown'):
                            message=(cm.dnn_out+" accessed door in "+dtm.find_date()+' at '+dtm.find_time())
                            dbm.updater(cm.dnn_out,'automatic')
                            warner.warning_sender(message)
                            pc.relayon()
                            time.sleep(10)
                            pc.relayoff()
                        else:
                            message=("unknown person try to accessed door in "+dtm.find_date()+' at '+dtm.find_time()+'\n'
                                    'the images of the person is attched above')
                            out=[]
                            file=glob.glob('/home/pi/cam/predicton_images/*')
                            random.shuffle(file)
                            for i in file[:3] :
                                img=(i.replace('\\','/'))
                                out.append(img)
                            warner.warning_sender(message, out)

                        files=glob.glob('/home/pi/cam/predicton_images/*')
                        for f in files:
                            os.remove(f)
                        cm.lbp_out=''
                        cm.dnn_out=''
                        b=False     
            time.sleep(2)
    except Exception as ex:
        print(ex)
        main()

if __name__=='__main__':
    main()