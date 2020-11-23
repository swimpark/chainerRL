# -*- coding: utf-8 -*-
import numpy as np
import chainer
import chainer.functions as F
import chainer.links as L
import chainer.initializers as I
from chainer import training
from chainer.training import extensions
import os
import six

# モデルの定義
class RNN(chainer.Chain):
    def __init__(self, n_layers, in_units, h_units, n_out, dout): # LSTMのレイヤー数, 入力次元数, 隠れ層の次元数, 分類クラス数, LSTMのdropout率        
        super(RNN, self).__init__()
        with self.init_scope():
            self.l1 = L.NStepBiLSTM(n_layers, in_units, h_units, dout) # 双方向LSTMを使用
            self.l2 = L.Linear(h_units * 2, h_units, initialW=I.HeNormal(scale=1.0))
            self.l3 = L.Linear(h_units, n_out, initialW=I.HeNormal(scale=1.0))
    def __call__(self, xs, ys, dout=0.5):
        h, _, _ = self.l1(None, None, xs) # 初期ベクトルとしてゼロベクトルを渡す。最後のタイムステップの出力値(h)のみを利用。xsはリスト形式。
        h = F.concat(h, axis=1) # 各方向ごとの出力結果を1次元に展開（1次元の場合は次元削除）                
        h = self.l2(h)        
        h = F.dropout(h, ratio=dout)
        h = F.relu(h)
        output = self.l3(h)
        return self.loss_calc(output, ys) 
    # 損失計算
    def loss_calc(self, xs, ys):        
        #ys = F.stack(ys, axis=0)                
        ys = np.asarray(ys, dtype=np.int32)        
        loss = F.softmax_cross_entropy(xs, ys)
        chainer.report({'loss': loss}, self)
        acc = F.accuracy(xs, ys)        
        chainer.report({'accuracy': acc}, self)        
        return loss

def convert(batch, device=None):
    def to_device_batch(batch):
        if device is None:            
            return batch
        elif device < 0:
            return [chainer.dataset.to_device(device, x) for x in batch]
        else:
            xp = cuda.cupy.get_array_module(*batch) #numpy,cupy判別
            concat = xp.concatenate(batch, axis=0) #2次元的にデータ次元で結合
            sections = np.cumsum([len(x) for x in batch[:-1]], dtype='i') #各シーケンスの長さを計算
            batch = xp.split(concat, sections) #シーケンスの長さで2次元データを分割
            return chainer.dataset.to_device(device, batch) #デバイスを変換

    return {'xs': to_device_batch([x for x, _ in batch]),
            'ys': to_device_batch([y for _, y in batch])}

epoch = 20
batchsize = 16

data = []
label = []
id = 0
data_dir = './data'
for c in sorted(os.listdir(data_dir)):
    print('class: {}, class id: {}'.format(c, id))
    d = os.path.join(data_dir, c)        
    files = os.listdir(d)
    for i in [ft for ft in files if ('txt' in ft)]:
        #print(os.path.join(d, i))
        with open(os.path.join(d, i), mode='r') as f:
            temp = []
            for line in f.readlines():
                t = line.strip().split(',')
                temp.append(t)            
        temp = np.array(temp, dtype=np.float32)        
        ave = np.mean(temp)
        var = np.std(temp)
        temp = (temp - ave) / var # 正規化
        data.append(temp)
        label.append(id)
    id += 1
data = np.array(data, dtype=np.float32)
label = np.array(label, dtype=np.int32)

train_source = data
train_target = label
assert len(train_source) == len(train_target) 
train = [(s, t) for s, t in six.moves.zip(train_source, train_target) ] # データセットをタプル化。

# モデルの定義
#model = RNN(1, 150, 128, 3, 0.5)
model = RNN(1, train[0][0].shape[1], 128, 4, 0.5)

# オプティマイザ
#optimizer = chainer.optimizers.Adam()
optimizer = chainer.optimizers.MomentumSGD(lr=0.01)
optimizer.setup(model)
optimizer.add_hook(chainer.optimizer_hooks.WeightDecay(5e-4))

# イタレータ
#train_iter = chainer.iterators.SerialIterator(train, args.batchsize, True, True)
train_iter = chainer.iterators.SerialIterator(train, batchsize, True, True)

# アップデータ
updater = training.StandardUpdater(train_iter, optimizer, converter=convert)

trainer = training.Trainer(updater, (epoch, 'epoch'))
trainer.extend(extensions.LogReport())
trainer.extend(extensions.PrintReport(['epoch', 'main/loss', 'main/accuracy', 'elapsed_time']))
trainer.extend(extensions.ProgressBar(update_interval=1))

#test_iter = chainer.iterators.SerialIterator(test, len(test), False, False)
#trainer.extend(extensions.Evaluator(test_iter, model))

# 5 epochごとに学習率を半分にする
trainer.extend(extensions.ExponentialShift('lr', 0.5), trigger=(5, 'epoch'))    

#trainer.extend(extensions.PlotReport(['main/loss', 'validation/main/loss'],'epoch', file_name='loss.png'))
#trainer.extend(extensions.PlotReport(['main/accuracy', 'validation/main/accuracy'],'epoch', file_name='accuracy.png'))

trainer.run()
model.to_cpu()

# Save the model and the optimizer
chainer.serializers.save_npz('result/RNN.model', model)
