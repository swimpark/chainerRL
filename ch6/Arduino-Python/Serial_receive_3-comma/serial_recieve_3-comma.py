# coding:utf-8
import serial
import time

with serial.Serial("COM6") as ser:
    time.sleep(5.0)
    for i in range(10):
        line = ser.readline()
        line = line.rstrip().decode('utf-8').strip().split(",")#<-����Ȋ����ō폜�������ł��D
#        line = line.rstrip().decode('utf-8')
        print(line)
