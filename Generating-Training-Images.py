'''
    Create a directory named dataset before executing
'''
import cv2
import matplotlib.pyplot as plt
import os
import shutil
model = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
os.chdir('dataset/')
Name=input('Name: ')
if os.path.exists(Name):
    shutil.rmtree(Name)
os.mkdir(Name)
Max=50
Count=1
VC = cv2.VideoCapture(0)
'''
cv.waitKey(delay=0)
Delay in milliseconds. 0 is the special value that means “forever”.
It returns the code of the pressed key or -1 if no key was pressed before the specified time had elapsed.
'''
while(cv2.waitKey(1)==-1 and Count<=50):
    print('\nProcessing image: ',Count,end='')
    return_value,frame = VC.read()
    cv2.imshow('Sentinal',frame)
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=model.detectMultiScale(gray, 1.1, 5)
    if(len(faces)==1):
      for (x,y,W,H) in faces:
        cv2.rectangle(frame, (x,y), (x+W,y+H), (255,0,0), 2)
        cv2.imwrite(Name+'/' +str(Count)+".jpg", gray[y:y+H,x:x+W])
      Count+=1
    else:
        print('\tNumber of faces detected: ',len(faces))
    cv2.imshow('Sentinal',frame)
VC.release()
print() 
cv2.destroyAllWindows()