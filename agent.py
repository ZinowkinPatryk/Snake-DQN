import numpy as np
from collections import deque
import random
import torch
from model import NeuralNetwork, Trainer

# 0 0 0 0 0 0 0 0 0 0 0 -> code for agent
# First  -> left is save ? 1 - safe, 0 - wall or snake body
# Second ->  forward is save? 1 - safe, 0 - wall or snake body
# Third ->  right is save? 1 - safe, 0 - wall or snake body
# Fourth -> motion left? 1 - yes, 0 - no     V
# fifth -> motion right? 1 - yes, 0 - no     V
# sixth -> motion down? 1 - yes, 0 - no      V
# seventh -> motion up? 1 - yes, 0 - no      V
# apple in terms of snake head
# eights -> apple left? 1 - yes, 0 - no
# ninths -> apple right? 1 - yes, 0 - no
# tenth -> apple up? 1 - yes, 0 - no
# eleventh -> apple down? 1 - yes, 0 - no

class Agent:
    def __init__(self, snakeAIgame):
        self.gameState = snakeAIgame
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=10000)
        self.model = NeuralNetwork(11, 256, 3)
        self.trainer = Trainer(self.model, lr=0.001, gamma=self.gamma)


    def getState(self):
        code = []
        snake = self.gameState.snake.getSnakePosition()
        ApplePos = self.gameState.board.getApplePos()
        blocks = self.gameState.board.getBlockPos()
        direction = self.gameState.getDirection()

        max_x = blocks[-1][-1][0]
        max_y = blocks[-1][-1][1]

        # DANGER CODE
        snakeHead = snake[0]
        if direction[0] < 0 and direction[1] == 0:  # left
            if snakeHead[0] - 51 < 10 or (snakeHead[0] - 51, snakeHead[1]) in snake[1:]:  # is forward safe?
                code.append(1)
            else:
                code.append(0)
            if snakeHead[1] - 51 < 10 or (snakeHead[0], snakeHead[1] - 51) in snake[1:]:  # is right safe?
                code.append(1)
            else:
                code.append(0)
            if snakeHead[1] + 51 > max_y or (snakeHead[0], snakeHead[1] + 51) in snake[1:]:  # is left safe ?
                code.append(1)
            else:
                code.append(0)

        elif direction[0] > 0 and direction[1] == 0:  # right
            if snakeHead[0] + 51 > max_x or (snakeHead[0] + 51, snakeHead[1]) in snake[1:]:  # is forward safe?
                code.append(1)
            else:
                code.append(0)
            if snakeHead[1] + 51 > max_y or (snakeHead[0], snakeHead[1] + 51) in snake[1:]:  # is right safe?
                code.append(1)
            else:
                code.append(0)
            if snakeHead[1] - 51 < 10 or (snakeHead[0], snakeHead[1] - 51) in snake[1:]:  # is left safe ?
                code.append(1)
            else:
                code.append(0)

        elif direction[0] == 0 and direction[1] > 0:  # down
            if snakeHead[1] + 51 > max_y or (snakeHead[0], snakeHead[1] + 51) in snake[1:]:  # is forward safe?
                code.append(1)
            else:
                code.append(0)
            if snakeHead[0] - 51 < 10 or (snakeHead[0] - 51, snakeHead[1]) in snake[1:]:  # is right safe?
                code.append(1)
            else:
                code.append(0)
            if snakeHead[0] + 51 > max_x or (snakeHead[0] + 51, snakeHead[1]) in snake[1:]:  # is left safe ?
                code.append(1)
            else:
                code.append(0)

        elif direction[0] == 0 and direction[1] < 0:  # up
            if snakeHead[1] - 51 < 10 or (snakeHead[0], snakeHead[1] - 51) in snake[1:]:  # is forward safe?
                code.append(1)
            else:
                code.append(0)
            if snakeHead[0] + 51 > max_x or (snakeHead[0] + 51, snakeHead[1]) in snake[1:]:  # is right safe?
                code.append(1)
            else:
                code.append(0)
            if snakeHead[0] - 51 < 10 or (snakeHead[0] - 51, snakeHead[1]) in snake[1:]:  # is left safe ?
                code.append(1)
            else:
                code.append(0)
        # MOTION CODE
        if direction[0] < 0 and direction[1] == 0:
            code.extend([1, 0, 0, 0])  # motion left
        elif direction[0] > 0 and direction[1] == 0:
            code.extend([0, 1, 0, 0])  # motion right
        elif direction[0] == 0 and direction[1] < 0:
            code.extend([0, 0, 1, 0])  # motion up
        elif direction[0] == 0 and direction[1] > 0:
            code.extend([0, 0, 0, 1])  # motion down
        # APPLE IN TERMS OF SNAKE HEAD CODE
        if ApplePos[0] < snakeHead[0]:
            code.append(1)
        else:
            code.append(0)
        if ApplePos[0] > snakeHead[0]:
            code.append(1)
        else:
            code.append(0)
        if ApplePos[1] < snakeHead[1]:
            code.append(1)
        else:
            code.append(0)
        if ApplePos[1] > snakeHead[1]:
            code.append(1)
        else:
            code.append(0)
        return np.array(code, dtype=int)

    def getAction(self, state):
        finalMove = [0, 0, 0]
        self.epsilon = 80 - self.n_games
        if random.randint(0, 200) < self.epsilon:
            move_index = random.randint(0, 2)
            finalMove[move_index] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move_index = torch.argmax(prediction).item()
            finalMove[move_index] = 1
        return finalMove

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.trainStep(state, action, reward, next_state, done)

    def train_long_memory(self):
        if len(self.memory) > 1000:
            mini_sample = random.sample(self.memory, 1000)
        else:
            mini_sample = self.memory

        states, action, reward, next_states, done = zip(*mini_sample)
        self.trainer.trainStep(states, action, reward, next_states, done)

def train():
    file = open("./results/gameResults.txt", "w")
    record = 0
    from SnakeAI import SnakeAIgame
    game = SnakeAIgame()
    agent = Agent(game)
    while True:
        state_old = agent.getState()
        final_move = agent.getAction(state_old)
        reward, done, score = game.play_step(final_move)
        state_new = agent.getState()
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)
        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            if score > record:
                record = score
                agent.model.save()
            file.write(f"Game {agent.n_games}: Score {score}\n")
            print(f'Gra nr: {agent.n_games} | Wynik: {score} | Rekord: {record}')
    file.close()


if __name__ == '__main__':
    train()


