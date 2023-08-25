

image_dir='/home/pi/cam/data/images'

#requirement
#pip install pillow

import cv2
import os
import numpy as np
from PIL import Image
import pickle
import time
def train():
	
	face_cascade = cv2.CascadeClassifier('/home/pi/cam/recogniser/train/frontal-face-data.xml')
	recognizer = cv2.face.LBPHFaceRecognizer_create()

	current_id = 0
	label_ids = {}
	y_labels = []
	x_train = []

	for root, dirs, files in os.walk(image_dir):
		print(files)
		for file in files:
			if file.endswith("png") or file.endswith("jpg"):
				path = os.path.join(root, file)
				print(path)
				label = os.path.basename(root).replace(" ", "-").lower()
				print(str(label)+"---"+str(label_ids))
				if not label in label_ids:
					label_ids[label] = current_id
					current_id += 1
					print(str(label) + "----" + str(label_ids))
				id_ = label_ids[label]
				print(id_)
				img=Image.open(path)
				image_array = np.array(img, "uint8")
				print(image_array)
				faces = face_cascade.detectMultiScale(image_array)
				print(faces)
				for (x, y, w, h) in faces:
					roi = image_array[y:y + h, x:x + w]
					x_train.append(roi)
					y_labels.append(id_)

	with open("/home/pi/cam/model/saves/lbp/labels.pickle", 'wb') as f:
		pickle.dump(label_ids, f)
	print(str(x_train),end='\r')
	recognizer.train(x_train, np.array(y_labels))
	recognizer.save("/home/pi/cam/model/saves/lbp/face-trainner.yml")
	return ('model2 trained successfullty!!!')
	return True
# train()