import chainer
import chainer.functions as F
import chainer.links as L
import time
import copy
import numpy as np


class Environment1:

    def __init__(self, data, index):
        self.data = data
        self.index = index

    def step(self, act):

        self.odds = self.data.iloc[self.index, :]['B365H', 'B365D', 'B365A']
        self.forecast = self.data.iloc[self.index, :]['oddsHome', 'oddsDrawn', 'oddsAway']

        if act == 0:
            self.position.append(self.data.iloc[self.index, :]['']) #1

        elif act == 2:
            self.position.append(self.data.iloc[self.index, :]['']) #2

        else:
            self.position.append(self.data.iloc[self.index, :]['']) #X


        result = self.data.iloc[self.index, :][''] #result
        if act == result:
            reward = self.data.iloc[self.index, :][''] #odds
        else:
            reward = -1

        return self.odds, self.forecast, self.position, reward

env = Environment1(train)

def train_dqn(env):
    class Q_Network(chainer.Chain):

        def __init__(self, input_size, hidden_size, output_size):
            super(Q_Network, self).__init__(
                fc1=L.Linear(input_size, hidden_size),
                fc2=L.Linear(hidden_size, hidden_size),
                fc3=L.Linear(hidden_size, output_size)
            )

        def __call__(self, x):
            h = F.relu(self.fc1(x))
            h = F.relu(self.fc2(h))
            y = self.fc3(h)
            return y

        def reset(self):
            self.cleargrads()


    forecast_size = 3
    odd_size = 3
    input_size = forecast_size + odd_size

    Q = Q_Network(input_size=input_size, hidden_size=100, output_size=3)
    Q_ast = copy.deepcopy(Q)
    optimizer = chainer.optimizers.Adam()
    optimizer.setup(Q)

    epoch_num = 50
    step_max = len(env.data) - 1
    memory_size = 200
    batch_size = 20
    epsilon = 1.0
    epsilon_decrease = 1e-3
    epsilon_min = 0.1
    start_reduce_epsilon = 200
    train_freq = 10
    update_q_freq = 20
    gamma = 0.97
    show_log_freq = 5

    memory = []
    total_step = 0
    total_rewards = []
    total_losses = []

    start = time.time()
    for epoch in range(epoch_num):

        step = 0
        done = False
        total_reward = 0
        total_loss = 0

        while not done and step < step_max:

            # select act
            bet = np.random.randint(3)

            # act
            odds, forecast, position, reward = env.step(bet)

            # add memory
            memory.append((bet, odds, position, forecast, reward, done))
            if len(memory) > memory_size:
                memory.pop(0)

            # train or update q
            if len(memory) == memory_size:
                if total_step % train_freq == 0:
                    shuffled_memory = np.random.permutation(memory)
                    memory_idx = range(len(shuffled_memory))
                    for i in memory_idx[::batch_size]:
                        batch = np.array(shuffled_memory[i:i + batch_size])
                        b_bet = np.array(batch[:, 0].tolist(), dtype=np.float32)
                        b_odds = np.array(batch[:, 0].tolist(), dtype=np.float32).reshape(batch_size, -1)
                        b_forecast = np.array(batch[:, 3].tolist(), dtype=np.float32).reshape(batch_size, -1)
                        b_position = np.array(batch[:, 1].tolist(), dtype=np.int32)
                        b_reward = np.array(batch[:, 2].tolist(), dtype=np.int32)
                        b_done = np.array(batch[:, 4].tolist(), dtype=np.bool)

                        input_data = np.array(b_odds, b_forecast)

                        q = Q(input_data)
                        maxq = np.max(Q_ast(b_odds).data, axis=1)
                        target = copy.deepcopy(q.data)
                        for j in range(batch_size):
                            target[j, b_bet[j]] = b_reward[j] + gamma * maxq[j] * (not b_done[j])
                        Q.reset()
                        loss = F.mean_squared_error(q, target)
                        total_loss += loss.data
                        loss.backward()
                        optimizer.update()

                if total_step % update_q_freq == 0:
                    Q_ast = copy.deepcopy(Q)

            # epsilon
            if epsilon > epsilon_min and total_step > start_reduce_epsilon:
                epsilon -= epsilon_decrease

            # next step
            total_reward += reward
            pobs = obs
            step += 1
            total_step += 1

        total_rewards.append(total_reward)
        total_losses.append(total_loss)

        if (epoch + 1) % show_log_freq == 0:
            log_reward = sum(total_rewards[((epoch + 1) - show_log_freq):]) / show_log_freq
            log_loss = sum(total_losses[((epoch + 1) - show_log_freq):]) / show_log_freq
            elapsed_time = time.time() - start
            print('\t'.join(map(str, [epoch + 1, epsilon, total_step, log_reward, log_loss, elapsed_time])))
            start = time.time()

    return Q, total_losses, total_rewards
