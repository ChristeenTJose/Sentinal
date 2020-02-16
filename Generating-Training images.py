import cv2
import matplotlib.pyplot as plt
model = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
ID=1
Max=50
Count=1
VC = cv2.VideoCapture(0)
while(Count<=Max):
    print('\nProcessing image: ',Count,end='')
    return_value,frame = VC.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=model.detectMultiScale(gray, 1.3, 5)
    if(len(faces)==1):
      for (x,y,W,H) in faces:
        cv2.rectangle(frame, (x,y), (x+W,y+H), (255,0,0), 2)
        cv2.imwrite("dataset/User." +str(ID)+str(Count)+".jpg", gray[y:y+H,x:x+W])
      Count+=1
    else:
        print('\tNumber of faces detected: ',len(faces))
VC.release()
cv2.waitKey(0)
cv2.destroyAllWindows()