import cv2
import os
import numpy as np
from PIL import Image
model_recognizer=cv2.face.LBPHFaceRecognizer_create()
model_detector=cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
Categories=os.listdir('dataset/')
X=[]
Y=[]
LabelEncoder={Categories[i]:i for i in range(len(Categories))}
Count=0
for Directory in Categories:
    Filenames= os.listdir('dataset/'+Directory+'/')
    FilePaths=['dataset/'+Directory+'/'+Filename for Filename in Filenames]
    for ImagePath in FilePaths:
        print('\nProcessing image: '+ImagePath,end='')
        PIL_Image=Image.open(ImagePath).convert('L')#Convert it to grayscale
        numpy_Array = np.array(PIL_Image,'uint8')
        faces = model_detector.detectMultiScale(numpy_Array, 1.3, 5)
        print('\nNumber of faces found: ',len(faces))
        if(len(faces)==1):
            for (x,y,W,H) in faces:
                X.append(numpy_Array[y:y+H,x:x+W])
                Y.append(LabelEncoder[Directory])
            Count+=1
    print('\n\nRecogniser has been trained on ',Count,' images of ',Directory)
model_recognizer.train(X, np.array(Y))
model_recognizer.save('Recogniser.yml')

