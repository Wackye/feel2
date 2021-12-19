### 把聲音依序讀進來播放

from pydub import AudioSegment
from pydub.playback import play

import csv
import random
import threading
import os
import time

if __name__ == '__main__':  #必須放這段代碼，不然會Error

   
    ### file IO
    sounds = {}
    bg = {}
    bg_file = './sounds/44_53bar.wav'    
    path = './sounds_test/'

    ### Database
    encoding = {}
    test_case = []
    csv_file = 'encoding.csv'

    ### threading
    t_list = []
    
    random.seed(time.time())

    
    start = time.time()
    
    ### read sounds
    with open(bg_file,'rb') as f:
        d = {'bgm' : AudioSegment.from_file(f)}
        bg = d

    print('background : ' + str(time.time() - start))
    start = time.time()
    
    for file in os.listdir(path):
        if file.endswith(".wav"):
            # print('add ' + os.path.join(path,file))
            with open(os.path.join(path,file),'rb') as f:
                filename = file.replace('.wav', '')
                # d = {filename : AudioSegment.from_file(f)}
                sounds[str.upper(filename)] = AudioSegment.from_file(f)
                # audios.append(AudioSegment.from_file(os.path.join(path,file)))



    ### Read csv & play

    print('sounds: ' + str(time.time() - start))
    exit()

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

    
    
    
##    ----

    print('threading...')
        
    def shot(dict,filename):
        play(dict[filename])
        exit(0)
        
    # play background music
    t = threading.Thread(target=shot, args=(bg,'bgm'))
    t_list.append(t)

    ### play random sounds
    for i in range(1,len(test_case)):
        # print(sounds[test_case[i]])
        t = threading.Thread(target=shot, args=(sounds,test_case[i]))
        t_list.append(t)
    

    interval = 1.0   
    start = time.time()
    end = 0
    now = start
    for t in t_list:
        t.start()
        time.sleep(interval - end)
        end = ((time.time() - start) * 1000 % (interval * 1000)) / 1000
    for t in t_list:
        t.join()


