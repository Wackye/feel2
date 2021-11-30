import RPi.GPIO as GPIO
import time

led = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(led,GPIO.OUT)
led1 = GPIO.PWM(4,200)
led1.start(100)
time.sleep(0.5)
# some blink
# GPIO.output(led,GPIO.HIGH)
# time.sleep(0.1)
# GPIO.output(led,GPIO.LOW)
# time.sleep(0.1)
# GPIO.output(led,GPIO.HIGH)
# time.sleep(0.1)
# GPIO.output(led,GPIO.LOW)
# # led1.stop()


# GPIO.setup(4,GPIO.OUT)
# GPIO.output(4,GPIO.HIGH)
# led1 = GPIO.PWM(4,200)
# led1.start(0)
led1.ChangeDutyCycle(10)
time.sleep(5)
GPIO.cleanup()














