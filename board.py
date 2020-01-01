from consts import BOARD_HEIGHT, SIZES
from square import Square
import random
class Board:
    def __init__(self, difficulty=0, SEED=-1):
        # + 2 because of the bottom/top or left/right
        self.width = SIZES[difficulty][0]
        self.height = SIZES[difficulty][1]
        self.num_mines = SIZES[difficulty][2]
        self.board = []
        self.mines = []
        self.seed = SEED

    def getRandomSquare(self):
        return random.randint(0, self.height - 1), random.randint(0, self.width - 1)

    def getAdjacentSquares(self, y, x):
        adj = []
        # upper mid
        if y - 1 >= 0:
            adj.append((y - 1, x))
        # mid left
        if x - 1 >= 0:
            adj.append((y, x - 1))
        # mid right
        if x + 1 <= self.width - 1:
            adj.append((y, x + 1))
        # bottom mid
        if y + 1 <= self.height - 1:
            adj.append((y + 1, x))
        return adj

    def countAdjacentSquares(self, y, x):
        count = 0
        # upper left
        if y - 1 >= 0:
            if x - 1 >= 0:
                if self.board[y - 1][x - 1].is_mine:
                    count += 1
        # upper mid
        if y - 1 >= 0:
            if self.board[y - 1][x].is_mine:
                count += 1
        # upper right
        if y - 1 >= 0:
            if x + 1 <= self.width - 1:
                if self.board[y - 1][x + 1].is_mine:
                    count += 1
        # mid left
        if x - 1 >= 0:
            if self.board[y][x - 1].is_mine:
                count += 1
        # mid right
        if x + 1 <= self.width - 1:
            if self.board[y][x + 1].is_mine:
                count += 1
        # bottom left
        if y + 1 <= self.height - 1:
            if x - 1 >= 0:
                if self.board[y + 1][x - 1].is_mine:
                    count += 1
        # bottom mid
        if y + 1 <= self.height - 1:
            if self.board[y + 1][x].is_mine:
                count += 1
        # bottom right
        if y + 1 <= self.height - 1:
            if x + 1 <= self.width - 1:
                if self.board[y + 1][x + 1].is_mine:
                    count += 1
        return count

    def win(self):
        for elem in self.mines:
            if not elem.marked_mine:
                return False
        return True
    def buildBoard(self):
        for y in range(0, self.height):
            self.board.append([])
            for x in range(0, self.width):
                self.board[y].append(Square(y, x))

        if self.seed != -1:
            random.seed(self.seed)

        for i in range(0,self.num_mines):
            y, x = self.getRandomSquare()
            while self.board[y][x].is_mine:
                y, x = self.getRandomSquare()
            self.board[y][x].is_mine = True
            self.mines.append(self.board[y][x])

        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.board[y][x].is_mine:
                    continue
                count = self.countAdjacentSquares(y, x)
                if count == 0:
                    self.board[y][x].char = ' '
                else:
                    self.board[y][x].char = count
