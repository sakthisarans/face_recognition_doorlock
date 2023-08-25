import numpy as np
import os,cv2
from random import shuffle
from tqdm import tqdm
import sys
sys.path.insert(0,'/home/pi/cam/model')
import Dnn_model as Dnn

img_path='/home/pi/cam/data/images'
current_id=0

def arr_gen():
    dir=os.listdir(img_path)
    print(dir.__len__())
    dir.sort
    arr=[]
    for i in dir:
        arr.append(0)
    return arr

def my_label1(image_name):
    name = image_name.split('.')[-3] 
    dir=os.listdir(img_path)
    ind=dir.index(name)
    print(ind)
    tarr=arr_gen()
    tarr[ind]=1
    return(np.array(tarr))

def my_data():
    data = []
    for root, dirs, files in (os.walk(img_path)):
        
        for img in files:
            path=root+"\\"
            path=os.path.join(root,img)
            print(path)
            img_data = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            img_data = cv2.resize(img_data, (50,50))
            data.append([np.array(img_data), my_label1(img)])
            print(str(my_label1(img)))
    shuffle(data)  
    return data

def train():

    data = my_data()
    print(data)

    train = data[:200]  
    test = data[200:]
    X_train = np.array([i[0] for i in train]).reshape(-1,50,50,1)
    print(X_train.shape)
    y_train = [i[1] for i in train]
    X_test = np.array([i[0] for i in test]).reshape(-1,50,50,1)
    print(X_test.shape)
    print(y_train)
    y_test = [i[1] for i in test]

    dir=os.listdir(img_path)
    person_count=(dir.__len__())
    model=Dnn.model_generate(person_count)
    try:
        model.fit(X_train, y_train, n_epoch=12, validation_set=(X_test, y_test), show_metric = True, run_id="FRS" )
    except Exception as ex:
        print(ex)
    model.save("/home/pi/cam/model/saves/Dnn/Dnnmodel.h5")
    return 'model1 trained successfully!!!'
    return True

# train()
