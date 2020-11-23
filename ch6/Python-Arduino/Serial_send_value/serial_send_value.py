# -*- coding: utf-8 -*-
import serial
import time

with serial.Serial('COM5') as ser:
    time.sleep(5.0)
    for i in range(5):
        for j in range(255):
            ser.write((str(j)+'\n').encode('utf-8'))
            time.sleep(0.01)  #0.01秒待つ
