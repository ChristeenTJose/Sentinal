'''
    Create a directory named "dataset" before executing
    Create a directory named "intruder" before executing
'''
import cv2
import os
import shutil
import numpy as np
from PIL import Image
import RPi.GPIO as GPIO
import time
import datetime
model_detector=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
model_recognizer=cv2.face.LBPHFaceRecognizer_create(1,8,8,8,55)
'''
    Default values:
    radius = 1
    neighbors = 8
    grid_x = 8
    grid_y = 8   
    Threshold value: 80
'''
def Generate_Training_Images():
    print('\n\n\t\t\tGenerate Training Images\n\n')
    Name=input('Name: ')
    if os.path.exists('dataset/'+Name):
        print('User - ',Name,' already exists')
        print('Options: ')
        print('\n0: Overwrite')
        print('1: Append')
        print('Any other character to abort')
        append=input('\n\n')
        if append=='1':
            Files=os.listdir('dataset/'+Name+'/')
            Count=len(Files)+1
            Max=len(Files)+50
        elif append=='0':
            shutil.rmtree('dataset/'+Name)
            os.mkdir('dataset/'+Name)
            Count=1
            Max=50
        else:
            exit(1)
    else:
        os.mkdir('dataset/'+Name)
        Count=1
        Max=50
    VC = cv2.VideoCapture(0)
    '''
    cv.waitKey(delay=0)
    Delay in milliseconds. 0 is the special value that means “forever”.
    It returns the code of the pressed key or -1 if no key was pressed before the specified time had elapsed.
    '''
    while(cv2.waitKey(1)==-1 and Count<=Max):
        print('\nProcessing image: ',Count,end='')
        return_value,frame = VC.read()
        cv2.imshow('Sentinal',frame)
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces=model_detector.detectMultiScale(gray, 1.1, 5)
        if(len(faces)==1):
          for (x,y,W,H) in faces:
            cv2.rectangle(frame,(x,y),(x+W,y+H),(0,165,255),2)
            cv2.imwrite('dataset/'+Name+'/' +str(Count)+".jpg", gray[y:y+H,x:x+W])
          Count+=1
        else:
            print('\t\tNumber of faces detected: ',len(faces))
        cv2.imshow('Sentinal',frame)
    print()
    VC.release()
    cv2.destroyAllWindows()
def Training_Recogniser():
    print('\n\n\t\t\tTraining Recogniser')
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
        print('\n\nRecogniser will be trained on ',Count,' images of ',Directory,'\n\n')
    print('Training recogniser...')
    model_recognizer.train(X,np.array(Y))
    print('\n\nTraining completed')
    print('\n\nSaving recogniser....')
    model_recognizer.save('Recogniser.yml')
    print('\n\nRecogniser saved successfully !!!')
def Sentinal():
    print('\n\n\t\t\tSentinal\n\n')
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(14,GPIO.OUT)#Buzzer
    GPIO.setup(15,GPIO.OUT)#RED LED
    GPIO.setup(23,GPIO.OUT)#GREEN LED
    GPIO.output(14,GPIO.HIGH)
    GPIO.output(15,GPIO.LOW)
    GPIO.output(23,GPIO.HIGH)
    model_recognizer.read('Recogniser.yml')
    Categories=os.listdir('dataset/')
    InverseLabelEncoder={i+1:Categories[i] for i in range(len(Categories))}
    Font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    VC = cv2.VideoCapture(0)
    while cv2.waitKey(1)==-1:
        return_value,frame = VC.read()
        cv2.imshow('Sentinal',frame)
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=model_detector.detectMultiScale(gray, 1.1, 5)
        for (x,y,W,H) in faces:
            Name,Confidence=model_recognizer.predict(gray[y:y+H,x:x+W])
            if Name in InverseLabelEncoder:
                Name=InverseLabelEncoder[Name]
                GPIO.output(15,GPIO.LOW)
                GPIO.output(23,GPIO.HIGH)
                Color=(0,255,0)
            else:#-1
                Name='Intruder'
                GPIO.output(15,GPIO.HIGH)
                GPIO.output(23,GPIO.LOW)
                Color=(0,0,255)
                FilePath='intruder/'+str(datetime.datetime.now())
                cv2.imwrite(FilePath+".jpg",frame)
                i=1
                while(i<=4):
                    GPIO.output(14,GPIO.LOW)
                    time.sleep(0.1)
                    GPIO.output(14,GPIO.HIGH)
                    if i!=4:
                        time.sleep(0.1)
                    i+=1
            print(Name,'-----',Confidence)
            cv2.putText(frame,Name, (x,y-40), Font, 2,Color,1) 
            cv2.rectangle(frame,(x-20,y-20),(x+W+20,y+H+20),Color,2)
        cv2.imshow('Sentinal',frame)
    GPIO.cleanup()
    VC.release()
    cv2.destroyAllWindows()
print('\t\t\tSENTINAL')
terminate=0
while terminate==0:
    choice=input('\nOptions:\n\n1. Generate Training Images\n2. Train Recogniser\n3. Launch Sentinal\n\n   [Any other character to terminate]\n\n')
    if choice not in [str(i) for i in range(1,4)]:
        terminate=1
    elif choice=='1':
        Generate_Training_Images()
    elif choice=='2':
        Training_Recogniser()
    else:
        Sentinal()
        