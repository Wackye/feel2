### autorun on startup using Terminal> sudo nano /etc/rc.local > added path, remove to cancel

import RPi.GPIO as GPIO
import queue

from pydub import AudioSegment
from pydub.playback import play
from time import sleep

import threading
import os
import time
import csv

def Initialize():

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

    
    ### reset 電位器，用3個pin去控制
    ### 每run一次會上去一個位階，所以要跑100次
    for i in range (1, 100):		
        GPIO.output(3,GPIO.LOW)
        time.sleep(0.0002)
        GPIO.output(3,GPIO.HIGH)
        time.sleep(0.0002)
    print("Finished setting DigiPot to max.")
    time.sleep(3)
    ### ^reset DigiPot to maxium resistance (10k)
    
    # set to init state
    GPIO.output(18,GPIO.LOW)
    ### Relay Off
    GPIO.output(27,GPIO.LOW)
    ### Led Off


def Nothing():
    # def Init_potentiometer(UD,INC,CS):
    #     ### setup pins for x9c103 digital potentiometer 
    #     GPIO.setup(UD,GPIO.OUT)
    #     GPIO.output(UD,GPIO.HIGH)
    #     ### ^setup UD as increase res
    #     GPIO.setup(INC,GPIO.OUT)
    #     GPIO.output(INC,GPIO.LOW)
    #     ### ^setup INC 
    #     GPIO.setup(CS,GPIO.OUT)
    #     GPIO.output(CS,GPIO.LOW)
    #     ### ^setup CS 


    #     ### reset 電位器，用3個pin去控制
    #     ### 每run一次會上去一個位階，所以要跑100次
    #     for i in range (1, 100):		
    #         GPIO.output(3,GPIO.LOW)
    #         time.sleep(0.0002)
    #         GPIO.output(3,GPIO.HIGH)
    #         time.sleep(0.0002)
    #     print("Finished setting DigiPot to max.")
    #     time.sleep(3)
    #     ### ^reset DigiPot to maxium resistance (10k)


    # def Init_Other(relay, toggle):
        
    #     GPIO.setup(relay,GPIO.OUT)
    #     ### ^setup Relay

    #     GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #     ### ^setup Toggle Switch


    # def Init_Led(led):
    #     GPIO.setup(led,GPIO.OUT)
    #     ### ^setup LED

    # def Init_Servo(servo):
    #     GPIO.setup(servo,GPIO.OUT)
    #     servo = GPIO.PWM(servo,50) # pin 11 for servo1, pulse 50Hz
    #     # Start PWM running, with value of 0 (pulse off)
    #     servo.start(0)
    #     ### ^Setup Servo
    print('nothing!')

### 讀取音檔後回傳
def read_sound(path, file):
        # if(os.path.exists(os.path.join(path,file))):
        with open(os.path.join(path,file),'rb') as f:
            return AudioSegment.from_file(f)

def Read_Background(path,bg_list):
    for file in os.listdir(path):
        if file.endswith(".wav"):
            bg_list.append(read_sound(path,file))

### 讀取csv並存入database
def Read_Database(database, csv_file, path):
    
    start = time.time()
    with open(csv_file, newline='') as csvfile:

        # 讀取csv檔案內容
        rows = csv.reader(csvfile)
        for row in rows:
            # print(row)
            sound = read_sound(path,row[2] + '.wav')
            for i in range(0, int(row[1])):
                qrcode = str(row[3])[0:-1] + str(i+1)
                dict = { qrcode : sound } # qrcode: sound_file pair
                database.update(dict)
        print('finish read database')
    print(time.time() - start)


### 在開始旋轉後常亮106秒
def Run_Led(led,self):
    
    print("run_led")
    GPIO.setup(led,GPIO.OUT)
    led1 = GPIO.PWM(led,200)
    led1.start(0)
    led1.ChangeDutyCycle(100)
    time.sleep(106)
    exit()

### 改變角度後休息一秒return, call by run_servo
def changeAngle(s1, angle):
    # GPIO.setup(s1,GPIO.OUT)
    servo = GPIO.PWM(s1,50) # pin 11 for servo1, pulse 50Hz
    servo.start(0)
    servo.ChangeDutyCycle(2+(angle/18))
    time.sleep(1)
    servo.stop()


def Run_Servo(s1,sleep_list):

    changeAngle(s1,0)
    print('servo rotate 0')
    time.sleep(sleep_list[0] - 1)

    changeAngle(s1,75)
    print('servo rotate 75')
    time.sleep(sleep_list[1] - 1)
    
    changeAngle(s1,105)
    print('servo rotate 105')
    time.sleep(sleep_list[2] - 1)
    
    changeAngle(s1,135)
    print('servo rotate 135')
    time.sleep(sleep_list[3] - 1)
    
    changeAngle(s1,165)
    print('servo rotate 165')
    time.sleep(sleep_list[4] - 1)
    exit()

