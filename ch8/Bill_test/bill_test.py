# -*- coding: utf-8 -*-
"""
入力の中の1の数を数えるプログラム
Copyright(c) 2019 Koji Makino and Hiromitsu Nishizaki All Rights Reserved.
"""
import numpy as np
import chainer
import chainer.functions as F
import chainer.links as L
import chainer.initializers as I
from chainer import training
from chainer.training import extensions
import serial

class MyChain(chainer.Chain):
    def __init__(self):
        super(MyChain, self).__init__()
        with self.init_scope():
            self.l1 = L.Linear(4, 10)#入力4，中間層10
            self.l2 = L.Linear(10, 10)#中間層10，中間層10
            self.l3 = L.Linear(10, 4)#中間層10，出力4
    def __call__(self, x):
        h1 = F.relu(self.l1(x))
        h2 = F.relu(self.l2(h1))
        y = self.l3(h2)
        return y        

epoch = 1000
batchsize = 8

# ニューラルネットワークの登録
model = L.Classifier(MyChain(), lossfun=F.softmax_cross_entropy)
chainer.serializers.load_npz("result/out.model", model)

# 学習結果の評価
with serial.Serial('COM5') as ser:
    while True:
        line = ser.readline()
        line = line.rstrip().decode('utf-8')
        data = line.strip().split(",")
        data = np.array(data, dtype=np.int32)
        data = data[:4]  #次元削減
        data = np.array(data, dtype=np.float32)
        x = chainer.Variable(data.reshape(1,4))
        result = F.softmax(model.predictor(x))
        print("input: {}, result: {}".format(data, result.data.argmax()))
