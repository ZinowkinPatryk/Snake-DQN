class Snake:
    def __init__(self, screen, position, board):
        self._screen = screen
        self._bodyLenght = 1
        self._position = [(position[0], position[1])]
        self._board = board
        self._board.setSnakeBody(self._position)

    def move(self, newHeadPosition): # direction -> new [posX, posY]
        self._position.insert(0, newHeadPosition)
        if not self.Ate():
            self._position.pop()
        self._board.setSnakeBody(self._position)
        return self.Ate()

    def getSnakePosition(self):
        return self._position

    def Ate(self):
        if self._position[0] == self._board.getApplePos():
            self._bodyLenght += 1
            self._board._AppleExitst = False
            return True
        return False

    def checkGameOver(self):
        if (self._position[0][0] < 0 or self._position[0][1] < 0 or self._position[0][0] > self._board.getBlockPos()[-1][0][0]
                or self._position[0][1] > self._board.getBlockPos()[-1][-1][1]):
            return True
        if self._position[0] in self._position[1::]:
            return True
        return False
