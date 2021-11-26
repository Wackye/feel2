### test for GM67, howeve finally useless.

import serial

# test in cmd : ls /dev/tty*
ser = serial.Serial('/dev/tty1', # Device name varies
baudrate = 9600,
bytesize = 8,
parity = 'N',
stopbits = 1)

print(ser)
print('open serial port sucessed.')
# ser.close()
# ser.open()
# data = ser.read()
# print('data is : ' + data)
 
if ser.isOpen():
    print('wtf')
    while True:
        while ser.in_waiting:
            print('waiting...')
            data_raw = ser.readline()
            data = data_raw.decode()
            print('raw data received:', data_raw)
            print('data received:', data)
# except KeyboardInterrupt:
# 	ser.close()
# 	print('BYEBYE')	test1234


