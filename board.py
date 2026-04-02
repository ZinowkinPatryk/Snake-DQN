import pygame
import random

class Board:
    def __init__(self, width, height, screen):
        self._width = width
        self._height = height
        self._screen = screen
        self._blockPos = [[(10 + i + (i * 50), 10 + j + (j * 50))for j in range(self._width)] for i in range(self._height)]
        self._SnakeBody = []
        self._AppleExitst = False
        self.ApplePos = self.randApplePos()

    def getBlockPos(self):
        return self._blockPos

    def setSnakeBody(self, body):
        self._SnakeBody = body

    def randApplePos(self):
        AppPos = self._blockPos[random.randint(0,self._height-1)][random.randint(0,self._width-1)]
        while AppPos in self._SnakeBody:
            AppPos = self._blockPos[random.randint(0,self._height-1)][random.randint(0,self._width-1)]
        return AppPos

    def getApplePos(self):
        return self.ApplePos

    def draw(self):
        for i in self._blockPos:
            for j in i:
                pygame.draw.rect(self._screen, (255, 255, 255), (j[0], j[1], 50, 50))

        for pos in self._SnakeBody:
                pygame.draw.rect(self._screen, (34, 139, 34), (pos[0], pos[1], 50, 50))
        if not self._AppleExitst:
            self._AppleExitst = True
            self.ApplePos = self.randApplePos()
        pygame.draw.rect(self._screen, (255, 0, 0), (self.ApplePos[0], self.ApplePos[1], 50, 50))
