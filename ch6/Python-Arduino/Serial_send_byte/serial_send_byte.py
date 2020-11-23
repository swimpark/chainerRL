# -*- coding: utf-8 -*-
import serial
import time

with serial.Serial('COM5') as ser:
    time.sleep(5.0)
    for i in range(5):
        ser.write(b'a')
        time.sleep(1.0)
        ser.write(b'b')
        time.sleep(1.0)
