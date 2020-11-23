# -*- coding: utf-8 -*-
import numpy as np
import chainer
import chainer.functions as F
import chainer.links as L
import chainer.initializers as I
from chainer import training
from chainer.training import extensions
import os

class MyChain(chainer.Chain):
    def __init__(self):
        super(MyChain, self).__init__()
        with self.init_scope():
            self.conv1=L.Convolution2D(1, 16, 3, 1, 1) # 1�w�ڂ̏�ݍ��ݑw�i�t�B���^����16�j
            self.conv2=L.Convolution2D(16, 64, 3, 1, 1) # 2�w�ڂ̏�ݍ��ݑw�i�t�B���^����64�j
            self.l3=L.Linear(6400, 6) #�N���X���ޗp
    def __call__(self, x):
        h1 = F.max_pooling_2d(F.relu(self.conv1(x)), 2, 2) # �ő�l�v�[�����O��2�~2�C�������֐���ReLU
        h2 = F.max_pooling_2d(F.relu(self.conv2(h1)), 2, 2) 
        y = self.l3(h2)
        return y        

epoch = 20
batchsize = 100

train = []
label = 0
img_dir = 'img'
for c in os.listdir(img_dir):
    print('class: {}, class id: {}'.format(c, label))
    d = os.path.join(img_dir, c)        
    imgs = os.listdir(d)
    for i in [f for f in imgs if ('png' in f)]:
        train.append([os.path.join(d, i), label])            
    label += 1
train = chainer.datasets.LabeledImageDataset(train, '.')    

# �j���[�����l�b�g���[�N�̓o�^
model = L.Classifier(MyChain(), lossfun=F.softmax_cross_entropy)
optimizer = chainer.optimizers.Adam()
optimizer.setup(model)

# �C�e���[�^�̒�`
train_iter = chainer.iterators.SerialIterator(train, batchsize)# �w�K�p

# �A�b�v�f�[�^�̓o�^
updater = training.StandardUpdater(train_iter, optimizer)

# �g���[�i�[�̓o�^
trainer = training.Trainer(updater, (epoch, 'epoch'))

# �w�K�󋵂̕\����ۑ�
trainer.extend(extensions.LogReport())#���O
#trainer.extend(extensions.Evaluator(test_iter, model))# �G�|�b�N���̕\��
trainer.extend(extensions.PrintReport(['epoch', 'main/loss','main/accuracy', 'elapsed_time'] ))#�v�Z��Ԃ̕\��
#trainer.extend(extensions.dump_graph('main/loss'))#�j���[�����l�b�g���[�N�̍\��
#trainer.extend(extensions.PlotReport(['main/loss', 'validation/main/loss'], 'epoch',file_name='loss.png'))#�덷�̃O���t
#trainer.extend(extensions.PlotReport(['main/accuracy', 'validation/main/accuracy'],'epoch', file_name='accuracy.png'))#���x�̃O���t
#trainer.extend(extensions.snapshot(), trigger=(100, 'epoch'))# �ĊJ�̂��߂̃t�@�C���o��
#chainer.serializers.load_npz("result/snapshot_iter_500", trainer)#�ĊJ�p

# �w�K�J�n
trainer.run()

# �r����Ԃ̕ۑ�
chainer.serializers.save_npz('result/CNN.model', model)

