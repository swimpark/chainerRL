# -*- coding: utf-8 -*-

import numpy as np
import chainer
import chainer.functions as F
import chainer.links as L
import chainerrl
import copy
import time
import serial
import cv2

ser = serial.Serial('COM5')
cap = cv2.VideoCapture(0)

class QFunction(chainer.Chain):
    def __init__(self):
        super(QFunction, self).__init__()
        with self.init_scope():
            self.conv1 = L.Convolution2D(1, 8, 5, 1, 0)  # 1��ڂ̏�ݍ��ݑw�i�t�B���^����8�j
            self.conv2 = L.Convolution2D(8, 16, 5, 1, 0) # 2��ڂ̏�ݍ��ݑw�i�t�B���^����16�j
            self.l3 = L.Linear(400, 2) # �A�N�V������2�ʂ�
    def __call__(self, x, test=False):
        h1 = F.max_pooling_2d(F.relu(self.conv1(x)), ksize=2, stride=2)
        h2 = F.max_pooling_2d(F.relu(self.conv2(h1)), ksize=2, stride=2) 
        y = chainerrl.action_value.DiscreteActionValue(self.l3(h2))
        return y

def random_action():
    return np.random.choice([0, 1])

def step(_state, action):
    reward = 0
    if action==0:
        ser.write(b"p")
    else:
        ser.write(b"i")
#    time.sleep(1.0)  #�����Ɠ��삪���肷��ꍇ����
    reward = ser.read();
    return int(reward)

# USB�J��������摜���擾
def capture(ndim=3):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    xp = int(frame.shape[1]/2)
    yp = int(frame.shape[0]/2)
    d = 200
    cv2.rectangle(gray, (xp-d, yp-d), (xp+d, yp+d), color=0, thickness=10)
    cv2.imshow('gray', gray)
    gray = cv2.resize(gray[yp-d:yp + d, xp-d:xp + d],(32, 32))
    env = np.asarray(gray, dtype=np.float32)
    if ndim == 3:
        return env[np.newaxis, :, :] # 2������3�����e���\���ireplay�p�j
    else:
        return env[np.newaxis, np.newaxis, :, :] # 4�����e���\���i����p�j

gamma = 0.8
alpha = 0.5
max_number_of_steps = 15  #1���s��step��
num_episodes = 1  #�����s��

q_func = QFunction()
optimizer = chainer.optimizers.Adam(eps=1e-2)
optimizer.setup(q_func)
explorer = chainerrl.explorers.LinearDecayEpsilonGreedy(start_epsilon=0.0, end_epsilon=0.0, decay_steps=num_episodes, random_action_func=random_action)
replay_buffer = chainerrl.replay_buffer.PrioritizedReplayBuffer(capacity=10 ** 6)
phi = lambda x: x.astype(np.float32, copy=False)
agent = chainerrl.agents.DoubleDQN(
    q_func, optimizer, replay_buffer, gamma, explorer,
    replay_start_size=50, update_interval=1, target_update_interval=10, phi=phi)
agent.load('agent')

time.sleep(5.0)
for episode in range(num_episodes):  #���s�����J��Ԃ�
    state = np.array([0])
    R = 0
    reward = 0
    done = True
    ser.write(b"c")
 
    for t in range(max_number_of_steps):  #1���s�̃��[�v
        camera_state = capture(ndim=3)
        action = agent.act(camera_state)
        reward = step(state, action)
        print(t, action, reward)
        R += reward  #��V��ǉ�
#    agent.stop_episode_and_train(camera_state, reward, done)

#    print('episode : %d total reward %d' %(episode+1, R))
    print('episode : ', episode+1, 'R', R, 'statistics:', agent.get_statistics())
ser.close()
cap.release()

#agent.save('agent')
