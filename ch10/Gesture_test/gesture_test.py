# -*- coding: utf-8 -*-
"""
ジェスチャー認識モデル学習スクリプト
"""
import numpy as np
import chainer
import chainer.functions as F
import chainer.links as L
import chainer.initializers as I
from chainer import training
from chainer.training import extensions
import os
import six
import serial

# モデルの定義
class RNN(chainer.Chain):
    def __init__(self, n_layers, in_units, h_units, n_out, dout): # LSTMのレイヤー数, 入力次元数, 隠れ層の次元数, 分類クラス数, LSTMのdropout率        
        super(RNN, self).__init__()
        with self.init_scope():
            self.l1 = L.NStepBiLSTM(n_layers, in_units, h_units, dout) # 双方向LSTMを使用
            self.l2 = L.Linear(h_units * 2, h_units, initialW=I.HeNormal(scale=1.0))
            self.l3 = L.Linear(h_units, n_out, initialW=I.HeNormal(scale=1.0))
    # フォワード処理＆損失計算
    def __call__(self, xs):
        h, _, _ = self.l1(None, None, xs) 
        h = F.concat(h, axis=1) 
        h = self.l2(h)
        h = F.relu(h)
        output = self.l3(h)
        pp = F.softmax(output) # 事後確率の計算
        y = F.argmax(pp, axis=1)
        return y

# モデルの定義
model = RNN(1, 3, 128, 4, 0.5)
chainer.serializers.load_npz('result/RNN.model', model)

with serial.Serial('COM6', 115200) as ser:
    while True:
        temp = []
        gn = ser.readline()
        gn = gn.strip()
        with open('temp.txt', 'w') as f:
            for i in range(50):
                t = ser.readline()
                line = t.rstrip().decode('utf-8')
                f.write(line+'\n')
                t = t.rstrip().decode('utf-8').split(',')
                temp.append(t)

        temp = np.array(temp, dtype=np.float32)        
        ave = np.mean(temp)
        var = np.std(temp)
        temp = (temp - ave) / var # 正規化（正規化は不要かもしれません）
        data = [temp]
        y = model(data)
        print(y)
