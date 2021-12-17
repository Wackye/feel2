from pydub import AudioSegment
from pydub.playback import play

import csv
import random
import threading
import os
import time
import RPi.GPIO as GPIO      
import queue    
from time import sleep
import sys


### 讀取音檔後回傳
def read_sound(path, file):
        # if(os.path.exists(os.path.join(path,file))):
        with open(os.path.join(path,file),'rb') as f:
            return AudioSegment.from_file(f)

### 讀取csv並存入database
def read_database(database, csv_file, path):
    
    start = time.time()
    with open(csv_file, newline='') as csvfile:

        # 讀取csv檔案內容
        rows = csv.reader(csvfile)
        # break out single row to database
        # and add correct piece of code according to repeat time. 
        for row in rows:
            # print(row)
            sound = read_sound(path,row[2] + '.wav')
            for i in range(0, int(row[1])):
                qrcode = str(row[3])[0:-1] + str(i+1)
                dict = { qrcode : sound } # qrcode: sound_file pair
                database.update(dict)
        print('finish read database')
    print(time.time() - start)

### 初始化步進馬達
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
    
### 初始化Servo馬達
def init_servo(s1):
    print('initialize servo')
    GPIO.setup(s1,GPIO.OUT)
    servo1 = GPIO.PWM(s1,50) # pin 11 for servo1, pulse 50Hz
        
    # Start PWM running, with value of 0 (pulse off)
    servo1.start(0)
    angle = 0
    servo1.ChangeDutyCycle(2+(angle/18))
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)
    servo1.stop()

### 初始化led
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

### 在loading 狀態時讓馬達動一動
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
    time.sleep(3)
    servo.stop()

### 在開始旋轉後常亮106秒
def run_led(led,self):
    
    print("run_led")
    GPIO.setup(led,GPIO.OUT)
    led1 = GPIO.PWM(led,200)
    led1.start(0)
    led1.ChangeDutyCycle(100)
    time.sleep(106)

### 改變角度後休息一秒return, call by run_servo
def changeAngle(s1, angle):
    # GPIO.setup(s1,GPIO.OUT)
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

def run_motor():
    
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
    time.sleep(10)
    GPIO.output(5,GPIO.LOW)


def playbg(background,self):
    play(background)
    exit()

### 播放單個音檔
def shot(path, q):
    while(True):
        if(q.empty() != True):
            play(q.get())
            time.sleep(0.02)

def stop_led(led):
    GPIO.setup(led,GPIO.OUT)
    led1 = GPIO.PWM(led,200)
    led1.ChangeDutyCycle(0)
    # GPIO.output(led,GPIO.LOW)
    led1.stop()

def stop_servo(s1):
    servo1 = GPIO.PWM(s1,50) # pin 11 for servo1, pulse 50Hz
    servo1.ChangeDutyCycle(0)
    time.sleep(1)
    servo1.stop()

def led_control(led, switch):
    print("initialize led switch thread")
    GPIO.setup(led,GPIO.OUT)
    GPIO.setup(switch,GPIO.IN)
    led1 = GPIO.PWM(led,50)
    led1.start(0)

    while True:
        tmp = GPIO.input(switch)
        
        # print(tmp)
        # if(val > 0.5):
        if(tmp == 1):
            led1.ChangeDutyCycle(100)
        elif(tmp == 0):
            led1.ChangeDutyCycle(0)

database = dict()
q = queue.Queue()

if __name__ == '__main__':  #必須把程式包在main function內，不然會Error

    GPIO.setwarnings(False)
    ### file IO

    bg_file = './sounds/bale_53bar.wav'  ### 背景音樂
    # bg_file = './sounds/44_53bar.wav'    
    path = './sounds_complete/' ### 音檔資料夾

    ### database
    csv_file = './1.csv'

    ### motor
    m1 = 24
    m2 = 23
    en = 25
        
    ### servo
    s1 = 17
    countCircle = 0
    
    ### read count
    count = 0

    ### led
    led = 4
    switch = 18

    ### threading
    t_list = []

    ###----------上面是宣告，下面才正式開始執行----------

    GPIO.setmode(GPIO.BCM)
    print('initialize...')

    init_motor()
    init_servo(s1)
    init_led(led)
    
    # led_thread = threading.Thread(target=led_control, args=(led, switch))
    # led_thread.start()
    
    ### 用多執行緒方式載入loading
    loading = threading.Thread(target=loading_servo, args=(s1,0))
    loading.start()
    
    ### 讀取csv建立QR Code和音檔pair, 背景音樂和音檔
    print('loading background music...')
    with open(bg_file,'rb') as f:
        # filename = bg_file.replace('.wav', '')
        bg = AudioSegment.from_file(f)

    print('loading database...')
    read_database(database, csv_file, path)

    ### 將伺服馬達, 直流馬達, 燈光, 背景音樂, 皆加入多執行緒
    print('threading...')
    servo_thread = threading.Thread(target=run_servo, args=(s1,''))      
    motor_thread = threading.Thread(target=run_motor)
    led_thread = threading.Thread(target=run_led,args=(led,''))

    # play background music
    bg_thread = threading.Thread(target=playbg, args=(bg,'bgm'))

    
    # loading.join()
    
    ### 開啟4個用來播放音檔的執行緒池, 一有音檔讀入queue, 就會被其中一個執行緒抓去播放
    for i in range(0,4):
        t = threading.Thread(target=shot, args=(path, q))
        t_list.append(t)
        # time.sleep(0.25)
        t_list[i].start()

    ### 執行緒開始
    led_thread.start()
    servo_thread.start()
    motor_thread.start()
    
    # os.system('python3 ./player_test.py')
    bg_thread.start() 

    ### 先轉四秒再開始播放音檔
    time.sleep(4)

    
    ### 讀取/播放音檔間隔
    interval = 1.0

    ### 計時器用
    last = 0
    end = 0
    start = time.time()     
    
    ### 持續讀入QR Code, 存入對應音檔
    while(True):

        tmp = input()
        if( tmp != last):
            # print('\n file:   ' + database[tmp])

            q.put(database[tmp])
                   
            last = tmp
            # time.sleep(interval)
            # print(interval - end)
            end = ((time.time() - start) * 1000 % (interval * 1000)) / 1000
            time.sleep(interval - end)

            # start = end
            # t = threading.Thread(target=playbg, args=(database[tmp],''))
            # t.start()

    ### 關閉其他執行緒
    servo_thread.join()
    motor_thread.join()
    bg_thread.join()

    #Clean things
    stop_servo(s1)
    stop_led(led)

    GPIO.cleanup()
    print('finish')
    exit(0)

