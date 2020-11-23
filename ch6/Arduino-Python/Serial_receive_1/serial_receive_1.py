# -*- coding: utf-8 -*-
import serial
import time

with serial.Serial('COM5') as ser:
    time.sleep(5.0)
    for i in range(10):
        line = ser.read()
        print(line)
