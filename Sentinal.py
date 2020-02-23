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
GPIO.setup(18,GPIO.OUT)
model_recognizer=cv2.face.LBPHFaceRecognizer_create()
model_recognizer.read('Recogniser.yml')
model_detector=cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
Categories=os.listdir('dataset/')
InverseLabelEncoder={i:Categories[i] for i in range(len(Categories))}
Font = cv2.FONT_HERSHEY_SIMPLEX
VC = cv2.VideoCapture(0)
while True:
    print(count)
    return_value,frame = VC.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=model_detector.detectMultiScale(gray, 1.1, 5)
    for (x,y,W,H) in faces:
        count+=1
        cv2.rectangle(frame,(x-20,y-20),(x+W+20,y+H+20),(0,255,0),4)
        Name=model_recognizer.predict(gray[y:y+H,x:x+W])
        if Name in InverseLabelEncoder:
            Name=InverseLabelEncoder[Name]
            GPIO.output(18,GPIO.LOW)
        else:
            print(Name)
            Name='Intruder'
            i=1
            while(i<=3):
                GPIO.output(18,GPIO.LOW)
                time.sleep(0.1)
                if i==1:
                    cv2.rectangle(frame, (x-22,y-90), (x+W+22, y-22), (0,255,0), -1)
                    cv2.putText(frame,Name, (x,y-40), Font, 2, (255,255,255), 3) 
                    Name+='/'+str(datetime.datetime.now())
                    cv2.imwrite(Name+".jpg",gray[y:y+H,x:x+W])
                GPIO.output(18,GPIO.HIGH)
                if i!=3:
                    time.sleep(0.1)
            i+=1
            GPIO.cleanup()
            print(Name)
    if cv2.waitKey(0):
        VC.release()
        cv2.destroyAllWindows()
        break