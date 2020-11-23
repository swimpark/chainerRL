# -*- coding: utf-8 -*-
"""
井戸学習問題のDQNプログラム
Copyright(c) 2019 Koji Makino and Hiromitsu Nishizaki All Rights Reserved.
"""
import numpy as np
import chainer
import chainer.functions as F
import chainer.links as L
import chainerrl
import copy

class QFunction(chainer.Chain):
    def __init__(self, obs_size, n_actions, n_hidden_channels=10):
        super(QFunction, self).__init__()
        with self.init_scope():
            self.l1=L.Linear(obs_size, n_hidden_channels)
            self.l2=L.Linear(n_hidden_channels, n_hidden_channels)
            self.l3=L.Linear(n_hidden_channels, n_actions)
    def __call__(self, x, test=False):
        h1 = F.relu(self.l1(x))
        h2 = F.relu(self.l2(h1))
        y = chainerrl.action_value.DiscreteActionValue(self.l3(h2))
        return y

def random_action():
    return np.random.choice([0, 1])
	
def step(_state, action):
    state = _state.copy()
    reward = 0
    if state[0]==0 and state[1]==1:
        if action==0:
            state[0] = 1
    elif state[0]==1 and state[1]==1:
        if action==0:
            state[0] = 0
        elif action==1:
            state[1] = 0
            reward = 1
    elif state[0]==1 and state[1]==0:
        if action==0:
            state[0] = 0
            state[1] = 1
    return np.array(state), reward

gamma = 0.8
alpha = 0.5
max_number_of_steps = 15  #1試行のstep数
num_episodes = 1  #総試行回数

q_func = QFunction(2, 2)
optimizer = chainer.optimizers.Adam(eps=1e-2)
optimizer.setup(q_func)
explorer = chainerrl.explorers.LinearDecayEpsilonGreedy(start_epsilon=0.0, end_epsilon=0.0, decay_steps=num_episodes, random_action_func=random_action)
replay_buffer = chainerrl.replay_buffer.PrioritizedReplayBuffer(capacity=10 ** 6)
phi = lambda x: x.astype(np.float32, copy=False)
agent = chainerrl.agents.DoubleDQN(
    q_func, optimizer, replay_buffer, gamma, explorer,
    replay_start_size=50, update_interval=1, target_update_interval=10, phi=phi)
agent.load('agent')

for episode in range(num_episodes):  #試行数分繰り返す
    state = np.array([1,0])
    R = 0
    reward = 0
    done = True

    for t in range(max_number_of_steps):  #1試行のループ
        action = agent.act(state)
        next_state, reward = step(state, action)
        print(state, action, reward, next_state)
        R += reward  #報酬を追加
        state = next_state
#    agent.stop_episode_and_train(state, reward, done)
    print('episode : ', episode+1, 'R', R, 'statistics:', agent.get_statistics())

#agent.save('agent')
