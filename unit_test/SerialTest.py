import serial   
from time import sleep

ser = serial.Serial("/dev/ttyS0", 9600)
while True:
    print('loop')
    recieved_data = ser.read()
    sleep(0.03)
    data_left = ser.inWaiting()
    recieved_data += ser.read(data_left)
#    if(data_left > 0):#        recieved_data = str(int(recieved_data))
    print(recieved_data)