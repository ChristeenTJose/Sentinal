import cv2
import os
import numpy as np
from PIL import Image
model_recognizer=cv2.face.LBPHFaceRecognizer_create(1,8,8,8,75)
'''
Default values:
    radius = 1
    neighbors = 8
    grid_x = 8
    grid_y = 8   
Threshold value: 80
'''
Categories=os.listdir('dataset/')
X=[]
Y=[]
LabelEncoder={Categories[i]:i+1 for i in range(len(Categories))}
for Directory in Categories:
    Count=0
    Filenames= os.listdir('dataset/'+Directory+'/')
    FilePaths=['dataset/'+Directory+'/'+Filename for Filename in Filenames]
    for ImagePath in FilePaths:
        PIL_Image=Image.open(ImagePath).convert('L')#Convert it to grayscale
        numpy_Array = np.array(PIL_Image,'uint8')
        X.append(numpy_Array)
        Y.append(LabelEncoder[Directory])
        Count+=1
    print('Recogniser will be trained on ',Count,' images of ',Directory,'\n\n')
model_recognizer.train(X,np.array(Y))
model_recognizer.save('Recogniser.yml')

