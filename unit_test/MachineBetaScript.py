### autorun on startup using Terminal> sudo nano /etc/rc.local > added path, remove to cancel

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

### setup pins for x9c103 digital potentiometer 
GPIO.setup(2,GPIO.OUT)
GPIO.output(2,GPIO.HIGH)
### ^setup UD as increase res
GPIO.setup(3,GPIO.OUT)
GPIO.output(3,GPIO.LOW)
### ^setup INC
GPIO.setup(4,GPIO.OUT)
GPIO.output(4,GPIO.LOW)
### ^setup CS

GPIO.setup(22,GPIO.OUT)
### ^setup Relay

GPIO.setup(27,GPIO.OUT)
### ^setup LED

GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_UP)
### ^setup Toggle Switch

GPIO.setup(18,GPIO.OUT)
servo1 = GPIO.PWM(18,50) # pin 11 for servo1, pulse 50Hz
# Start PWM running, with value of 0 (pulse off)
servo1.start(0)
### ^Setup Servo

for i in range (1, 100):		
	GPIO.output(3,GPIO.LOW)
	time.sleep(0.0002)
	GPIO.output(3,GPIO.HIGH)
	time.sleep(0.0002)
print("Finished setting DigiPot to max.")
time.sleep(3)
### ^reset DigiPot to maxium resistance (10k)

##################################### Setup CMPL ##############################################################

try:
    while True:
        button_state = GPIO.input(17)
        while GPIO.input(17) == False:
            
            ############################# Start Motor Speed Control ###############################################

            GPIO.output(2,GPIO.LOW)
            ### ^setup UD as decrease resistance

            GPIO.output(22,GPIO.HIGH)
            ### ^switch on relay

            GPIO.output(27,GPIO.HIGH)
            ### ^turn on led

            ############################# Motor Speed 1 ###########################################################

            for i in range (1, 5):		
                GPIO.output(3,GPIO.LOW)
                time.sleep(0.002)
                GPIO.output(3,GPIO.HIGH)
                time.sleep(0.002)
            ### ^decrease DigiPot by 5 steps, desire 3.23v
            print("Speed 1 (step99, =3.08v)")

            servo1.ChangeDutyCycle(2+(0/18))

            time.sleep(3)
            ### ^delay for testing

            ############################# Motor Speed 2 ###########################################################

            for i in range (1, 3):		
                GPIO.output(3,GPIO.LOW)
                time.sleep(0.002)
                GPIO.output(3,GPIO.HIGH)
                time.sleep(0.002)
            ### ^decrease DigiPot by 3 steps, desire 3.82v
            print("Speed 2 (step96, =3.89v)")

            servo1.ChangeDutyCycle(2+(75/18))

            time.sleep(3)
            ### ^delay for testing

            ############################# Motor Speed 3 ###########################################################

            for i in range (1, 3):		
                GPIO.output(3,GPIO.LOW)
                time.sleep(0.002)
                GPIO.output(3,GPIO.HIGH)
                time.sleep(0.002)
            ### ^decrease DigiPot by 3 steps, desire 4.79v
            print("Speed 3 (step93, =4.70v)")

            servo1.ChangeDutyCycle(2+(105/18))

            time.sleep(3)
            ### ^delay for testing

            ############################# Motor Speed 4 ###########################################################

            for i in range (1, 5):		
                GPIO.output(3,GPIO.LOW)
                time.sleep(0.0002)
                GPIO.output(3,GPIO.HIGH)
                time.sleep(0.0002)
            ### ^decrease DigiPot by 5 steps, desire 6.37v
            print("Speed 4 (step87, =6.30v)")

            servo1.ChangeDutyCycle(2+(135/18))

            time.sleep(3)
            ### ^delay for testing

            ############################# Motor Speed 5 ###########################################################

            for i in range (1, 10):		
                GPIO.output(3,GPIO.LOW)
                time.sleep(0.0002)
                GPIO.output(3,GPIO.HIGH)
                time.sleep(0.0002)
            ### ^decrease DigiPot by 9 steps, desire  10.45v; 11 step = 10.54
            print("Speed 5 (step78, =10.10v)")

            servo1.ChangeDutyCycle(2+(165/18))

            time.sleep(3)
            ### delay for test resuld check

            ############################# Motor Speed Slowest #####################################################

            GPIO.output(2,GPIO.HIGH)
            ### ^setup UD as increase resistance
            for i in range (1, 100):
                GPIO.output(3,GPIO.LOW)
                time.sleep(0.0002)
                GPIO.output(3,GPIO.HIGH)
                time.sleep(0.0002)
            ### ^reset DigiPot to maxium resistance (10k)
            print("Finished setting DigiPot to max.")
        else:
            GPIO.output(18,GPIO.LOW)
            ### Relay Off
            GPIO.output(27,GPIO.LOW)
            ### Led Off
except:
    print('fin')
    GPIO.cleanup()
    


##################################### Cleanup #################################################################

GPIO.output(18,GPIO.LOW)
### Relay Off
GPIO.output(27,GPIO.LOW)
### Led Off

print("fin")

GPIO.cleanup()



