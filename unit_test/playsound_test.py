from playsound import playsound
import os
import time
# playsound('/Users/iuilab/Documents/feel2/feel2/sounds/1.wav')

path = './sounds_complete/'
for file in os.listdir(path):
        if file.endswith(".wav"):
            # print('add ' + os.path.join(path,file))
            t = time.time()
            playsound(os.path.join(path,file))
            print(time.time() - t)
            # with open(os.path.join(path,file),'rb') as f:
            #     print(f)