def Run_Motor(sleep_list):
    
            ############################# Start Motor Speed Control ###############################################

            GPIO.output(2,GPIO.LOW)
            ### ^setup UD as decrease resistance

            GPIO.output(22,GPIO.HIGH)
            ### ^switch on relay

            GPIO.output(27,GPIO.HIGH)
            ### ^turn on led

            ############################# Motor Speed 1 ###########################################################
            ### 從100階往下慢慢降
            for i in range (1, 5):		
                GPIO.output(3,GPIO.LOW)
                time.sleep(0.002)
                GPIO.output(3,GPIO.HIGH)
                time.sleep(0.002)
            ### ^decrease DigiPot by 5 steps, desire 3.23v
            print("Speed 1 (step99, =3.08v)")

            time.sleep(sleep_list[0])
            ### ^delay for testing

            ############################# Motor Speed 2 ###########################################################

            for i in range (1, 3):		
                GPIO.output(3,GPIO.LOW)
                time.sleep(0.002)
                GPIO.output(3,GPIO.HIGH)
                time.sleep(0.002)
            ### ^decrease DigiPot by 3 steps, desire 3.82v
            print("Speed 2 (step96, =3.89v)")

            time.sleep(sleep_list[1])
            ### ^delay for testing

            ############################# Motor Speed 3 ###########################################################

            for i in range (1, 3):		
                GPIO.output(3,GPIO.LOW)
                time.sleep(0.002)
                GPIO.output(3,GPIO.HIGH)
                time.sleep(0.002)
            ### ^decrease DigiPot by 3 steps, desire 4.79v
            print("Speed 3 (step93, =4.70v)")

            time.sleep(sleep_list[2])
            ### ^delay for testing

            ############################# Motor Speed 4 ###########################################################

            for i in range (1, 5):		
                GPIO.output(3,GPIO.LOW)
                time.sleep(0.0002)
                GPIO.output(3,GPIO.HIGH)
                time.sleep(0.0002)
            ### ^decrease DigiPot by 5 steps, desire 6.37v
            print("Speed 4 (step87, =6.30v)")

            time.sleep(sleep_list[3])
            ### ^delay for testing

            ############################# Motor Speed 5 ###########################################################

            for i in range (1, 10):		
                GPIO.output(3,GPIO.LOW)
                time.sleep(0.0002)
                GPIO.output(3,GPIO.HIGH)
                time.sleep(0.0002)
            ### ^decrease DigiPot by 9 steps, desire  10.45v; 11 step = 10.54
            print("Speed 5 (step78, =10.10v)")

            time.sleep(sleep_list[4])
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
            exit()

def playbg(background,self):
    play(background)
    exit()

### 播放單個音檔
def shot(q):
    while(True):
        if(q.empty() != True):
            play(q.get())
            time.sleep(0.02)

if __name__ == '__main__':

    ### 宣告變數

    ### Potentiometer
    UD = 2
    INC = 3
    CS = 4

    ### Others
    Relay = 22
    Led = 27
    Toggle = 17 

    ### Servo
    Servo = 18

    ### Sounds
    bg_path = './sounds/'  ### 背景音樂
    sound_path = './sounds_complete/' ### 音檔資料夾

    bg_list = []
    database = dict()
    q = queue.Queue()


    ### database
    csv_file = './1.csv'

    ### threading
    t_list = []

    ###----------上面是宣告，下面才正式開始執行----------

    GPIO.setmode(GPIO.BCM)

    # Init_potentiometer(UD, INC, CS)
    # Init_Other(Relay, Toggle)
    # Init_Led(Led)
    # Init_Servo(Servo)
        
    
    # --- 
    print('initialize...')
    Initialize()
    

    ### 用多執行緒方式載入loading
    print('hardware test...(skip)')
    # loading = threading.Thread(target=loading_servo, args=(s1,0))
    # loading.start()
    
    ### 讀取csv建立QR Code和音檔pair, 背景音樂和音檔
    print('loading background music...')

    Read_Background(bg_path, bg_list)
  
    print('loading database...')
    Read_Database(database, csv_file, sound_path)


    ### 將伺服馬達, 直流馬達, 燈光, 背景音樂, 皆加入多執行緒
    print('threading...')

    sleep_list = [34, 27, 21, 15, 9]
    
    servo_thread = threading.Thread(target=Run_Servo, args=(Servo,sleep_list))      
    motor_thread = threading.Thread(target=Run_Motor, args=(sleep_list,))
    led_thread = threading.Thread(target=Run_Led,args=(Led,))

    # play background music
    bg_thread = threading.Thread(target=playbg, args=(bg_list[0],'bgm'))

    # loading.join()
    
    ### 開啟4個用來播放音檔的執行緒池, 一有音檔讀入queue, 就會被其中一個執行緒抓去播放
    for i in range(0,4):
        t = threading.Thread(target=shot, args=(q,))
        t_list.append(t)
        t_list[i].start()
        # time.sleep(0.25)

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
    while(time.time() - start <= 106):

        tmp = input()
        if( tmp != last):
            q.put(database[tmp])
            last = tmp
            end = ((time.time() - start) * 1000 % (interval * 1000)) / 1000
            time.sleep(interval - end)


    ##################################### Cleanup #################################################################

    GPIO.output(18,GPIO.LOW)
    ### Relay Off
    GPIO.output(27,GPIO.LOW)
    ### Led Off

    print("fin")

    ### 關閉其他執行緒
    servo_thread.join()
    motor_thread.join()
    bg_thread.join()
    for t in t_list:
        t.join()

    #Clean things
    # stop_servo(s1)
    # stop_led(led)

    GPIO.cleanup()
    print('finish')
    exit(0)





