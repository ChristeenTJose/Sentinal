import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14,GPIO.OUT)
try:
    while(True):
        GPIO.output(14,GPIO.LOW)
        time.sleep(1)
        GPIO.output(14,GPIO.HIGH)
        time.sleep(1)               
except KeyboardInterrupt:
    GPIO.cleanup()
