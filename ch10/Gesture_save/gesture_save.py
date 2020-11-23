# -*- coding: utf-8 -*-
import serial
import time

n1 = 0
with serial.Serial('COM5', 115200) as ser:
    while True:
        gn = ser.readline()
        filename = 'receive/{0}.txt'.format(n1)
        n1 += 1
        print(filename)
        time.sleep(1.0)
        with open(filename, 'w') as f:
            for i in range(50):
                line = ser.readline()
                line = line.rstrip().decode('utf-8')
                f.write(line+'\n')
        print('End')
