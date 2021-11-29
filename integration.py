from pydub import AudioSegment
from pydub.playback import play

import csv
import random
import threading
import os
import time
import RPi.GPIO as GPIO          
from time import sleep

def read_sounds(bg, bg_file, sounds):
### read sounds
    print('read background music...')
    with open(bg_file,'rb') as f:
        bg['bgm'] = AudioSegment.from_file(f)
 
    print('read sounds...')
    for file in os.listdir(path):
        if file.endswith(".wav"):
            # print('add ' + os.path.join(path,file))
            with open(os.path.join(path,file),'rb') as f:
                filename = file.replace('.wav', '')
                # d = {filename : AudioSegment.from_file(f)}
                sounds[str.upper(filename)] = AudioSegment.from_file(f)
                # audios.append(AudioSegment.from_file(os.path.join(path,file)))

def read_csv(csv_file,test_case):
    ### Read csv & play
    print('read csv file...')
    # 開啟 CSV 檔案
    with open(csv_file, newline='', encoding='utf-8') as csvfile:

        # 讀取 CSV 檔案內容
        csvreader = csv.reader(csvfile)
        header = next(csvreader)
        # 以迴圈輸出每一列
        for row in csvreader:
            if row[2] != '':
                encoding[row[0]] = row[2]
                # print("Add " + row[0] + ":" + row[2])
                for times in range(0,int(row[1])):
                    test_case.append(str.upper(row[2]))

    random.shuffle(test_case)
    
    
def init_motor():
    print('intialize motor')
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

    
def init_servo(s1):
    print('initialize servo')
    # Set pin 11 as an output, and define as servo1 as PWM pin
    GPIO.setup(s1,GPIO.OUT)
    servo1 = GPIO.PWM(s1,50) # pin 11 for servo1, pulse 50Hz
        
    # Start PWM running, with value of 0 (pulse off)
    servo1.start(0)
    angle = 0
    servo1.ChangeDutyCycle(2+(angle/18))
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)
    servo1.stop()

def init_led(led):
    print('initialize led')
    GPIO.setup(led,GPIO.OUT)
    led1 = GPIO.PWM(4,200)

    # some blink
    GPIO.output(led,GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(led,GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(led,GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(led,GPIO.LOW)
    led1.stop()
#     l = GPIO.PWM(led,50)
#     l.start(10)

def loading_servo(s1,angle):
    servo = GPIO.PWM(s1,50) # pin 11 for servo1, pulse 50Hz    
    # Start PWM running, with value of 0 (pulse off)
    
    time.sleep(5)
    servo.start(0)
    servo.ChangeDutyCycle(2+(180/18))    
    time.sleep(5)    
    servo.stop()    

    servo.start(0)
    servo.ChangeDutyCycle(2+(0/18))
    time.sleep(1)
    servo.stop()
    

def loading_led(led):
    print("loading_led")
    GPIO.setup(led,GPIO.OUT)
    GPIO.output(led,GPIO.HIGH)
    led1 = GPIO.PWM(led,200)
    led1.ChangeDutyCycle(100)

    
def changeAngle(s1, angle):
    GPIO.setup(s1,GPIO.OUT)
    servo = GPIO.PWM(s1,50) # pin 11 for servo1, pulse 50Hz
    servo.start(0)
    servo.ChangeDutyCycle(2+(angle/18))
    time.sleep(1)
    servo.stop()

def run_servo(s1,n):

    changeAngle(s1,0)
    print('servo rotate 0')
    time.sleep(33)

    changeAngle(s1,75)
    print('servo rotate 75')
    time.sleep(26)
    
    changeAngle(s1,105)
    print('servo rotate 105')
    time.sleep(20)
    
    changeAngle(s1,135)
    print('servo rotate 135')
    time.sleep(14)
    
    changeAngle(s1,165)
    print('servo rotate 165')
    time.sleep(8)

def run_motor_new():
    
    GPIO.setup(5,GPIO.OUT)
    GPIO.setup(6,GPIO.OUT)
    GPIO.setup(13,GPIO.OUT)
    GPIO.setup(19,GPIO.OUT)
    GPIO.setup(26,GPIO.OUT)
    
    GPIO.output(26,GPIO.HIGH)
    time.sleep(34)
    GPIO.output(26,GPIO.LOW)

    GPIO.output(19,GPIO.HIGH)
    time.sleep(27)
    GPIO.output(19,GPIO.LOW)

    GPIO.output(13,GPIO.HIGH)
    time.sleep(21)
    GPIO.output(13,GPIO.LOW)

    GPIO.output(6,GPIO.HIGH)
    time.sleep(15)
    GPIO.output(6,GPIO.LOW)

    GPIO.output(5,GPIO.HIGH)
    time.sleep(9)
    GPIO.output(5,GPIO.LOW)

def playbg(dict,filename):
    play(dict[filename])

def shot(dict,filename):
    play(dict[filename])
    exit(0)

def stop_led(led):
    GPIO.setup(led,GPIO.OUT)
    GPIO.output(led,GPIO.LOW)
    
def stop_servo(s1):
    servo1 = GPIO.PWM(s1,50) # pin 11 for servo1, pulse 50Hz
    servo1.ChangeDutyCycle(0)
    time.sleep(1)
    servo1.stop()

### read csv
if __name__ == '__main__':  #必須放這段代碼，不然會Error

    GPIO.cleanup()

    ### file IO
    sounds = {}
    bg = {}
    bg_file = './sounds/44_53bar.wav'    
#    path = './sounds/sounds/'
    path = './sounds_complete/'

    ### database
    encoding = {}
    test_case = []
    csv_file = 'encoding.csv'

    ### threading
    t_list = []

    ### motor
    motor_list = []
    m1 = 24
    m2 = 23
    en = 25
    
    ### motor_control
    
    
    
    ### servo
    s1 = 17
    countCirlce = 0
    
    ### read count
    count = 0
    random.seed(time.time())

    ### led
    led = 4
    
    GPIO.setmode(GPIO.BCM)

    init_motor()
    init_servo(s1)
    init_led(led)
    
    loading = threading.Thread(target=loading_servo, args=(s1,0))
    loading.start()
    
    read_sounds(bg, bg_file,sounds)
    read_csv(csv_file, test_case)
        
    loading_led(led)
    
    print('threading...')
    t = threading.Thread(target=run_servo, args=(s1,''))
    motor_list.append(t)
      
    t = threading.Thread(target=run_motor_new)
    motor_list.append(t)
    
    # play background music
    t = threading.Thread(target=playbg, args=(bg,'bgm'))
    t_list.append(t)

    ### play random sounds
    for i in range(1,len(test_case)):
        # print(sounds[test_case[i]])
        t = threading.Thread(target=shot, args=(sounds,test_case[i]))
        t_list.append(t)
        
    loading.join()
    
    interval = 1.0   
    start = time.time()
    end = 0

    for m in motor_list:
        m.start()
    
    t_list[0].start()
    time.sleep(2)
        
    for i in range(1,len(t_list)):
#         count+=1
#         print(count)
        t_list[i].start()
        time.sleep(interval - end)
        print(interval - end)
        end = ((time.time() - start) * 1000 % (interval * 1000)) / 1000

    for m in motor_list:
        m.join()
        
    for t in t_list:
        t.join()    
    
    #Clean things
    stop_servo(s1)
    stop_led(led)

    GPIO.cleanup()
    print('finish')
    exit(0)

