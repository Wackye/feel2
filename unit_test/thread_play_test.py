### 測試用執行緒池(threading pool)的寫法來播放音效

import threading
import queue
import time
import pydub
from pydub import AudioSegment
from pydub.playback import play
q = queue.Queue()

def LoadSound(file):
    with open(file,'rb') as f:
        sfx = AudioSegment.from_file(f)
        return sfx

def shot(sfx, self):
        play(sfx)
        exit(0)

def shot_x(q,sfx):
    while(True):        
        if(q.empty() != True):
            q.get()
            play(sfx)
            print('111')
            time.sleep(0.02) 
def shot_y(q,sfx):
    while(True):
        if(q.empty() != True):
            q.get()
            play(sfx)
            print('222222')
            time.sleep(0.02)

def shot_z(q,sfx):
    while(True):
        if(q.empty() != True):
            q.get()
            play(sfx)
            print('3333333333333')
            time.sleep(0.02)
            
if __name__ == '__main__':

    file = './system.mp3'
    file2 = './system2.mp3'
    file3 = './system3.mp3'

    sfx = LoadSound(file)
    sfx2 = LoadSound(file2)
    sfx3 = LoadSound(file3)

    tx = threading.Thread(target=shot_x, args=(q,sfx))
    ty = threading.Thread(target=shot_y, args=(q,sfx2))
    tz = threading.Thread(target=shot_z, args=(q,sfx3))

    q.put('something')
    q.put('something')
    q.put('something')
    tx.start()
    ty.start()
    tz.start()
    last = 0
    cnt = 0
    while(last != 'finish'):    
        tmp = input()
        if(tmp != last):
            q.put(tmp)
            last = tmp
            cnt+=1
    print(cnt)
