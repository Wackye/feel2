### test code for switch, not yet finish


### GPIO04  (Pin 7) for led control (untested)
### GPIO18  (Pin12) for flip switch (untested)

# Import libraries
import RPi.GPIO as GPIO
import time

led = 27
switch = 17

# Set GPIO numbering mode
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Set pin 11 as an output, and define as servo1 as PWM pin
GPIO.setup(led,GPIO.OUT)
GPIO.setup(switch,GPIO.IN)
#led = GPIO.PWM(7,50) # pin 11 for servo1, pulse 50Hz

# Start PWM running, with value of 0 (pulse off)
#led.start(0)

val = 0
mean = 0.0
state = False



try:
    while True:
        #Ask user for angle and turn servo to it
#         time.sleep(0.2)
#         time.sleep(0.2)
        tmp = GPIO.input(switch)
        if(tmp == 1):
            state = True
            mean = 1
        elif(tmp == 0):
            mean -= 0.01;
            if(mean > 0):
                state = True             
            else:
                state = False
                mean = 0
        # if(val != tmp):
        if(state):
            GPIO.output(led, GPIO.HIGH)
        elif(state == False):
            GPIO.output(led, GPIO.LOW)
        val = tmp   
        print('status:  ', tmp)
        # time.sleep(0.5)        
        
finally:
    #Clean things up at the end with ctrl + C
#    led.stop()
#    switch.stop()
#     GPIO.cleanup()
    print("Goodbye!")