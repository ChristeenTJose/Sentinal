'''
    Create a directory named "intruder" before execution
'''
import cv2
import os
import RPi.GPIO as GPIO
import time
import datetime
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14,GPIO.OUT)
model_recognizer=cv2.face.LBPHFaceRecognizer_create(1,8,8,8,75)
model_recognizer.read('Recogniser.yml')
model_detector=cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
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
            GPIO.output(14,GPIO.LOW)
            Color=(0,255,0)
        else:
            Name='Intruder'
            FilePath='intruder/'+str(datetime.datetime.now())
            cv2.imwrite(FilePath+".jpg",frame[y:y+H,x:x+W])
            Intruder=cv2.imread(FilePath+".jpg")
            cv2.imshow('Sentinal-Intruders',Intruder)
            Color=(0,0,255)
            i=1
            while(i<=3):
                GPIO.output(14,GPIO.LOW)
                time.sleep(0.1)
                GPIO.output(14,GPIO.HIGH)
                if i!=5:
                    time.sleep(0.1)
                i+=1
            Name='Intruder'
        print(Name,'-----',Confidence)
        cv2.putText(frame,Name, (x,y-40), Font, 2,Color,1) 
        cv2.rectangle(frame,(x-20,y-20),(x+W+20,y+H+20),Color,2)
        cv2.imshow('Sentinal',frame)
GPIO.cleanup()
VC.release()
cv2.destroyAllWindows()