### servo test code 


# Import libraries
import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 11 as an output, and define as servo1 as PWM pin
GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50) # pin 11 for servo1, pulse 50Hz

# Start PWM running, with value of 0 (pulse off)
servo1.start(0)

# Loop to allow user to set servo angle. Try/finally allows exit
# with execution of servo.stop and GPIO cleanup :)

## 0 65 105 140 170

try:
    while True:
        #Ask user for angle and turn servo to it
        angle = float(input('Enter angle between 0 & 180: '))
        servo1.ChangeDutyCycle(2+(angle/18))
        time.sleep(0.5)
#         servo1.ChangeDutyCycle(0)

finally:
    #Clean things up at the end with ctrl + C
    servo1.stop()
    GPIO.cleanup()
    print("Goodbye!")

##################################################################

### GPIO17 (Pin11) for servo PWM

### GPIO23 (Pin16) for motor controlA
### GPIO24 (Pin18) for motor controlB
### GPIO25 (Pin22) for motor control PWM

### GPIO04  (Pin 7) for led control (untested)
### GPIO18  (Pin12) for flip switch (untested)

### usb for qr code scanner (GM67)

##################################################################

#import RPi.GPIO as GPIO
#import time

#GPIO.setmode(GPIO.BCM)

#GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#while True:
#    input_state = GPIO.input(18)
#    if input_state == False:
#        print('Button Pressed')
#        time.sleep(0.2)
