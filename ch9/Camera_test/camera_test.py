# -*- coding: utf-8 -*-
import cv2

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray', gray)
    c = cv2.waitKey(10)
    if c == 115:#s
        cv2.imwrite('camera.png', gray)
    if c == 27:#Esc
        break
cap.release()
