# -*- coding: utf-8 -*-

import numpy as np
import chainer
import chainer.functions as F
import chainer.links as L
import chainer.initializers as I
import chainerrl
import serial
import time

class QFunction(chainer.Chain):
    def __init__(self, obs_size, n_actions, n_hidden_channels=64):
        super(QFunction, self).__init__()
        with self.init_scope():
            self.l1=L.Linear(obs_size, n_hidden_channels, initialW=I.HeNormal(scale=0.5))
            self.l2=L.Linear(n_hidden_channels, n_hidden_channels, initialW=I.HeNormal(scale=0.5))
            self.l3=L.Linear(n_hidden_channels, n_hidden_channels, initialW=I.HeNormal(scale=0.5))
            self.l4=L.Linear(n_hidden_channels, n_actions, initialW=I.HeNormal(scale=0.5))
    def __call__(self, x, test=False):
        h1 = F.tanh(self.l1(x))
        h2 = F.tanh(self.l2(h1))
        h3 = F.tanh(self.l3(h2))
        y = chainerrl.action_value.DiscreteActionValue(self.l4(h3))
        return y

def random_action():
    return np.random.choice(range(5))
 
def step(action):
    ser.write(str(action).encode('utf-8') )
    state = ser.readline()
    state = state.rstrip().decode('utf-8').split(',')
    reward = state.pop(-1)
    state = state[:3]
    return np.array(state, dtype=np.float32), float(reward)

gamma = 0.9
alpha = 0.5
max_number_of_steps = 500  #1試行のstep数
num_episodes = 1000  #総試行回数

q_func = QFunction(3, 5)
optimizer = chainer.optimizers.Adam(eps=1e-2)
optimizer.setup(q_func)
explorer = chainerrl.explorers.LinearDecayEpsilonGreedy(start_epsilon=1.0, end_epsilon=0.0, decay_steps=num_episodes*100, random_action_func=random_action)
replay_buffer = chainerrl.replay_buffer.PrioritizedReplayBuffer(capacity=10 ** 6)
phi = lambda x: x.astype(np.float32, copy=False)
agent = chainerrl.agents.DoubleDQN(
    q_func, optimizer, replay_buffer, gamma, explorer,
    replay_start_size=1000, minibatch_size=160, update_interval=1, target_update_interval=50, phi=phi)
#agent.load('agent')

ser = serial.Serial('COM6')
time.sleep(5.0)

for episode in range(num_episodes):  #試行数分繰り返す
    state = np.array([0,0,0])
    R = 0
    reward = 0
    done = False
    count=0
    ser.write(b"a")
    tmp = ser.readline()

    for t in range(max_number_of_steps):  #1試行のループ
        action = agent.act_and_train(state, reward)
        state, reward = step(action)
        if reward < 0:
            done = True
	break
        R += reward  #報酬を追加
    agent.stop_episode_and_train(state, reward, done)

    print('Episode {}: reward {} done {}, statistics: {}, epsilon {}'.format(episode+1, R, done, agent.get_statistics(), agent.explorer.epsilon))
agent.save('agent')
ser.close()
