import picamera
camera=picamera.PiCamera()
camera.vflip=True
camera.capture('example.jpg')
