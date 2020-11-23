# -*- coding: utf-8 -*-
import serial
import time

with serial.Serial('COM5', timeout=0.5) as ser:
    time.sleep(5.0)
    with open('data.txt', 'w') as f:
        for i in range(10):
            line = ser.readline()
            line = line.rstrip().decode('utf-8')
            print(line)
            f.write((line)+'\n')
