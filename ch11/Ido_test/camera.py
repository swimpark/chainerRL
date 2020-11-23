# -*- coding: utf-8 -*-
import cv2

n0 = 0
n1 = 0
n2 = 0
n3 = 0
n4 = 0
n5 = 0
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    xp = int(frame.shape[1]/2)
    yp = int(frame.shape[0]/2)
    d = 200
    cv2.rectangle(gray, (xp-d, yp-d), (xp+d, yp+d), color=0, thickness=10)
    cv2.imshow('gray', gray)
    gray = cv2.resize(gray[yp-d:yp + d, xp-d:xp + d],(40, 40))
    c =cv2.waitKey(10) 
    if c == 48:#0
        cv2.imwrite('img/0/{0}.png'.format(n0), gray)
        n0 = n0 + 1
    elif c == 49:#1
        cv2.imwrite('img/1/{0}.png'.format(n1), gray)
        n1 = n1 + 1
    elif c == 50:#2
        cv2.imwrite('img/2/{0}.png'.format(n2), gray)
        n2 = n2 + 1
    elif c == 51:#3
        cv2.imwrite('img/3/{0}.png'.format(n3), gray)
        n3 = n3 + 1
    elif c == 52:#4
        cv2.imwrite('img/4/{0}.png'.format(n4), gray)
        n4 = n4 + 1
    elif c == 53:#5
        cv2.imwrite('img/5/{0}.png'.format(n5), gray)
        n5 = n5 + 1
    elif c == 27:#Esc
        break
cap.release()
