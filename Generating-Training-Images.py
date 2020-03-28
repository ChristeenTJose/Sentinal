'''
    Create a directory named dataset before executing
'''
import cv2
import os
import shutil
model = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
os.chdir('dataset/')
Name=input('Name: ')
if os.path.exists(Name):
    print('User - ',Name,' already exists')
    print('Options: ')
    print('\n0: Overwrite')
    print('1: Append')
    print('Any other character to abort')
    append=input('\n\n')
    if append=='1':
        Files=os.listdir(Name+'/')
        Count=len(Files)+1
        Max=len(Files)+50
    elif append=='0':
        shutil.rmtree(Name)
        os.mkdir(Name)
        Count=1
        Max=50
    else:
        exit(1)
else:
    os.mkdir(Name)
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
    faces=model.detectMultiScale(gray, 1.1, 5)
    if(len(faces)==1):
      for (x,y,W,H) in faces:
        cv2.rectangle(frame,(x,y),(x+W,y+H),(0,165,255),2)
        cv2.imwrite(Name+'/' +str(Count)+".jpg", gray[y:y+H,x:x+W])
      Count+=1
    else:
        print('\tNumber of faces detected: ',len(faces))
    cv2.imshow('Sentinal',frame)
print()
VC.release()
cv2.destroyAllWindows()