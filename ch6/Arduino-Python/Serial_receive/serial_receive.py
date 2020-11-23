# -*- coding: utf-8 -*-
import serial
import time

ser = serial.Serial('COM5', timeout=0.5)
time.sleep(5.0)
for i in range(10):
    line = ser.read()
    print(line)
ser.close()
