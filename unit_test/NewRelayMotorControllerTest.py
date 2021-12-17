### +N原本的測試檔案

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

### setup LED pin
#GPIO.setup(4,GPIO.OUT)
#GPIO.output(4,GPIO.LOW)
### setup LED pin
GPIO.setup(4,GPIO.OUT)
led1 = GPIO.PWM(4,200)
led1.start(0)
# Set pin 11 as an output, and define as servo1 as PWM pin
GPIO.setup(17,GPIO.OUT)
servo1 = GPIO.PWM(17,50) # pin 11 for servo1, pulse 50Hz
# Start PWM running, with value of 0 (pulse off)
servo1.start(0)

### setup Motor control relay pin
GPIO.setup(5,GPIO.OUT)
GPIO.output(5,GPIO.LOW)
GPIO.setup(6,GPIO.OUT)
GPIO.output(6,GPIO.LOW)
GPIO.setup(13,GPIO.OUT)
GPIO.output(13,GPIO.LOW)
GPIO.setup(19,GPIO.OUT)
GPIO.output(19,GPIO.LOW)
GPIO.setup(26,GPIO.OUT)
GPIO.output(26,GPIO.LOW)

### test play the whole plate

### turn on led light
#GPIO.output(4,GPIO.HIGH)
led1.ChangeDutyCycle(15)

servo1.ChangeDutyCycle(2+(0/18))
GPIO.output(26,GPIO.HIGH)
time.sleep(34)
GPIO.output(26,GPIO.LOW)

servo1.ChangeDutyCycle(2+(75/18))
GPIO.output(19,GPIO.HIGH)
time.sleep(27)
GPIO.output(19,GPIO.LOW)

servo1.ChangeDutyCycle(2+(105/18))
GPIO.output(13,GPIO.HIGH)
time.sleep(21)
GPIO.output(13,GPIO.LOW)

servo1.ChangeDutyCycle(2+(135/18))
GPIO.output(6,GPIO.HIGH)
time.sleep(15)
GPIO.output(6,GPIO.LOW)

servo1.ChangeDutyCycle(2+(165/18))
GPIO.output(5,GPIO.HIGH)
time.sleep(9)
GPIO.output(5,GPIO.LOW)

### turn off led light
#GPIO.output(4,GPIO.LOW)
led1.ChangeDutyCycle(0)

#Clean things
servo1.stop()
led1.stop()
GPIO.cleanup()
