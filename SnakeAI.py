import sys
import pygame
from board import Board
from snake import Snake

class SnakeAIgame():
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("SnakeAI")
        self.board = Board(10, 10, self.window)
        self.snake = Snake(self.window, self.board.getBlockPos()[5][5], self.board)
        self.xChange = 51
        self.yChange = 0
        self.score = 0
        self.frame_iteration = 0

    def getDirection(self):
        return [self.xChange, self.yChange]

    def reset(self):
        self.board = Board(10, 10, self.window)
        self.snake = Snake(self.window, self.board.getBlockPos()[5][5], self.board)
        self.xChange = 51
        self.yChange = 0
        self.score = 0
        self.frame_iteration = 0

    def play_step(self, action):
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        aktualna_glowa = self.snake.getSnakePosition()[0]
        pozycja_jablka = self.board.getApplePos()
        odleglosc_przed = abs(aktualna_glowa[0] - pozycja_jablka[0]) + abs(aktualna_glowa[1] - pozycja_jablka[1])

        if action == [0, 0, 1]:
            if self.xChange == 51 and self.yChange == 0:
                self.yChange = 51
                self.xChange = 0
            elif self.xChange == -51 and self.yChange == 0:
                self.yChange = -51
                self.xChange = 0
            elif self.xChange == 0 and self.yChange == 51:
                self.yChange = 0
                self.xChange = 51
            elif self.xChange == 0 and self.yChange == -51:
                self.yChange = 0
                self.xChange = -51
        elif action == [1, 0, 0]:
            if self.xChange == 51 and self.yChange == 0:
                self.yChange = -51
                self.xChange = 0
            elif self.xChange == -51 and self.yChange == 0:
                self.yChange = 51
                self.xChange = 0
            elif self.xChange == 0 and self.yChange == 51:
                self.yChange = 0
                self.xChange = -51
            elif self.xChange == 0 and self.yChange == -51:
                self.yChange = 0
                self.xChange = 51

        aktualna_glowa = self.snake.getSnakePosition()[0]
        nowe_x = aktualna_glowa[0] + self.xChange
        nowe_y = aktualna_glowa[1] + self.yChange
        wasAte = self.snake.move((nowe_x, nowe_y))
        reward = 0
        game_over = False
        if self.snake.checkGameOver() or self.frame_iteration > 100 * len(self.snake.getSnakePosition()):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        if wasAte:
            reward = 10
            self.score += 1
        else:
            nowa_glowa = self.snake.getSnakePosition()[0]
            odleglosc_po = abs(nowa_glowa[0] - pozycja_jablka[0]) + abs(nowa_glowa[1] - pozycja_jablka[1])
            if odleglosc_po < odleglosc_przed:
                reward = 1
            else:
                reward = -1

        self.window.fill((0, 0, 0))
        self.board.draw()
        pygame.display.flip()
        #pygame.time.delay(100)
        return reward, game_over, self.score