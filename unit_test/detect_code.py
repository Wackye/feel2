### 把聲音依序讀進來播放

from pydub import AudioSegment
from pydub.playback import play

import threading
import queue
import time


def LoadSound(file):
    with open(file,'rb') as f:
        sfx = AudioSegment.from_file(f)
        return sfx

def shot(sfx, self):
        play(sfx)
        exit(0)

def shot_loop(q,self):
    while(1):
        if(q.empty() != True):
            play(q.get())
        
q = queue.Queue()
if __name__ == '__main__':  #必須放這段代碼，不然會Error

   
    ### file IO
    file = './system.mp3'
    file2 = './system2.mp3'
    file3 = './system3.mp3'

    sfx = LoadSound(file)
    sfx2 = LoadSound(file2)
    sfx3 = LoadSound(file3)
   
    t = threading.Thread(target=shot, args=(sfx,''))
    t2 = threading.Thread(target=shot, args=(sfx2,''))
    t3 = threading.Thread(target=shot, args=(sfx3,''))
    
    val = 0
    while(True):
        tmp = input('scan qr code\n')
        # print(val)
        if tmp == '10262':  

            t.start()

            play(sfx)

        #   
        # elif tmp == '10462':
        #     t2.start()
        # else:
        #     play(sfx3)
        # val = tmp
        # time.sleep(0.1)
    t.join()
    t2.join()

