### edit autostart : in home/pi folder, sudo nano autostart.sh


### input using serial version
import termios
import RPi.GPIO as GPIO
import queue
import sys
import serial

from pydub import AudioSegment
from pydub.playback import play
from time import sleep
from termios import tcflush

import threading
import os
import time
import csv
import random
import re 

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

    print('test servo..')
    GPIO.setup(18,GPIO.OUT)
    servo1 = GPIO.PWM(18,50) # pin 18 for servo1, pulse 50Hz
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
    ### ^reset DigiPot to maxium resistance (10k)
    
    # set to init state
    GPIO.output(18,GPIO.LOW)
    ### Relay Off
    GPIO.output(27,GPIO.LOW)
    ### Led Off


def load_test(s1,led):
    print('Servo & LED test...')
    led1 = GPIO.PWM(led,200)
    servo1 = GPIO.PWM(s1,50) # pin 18 for servo1, pulse 50Hz
    led1.start(0)
    servo1.start(0)
    
    servo1.ChangeDutyCycle(180/18 + 2)
    led1.ChangeDutyCycle(100)
    time.sleep(2)
    servo1.ChangeDutyCycle(2)
    led1.ChangeDutyCycle(0)
    time.sleep(2)
    print('Finish servo & led test')

    
### 讀取音檔後回傳
def read_sound(path, file):
        # if(os.path.exists(os.path.join(path,file))):
        with open(os.path.join(path,file),'rb') as f:
            return AudioSegment.from_file(f)

def Read_Background(path,bg_list):
    # for file in os.listdir(path):
    #     if file.endswith(".wav"):
            # bg_list.append(read_sound(path,file))
    bg_list.append(read_sound(path,'1.wav'))
    bg_list.append(read_sound(path,'2.wav'))
    bg_list.append(read_sound(path,'3.wav'))
    bg_list.append(read_sound(path,'4.wav'))
    print('Finish load background music.')

### 讀取csv並存入database
def Read_Database(database, csv_file, path, code_list):
    
    
    start = time.time()
    with open(csv_file, newline='') as csvfile:

        # 讀取csv檔案內容
        rows = csv.reader(csvfile)
        next(rows, None)
        for row in rows:
            # print(row)
            sound = read_sound(path,row[2].upper() + '.wav')
            qrcode = str(row[3])[0:4]
            dict = { qrcode : sound } # qrcode: sound_file pair
            database.update(dict)
#           code_list.append(qrcode)
        print('finish read database')
    print('read time: ' + str(time.time() - start))


### 在開始旋轉後常亮112秒 (平均每個曲子的時間落在1:52-1:56) 
def Run_Led(led, duration):
    
    # 1-> duration -> 5
    print("run_led")
    GPIO.setup(led,GPIO.OUT)
    GPIO.output(led,GPIO.HIGH)
    time.sleep(1)
    time.sleep(duration)
    GPIO.output(led, GPIO.LOW)
    time.sleep(8)
    # led1 = GPIO.PWM(led,200)
    # time.sleep(1)
    # led1.ChangeDutyCycle(100)
    # time.sleep(duration)
    # led1.ChangeDutyCycle(0)
    # time.sleep(8)
    # print("LED thread finish")
    # led1.ChangeDutyCycle(100)
    # time.sleep(1)


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

    changeAngle(s1,70)
    print('servo rotate 70')
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
    print("Servo thread finish")

    changeAngle(s1,0)
    # exit()

def Run_Motor(sleep_list):
    
    ### ^delay for testing############################# Start Motor Speed Control ###############################################

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
    print("Motor thread finish")
    # exit()


def playbg(background):
    play(background)
    print("bg thread finish")
    # exit()

def shot(q):
    while(True):
        if(q.empty() != True):
            try:
                play(q.get())
                time.sleep(0.01)
            except:
                time.sleep(0.01)
    print('Shot thread finish')

