import threading
import queue
import time

q = queue.Queue()

def shot_x(q,self):
    while(True):        
        if(q.empty() != True):
            q.get()
            print('1111')
            time.sleep(0.3) 
def shot_y(q,self):
    while(True):
        if(q.empty() != True):
            q.get()
            print('2222222')
            time.sleep(0.3)
def shot_z(q,self):
    while(True):
        if(q.empty() != True):
            q.get()
            print('3333333333333')
            time.sleep(0.3)
if __name__ == '__main__':
    tx = threading.Thread(target=shot_x, args=(q,''))
    ty = threading.Thread(target=shot_y, args=(q,''))
    tz = threading.Thread(target=shot_z, args=(q,''))

    q.put('something')
    q.put('something')
    q.put('something')
    tx.start()
    ty.start()
    tz.start()
    last = 0

    while(True):    
        tmp = input()
        if(tmp != last):
            q.put(tmp)
        last = tmp
        # ('something')
        time.sleep(0.1)
        