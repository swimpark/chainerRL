# -*- coding: utf-8 -*-
import numpy as np
import chainer
import chainer.functions as F
import chainer.links as L
import chainer.initializers as I
from chainer import training
from chainer.training import extensions
import os
import cv2
import serial

class MyChain(chainer.Chain):
    def __init__(self):
        super(MyChain, self).__init__()
        with self.init_scope():
            self.conv1=L.Convolution2D(1, 16, 3, 1, 1) # 1層目の畳み込み層（フィルタ数は16）
            self.conv2=L.Convolution2D(16, 64, 3, 1, 1) # 2層目の畳み込み層（フィルタ数は64）
            self.l3=L.Linear(6400, 6) #クラス分類用
    def __call__(self, x):
        h1 = F.max_pooling_2d(F.relu(self.conv1(x)), 2, 2) # 最大値プーリングは2×2，活性化関数はReLU
        h2 = F.max_pooling_2d(F.relu(self.conv2(h1)), 2, 2) 
        y = self.l3(h2)
        return y        

# ニューラルネットワークの登録
model = L.Classifier(MyChain(), lossfun=F.softmax_cross_entropy)
chainer.serializers.load_npz('result/CNN.model', model)

cap = cv2.VideoCapture(0)

with serial.Serial('COM5', timeout=0.1) as ser:

    while True:
        ret, frame = cap.read()            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        xp = int(frame.shape[1]/2)
        yp = int(frame.shape[0]/2)
        d = 200
        cv2.rectangle(gray, (xp-d, yp-d), (xp+d, yp+d), color=0, thickness=10)
        cv2.imshow('gray', gray)
        if cv2.waitKey(10) == 27:
            break
        a = ser.read()
        if a == b'1':
            gray = cv2.resize(gray[yp-d:yp + d, xp-d:xp + d],(40, 40))
            img = np.asarray(gray,dtype=np.float32)  # 型変換
            img = img[np.newaxis, np.newaxis, :, :] # 4次元テンソルに変換（1×1×8×8，バッチ数×チャンネル数×縦×横）
            x = chainer.Variable(img)
            y = model.predictor(x)
            c = F.softmax(y).data.argmax()
            print(c)
            with open('key.txt', 'r') as f:
                b = int(f.read())
            print(b)
            if b==0:
                if c!=0:
                    ser.write(b'c')
                    with open('key.txt', 'w') as f:
                       f.write(str(c))
                    print('close')
            else:
                if b==c:
                    ser.write(b'o')
                    with open('key.txt', 'w') as f:
                       f.write('0')
                    print('open')
cap.release()
