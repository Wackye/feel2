import threading
import serial   
from time import sleep

ser = serial.Serial("/dev/ttyS0", 9600)
recieved_data = ''
last_string = []
def read_value(re):
    while(True):
        recieved_data = ser.read()
        sleep(0.03)
        data_left = ser.inWaiting()
        recieved_data += ser.read(data_left)
        last_string.append(recieved_data)
#        print(recieved_data)
        

t = threading.Thread(target=read_value, args=(recieved_data,))
t.start()
while True:
    sleep(0.3)
#    print(len(recieved_data))
    if(len(last_string) != 0):
        s = str(int(last_string[0]))
        last_string.pop()
        print(s)
        print(s[0] + ' ' + s[1] + ' ' + s[2] + ' ')
#    if(len(recieved_data) > 0):
#        print(recieved_data)
        # li = ''