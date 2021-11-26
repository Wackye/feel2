### 把音樂全部讀進來，按照順序多執行序播放


from pydub import AudioSegment
from pydub.playback import play
import time
import os
import threading
import random
import multiprocessing as mp
import operator

if __name__ == '__main__':  #必須放這段代碼，不然會Error

    random.seed(time.time())
    sounds = []
    bg_file1 = './/long/0_waltz_v4.wav'
    bg_file2 = './/long/0_44_v3.wav'
    path = './sounds'
    readStart = time.time()
    with open(bg_file2,'rb') as f:
        d = {'file': 'bgm', 'audio':AudioSegment.from_file(f)}
        sounds.append(d)
    

    for file in os.listdir(path):
        if file.endswith(".wav"):
            # print('add ' + os.path.join(path,file))
            with open(os.path.join(path,file),'rb') as f:
                d = {'file': file, 'audio':AudioSegment.from_file(f)}
                sounds.append(d)
                # audios.append(AudioSegment.from_file(os.path.join(path,file)))

    bg = sounds[0]
    suffle_sounds = sounds[1:-1]
    random.shuffle(suffle_sounds)
    sounds.clear()
    sounds.append(bg)
    sounds += suffle_sounds

    t_list = []
        
    def shot(sound, filename):
        play(sound)
        print(filename)

    # ## just for test
    # for audio in audios:
    #     play(audio)
    # ## just for test

    
    print('loading file time: ', time.time() - readStart)
    
    print('threading...')
    t = threading.Thread(target=shot, args=(sounds[0]['audio'],sounds[0]['file']))
    t_list.append(t)


    for i in range(1,len(sounds)):
        t = threading.Thread(target=shot, args=(sounds[i]['audio'],sounds[i]['file']))
        t_list.append(t)
    

    
    interval = 1
    start = time.time()
    end = 0
    now = start
    for t in t_list:
        t.start()
        time.sleep(interval - end)
        end = ((time.time() - start) * 1000 % (interval * 1000)) / 1000
        # print(end)
    for t in t_list:
        t.join()