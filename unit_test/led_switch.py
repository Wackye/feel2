### test code for switch, not yet finish


### GPIO04  (Pin 7) for led control (untested)
### GPIO18  (Pin12) for flip switch (untested)

# Import libraries
import RPi.GPIO as GPIO
import time

led = 7
switch = 18

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 11 as an output, and define as servo1 as PWM pin
GPIO.setup(led,GPIO.OUT)
GPIO.setup(switch,GPIO.IN)
#led = GPIO.PWM(7,50) # pin 11 for servo1, pulse 50Hz

# Start PWM running, with value of 0 (pulse off)
#led.start(0)

val = 0

try:
    while True:
        #Ask user for angle and turn servo to it
        GPIO.output(led, GPIO.HIGH)
#         time.sleep(0.2)
#         time.sleep(0.2)
        tmp = GPIO.input(switch)
#         if(val != tmp):
        print('status:  ', tmp)
        val = tmp
        time.sleep(0.2)        
        
finally:
    #Clean things up at the end with ctrl + C
#    led.stop()
#    switch.stop()
#     GPIO.cleanup()
    print("Goodbye!")