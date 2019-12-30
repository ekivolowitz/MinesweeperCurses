from consts import BOARD_HEIGHT, SIZES
from square import Square
import random
class Board:
    def __init__(self, curses, difficulty=0):
        # + 2 because of the bottom/top or left/right
        self.default = curses
        self.width = SIZES[difficulty][0]
        self.height = SIZES[difficulty][1]
        self.num_mines = SIZES[difficulty][2]
        self.board = []
        self.num_placed_mines = 0

    def getRandomSquare(self):
        return random.randint(0, self.height - 1), random.randint(0, self.width - 1)

    def buildBoard(self):
        for y in range(0, self.height):
            self.board.append([])
            for x in range(0, self.width):
                self.board[y].append(Square(y, x))
        for i in range(0,self.num_mines):
            y, x = self.getRandomSquare()
            while self.board[y][x].is_mine:
                y, x = self.getRandomSquare()
            self.board[y][x].is_mine = True
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.board[y][x].is_mine:
                    continue
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
                if count == 0:
                    self.board[y][x].char = ' '
                else:
                    self.board[y][x].char = count
