### motor test code

import RPi.GPIO as GPIO          
from time import sleep

in1 = 24
in2 = 23
en = 25 ### who is en?
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)

### 到時候是
p.start(50)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    

### tier 5: bpm 30, 9 slot
### tier 4: bpm 55, 15 slot
### tier 3: bpm 78, 21 slot
### tier 2: bpm 105, 27 slot
### tier 1: bpm 124, 33 slot
sum

while(1):

    x=input('enter command code:')
    if x=='r':
        print("run")
        if(temp1==1):
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         print("forward")
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         print("backward")
         x='z'

    elif x=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        temp1=1
        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        temp1=0
        x='z'

    elif x=='l':
        print("low")
        p.ChangeDutyCycle(43)
        x='z'

    elif x=='m':
        print("medium")
        p.ChangeDutyCycle(60)
        x='z'

    elif x=='h':
        print("high")
        p.ChangeDutyCycle(90)
        x='z'
     
    
    elif x=='e':
        GPIO.cleanup()
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")