def read_input(data, ser):
    while(True):
        recieved_data = ser.read()
        sleep(0.03)
        data_left = ser.inWaiting()
        recieved_data += ser.read(data_left)
        regex_eli = r'[^0-9]+'

        r = re.sub(regex_eli, '', str(recieved_data))
        data.append(r)
        print(r)
        
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
    Toggle_state = 0

    ### Servo
    Servo = 18

    ### Sounds
    bg_path = './sounds/'  ### 背景音樂
    sound_path = './sounds/sfx/' ### 音檔資料夾

    bg_list = []
    code_list = []
    database = dict()


    ### database
    csv_file = './csv/all.csv'

    ### threading
    t_list = []
    stop = False
    q = queue.Queue()
    playReady = False

    ### serial input
    received = []
    ser = serial.Serial("/dev/ttyS0", 9600)

    ###----------上面是宣告，下面才正式開始執行----------

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # Init_potentiometer(UD, INC, CS)
    # Init_Other(Relay, Toggle)
    # Init_Led(Led)
    # Init_Servo(Servo)
        
    
    # --- 
    print('initialize...')
    Initialize()



    ### 用多執行緒方式載入loading
    print('hardware test...')
    loading = threading.Thread(target=load_test, args=(Servo,Led))
    loading.start()
    
    ### 讀取csv建立QR Code和音檔pair, 背景音樂和音檔
    print('loading background music...')

    Read_Background(bg_path, bg_list)
  
    print('loading database...')
    Read_Database(database, csv_file, sound_path, code_list)
    
    print('Loading Finish! Ready.')

    # play(AudioSegment.from_file('system.mp3'))

    paint_number = 0
    paint_already_know = False
    Toggle_state = GPIO.input(17)

    ### 開啟4個用來播放音檔的執行緒池, 一有音檔讀入queue, 就會被其中一個執行緒抓去播放
    for i in range(0,4):
        t = threading.Thread(target=shot, args=(q,))
        t.daemon = True
        t_list.append(t)
        t_list[i].start()

    ### serial read input
    t = threading.Thread(target=read_input, args=(received, ser))
    t.start()

    ### Led On
    GPIO.output(27,GPIO.HIGH)

    while(True):
        # tcflush(sys.stdin, termios.TCIFLUSH)
        Toggle_state = GPIO.input(17)
        GPIO.output(Led ,GPIO.HIGH)
        ###---------------------- user not decide which paint to use ---------
        last = 0
        received.clear()
        print('put the paint and recognize the number.')
        while(playReady == False or paint_already_know == False):
            if(playReady == False):
                Toggle_state = GPIO.input(17)
                if(Toggle_state == 0 and paint_already_know == True):
                    playReady = True

            # if(paint_already_know == False):
            GPIO.output(Led,GPIO.HIGH)
            ### Relay On
 
                    
            if len(received) != 0:
                s = str(received[0])
                received.pop()
                tmp = s
                try:
                    if(tmp[0] == '1' and last != 1):
                        paint_number = 1
                        paint_already_know = True
                        last = 1
                        play(AudioSegment.from_file('./sounds/confirm/1_confirm.wav'))
                    elif(tmp[0] == '2' and last != 2):
                        paint_number = 2    
                        paint_already_know = True
                        last = 2
                        play(AudioSegment.from_file('./sounds/confirm/2_confirm.wav'))
                    elif(tmp[0] == '3' and last != 3):
                        paint_number = 3    
                        paint_already_know = True
                        last = 3
                        play(AudioSegment.from_file('./sounds/confirm/3_confirm.wav'))
                    elif(tmp[0] == '4' and last != 4):
                        paint_number = 4    
                        paint_already_know = True
                        last = 4
                        play(AudioSegment.from_file('./sounds/confirm/4_confirm.wav'))

                    # debug mode
                    elif(tmp[0] == '8' and last != 8):
                        paint_number = 0    
                        paint_already_know = True
                        playReady = True
                        last = 8
                        play(AudioSegment.from_file('./sounds/confirm/open_demo.wav'))
                    # elif(tmp[0] == '9' and last != 9):
                    #     paint_number = 0 
                    #     last = 9
                    #     play(AudioSegment.from_file('./sounds/confirm/close_demo.wav'))

                except:  
                    tmp = 0

        ###---------------------- user open the toggle switch, already verified which paint -----
    
             
        ### normal mode
        if(paint_number == 1 or paint_number == 2 or paint_number == 3 or paint_number == 4):
            
            ### 將伺服馬達, 直流馬達, 燈光, 背景音樂, 皆加入多執行緒
            print('threading...')
            sleeps = [34, 27, 21, 15, 9]
            led_duration = [108, 114, 106, 115]

            servo_thread = threading.Thread(target=Run_Servo, args=(Servo,sleeps))      
            motor_thread = threading.Thread(target=Run_Motor, args=(sleeps,))
            led_thread = threading.Thread(target=Run_Led,args=(Led,led_duration[(paint_number-1)%4]))
            bg_thread = threading.Thread(target=playbg, args=(bg_list[(paint_number-1)%4],))

            servo_thread.daemon = True
            motor_thread.daemon = True
            led_thread.daemon = True
            bg_thread.daemon = True    

            ### 執行緒開始
            led_thread.start()
            time.sleep(1)
            bg_thread.start() 

            ### 先轉4拍再開始播放音檔
            time.sleep(led_duration[(paint_number-1)] - 106)
            motor_thread.start()
            servo_thread.start()

            ### 讀取/播放音檔間隔
            interval = 1.0

            ### 計時器用
            last = 0
            end = 0
            start = time.time()     
            val = 0

            received.clear()
            ### 持續讀入QR Code, 存入對應音檔
            while(time.time() - start <= 106):
                if len(received) != 0:
                    s = str(received[0])
                    received.pop()
                    val = s
                    if(val != last):
                        try:
                            q.put(database[val[0:4]])
                            last = val
                            end = ((time.time() - start) * 1000 % (interval * 1000)) / 1000
                            duration = interval - end
                            time.sleep(duration)
                        except:
                            val = 0
                        # if(tmp == 'stop'):
                        #     stop = True
            
            ##################################### Cleanup #################################################################
            print("Read finish")

        
        ### 播放單個音檔
        elif(paint_number == 0):
            val = '0000'
            last = 0
            while(val[0] != '9'):                
                if len(received) != 0:
                    s = str(received[0])
                    received.pop()
                    if(len(s) > 0):
                        val = s
                        if(val != last and len(val) > 0 and val[0] != '9'):
                            try:
                                q.put(database[val[0:4]])
                                last = val  
                                time.sleep(0.5)
                            except:
                                last = 0
                            
            play(AudioSegment.from_file('./sounds/confirm/close_demo.wav'))

        if(paint_number != 0):
            endbreak = (led_duration[(paint_number-1)]) - 96
            print('main thread sleep in end ' + str(endbreak))
            time.sleep(endbreak)
            led_thread.join()
            stop = True
            servo_thread.join()
            motor_thread.join()
            received.clear()
        paint_already_know = False
        playReady = False
        print('again')




