import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
while(True):
	GPIO.output(18,GPIO.LOW)
	time.sleep(1)
	GPIO.output(18,GPIO.HIGH)
	time.sleep(1)
#GPIO.cleanup()
