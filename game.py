import argparse
import sys
import curses
import locale
import time as t
from threading import Thread, Lock
from curses import wrapper
from board import Board
from consts import SIZES
from debug import DEBUG
from clock import Clock
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

debug = False
DIFFICULTY = -1

DRAW_LOCK = Lock()

y_min = 0
y_max = None
x_min = 0
x_max = None

def runClock(clock, time, stdscr):
    while True:
        if clock.getKill():
            break 
        clock.updateTime()
        updateBox(time, stdscr, clock.getTime(), 7)
        t.sleep(1)

def lose(stdscr):
    with DRAW_LOCK:
        stdscr.addstr("You lose!")

def displayBoard(window, b):
    with DRAW_LOCK:
        window.move(1, 1)
        for row in b.board:
            for column in row:
                window.addch(curses.ACS_CKBOARD, curses.color_pair(240))
            y, x = window.getyx() 
            window.move(y + 1, 1)
        window.move(1, 1)
        window.refresh()

def removeZeros(stdscr, b, y, x):
    queue = []
    queue.append((y, x))
    with DRAW_LOCK:
        stdscr.addch(y + 1, x + 1, ' ')
    while len(queue) != 0:
        item_y, item_x = queue.pop()
        b.board[item_y][item_x].visited = True
        if b.board[item_y][item_x].char == ' ':
            for i in b.getAdjacentSquares(item_y, item_x):
                adj = b.board[i[0]][i[1]]
                if adj.is_mine:
                    continue
                elif adj.char != ' ' and not adj.visited:
                    adj.visited = True
                    adj.marked_not_mine = True
                    with DRAW_LOCK:
                        stdscr.addch(adj.y + 1, adj.x + 1, str(adj.char))
                elif adj.char == ' ' and not adj.visited and not adj.is_mine:
                    adj.visited = True
                    with DRAW_LOCK:
                        stdscr.addch(adj.y + 1, adj.x + 1, ' ')
                    queue.append((adj.y, adj.x))
                else:
                    continue

def check_y_x(y, x):
    if y > y_max:
        y = y_max
    if y < y_min:
        y = y_min
    if x > x_max:
        x = x_max
    if x < x_min:
        x = x_min
    return y, x

def updateBox(window, game_window, value, width):
    with DRAW_LOCK:
        y, x = game_window.getyx()
        if value < 10:
            window.erase()
            window.box(curses.ACS_VLINE, curses.ACS_HLINE)
            window.addch(1, int(width / 2), str(value))
        else:
            window.addstr(1, int(width / 2), str(value))
        game_window.move(y, x)
        window.refresh()
        game_window.refresh()

def main(stdscr):

    height = SIZES[DIFFICULTY][0] + 2
    width = SIZES[DIFFICULTY][1] + 2

    game = stdscr.subwin(height, width, 0, 0)
    mines = stdscr.subwin(3, width, height, 0)
    time = stdscr.subwin(3, 7, height, width)

    curses.cbreak()
    curses.use_default_colors()

    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    
    clock = Clock()
    clock_thread = Thread(target=runClock, args=(clock, time, stdscr))

    _board = Board(DIFFICULTY)
    mines.box(curses.ACS_VLINE, curses.ACS_HLINE)
    game.box(curses.ACS_VLINE, curses.ACS_HLINE) 
    time.box(curses.ACS_VLINE, curses.ACS_HLINE)

    updateBox(mines, stdscr,_board.num_mines, width) 
    _board.buildBoard()

    displayBoard(stdscr, _board)
    stdscr.move(1, 1)
    clock_thread.start()

    while True:
        if _board.win():
            with DRAW_LOCK:
                stdscr.addstr("YOU WIN")
            clock.killClock()
            stdscr.getch()
            break
        # Only use y and x when moving the cursor.
        # All other math should be done using board_y, board_x
        with DRAW_LOCK:
            c = stdscr.getch()
            y, x = stdscr.getyx()
        board_y, board_x = y - 1, x - 1
        board_y, board_x = check_y_x(board_y, board_x)
        
        with DRAW_LOCK:
            stdscr.move(y, x)
            stdscr.refresh()

        # Adjusts for the game indexing from (1, 1) to 
        # the underlying data structure indexing from (0, 0)
        curr_square = _board.board[board_y][board_x]
        if c == ord(' '):
            # Unmarked square being marked.
            if not curr_square.marked_mine and not curr_square.marked_not_mine:
                if _board.num_mines <= 0:
                    continue
                with DRAW_LOCK:
                    stdscr.addch(curses.ACS_CKBOARD, curses.color_pair(2))
                _board.num_mines -= 1
                updateBox(mines, stdscr, _board.num_mines, width)
                curr_square.marked_mine = True
            else:
                # Removing the x mark
                if not curr_square.marked_not_mine:
                    _board.num_mines += 1
                    updateBox(mines, stdscr, _board.num_mines, width)
                    with DRAW_LOCK:
                        stdscr.addch(curses.ACS_CKBOARD, curses.color_pair(240))
                curr_square.marked_mine = False
            with DRAW_LOCK:
                stdscr.move(y, x)
        elif c == ord('w'):
            if board_y - 1 >= y_min:
                with DRAW_LOCK:
                    stdscr.move(y - 1, x)
        elif c == ord('a'):
            if board_x - 1 >= x_min:
                with DRAW_LOCK:
                    stdscr.move(y, x - 1)
        elif c == ord('s'):
            if board_y + 1 < y_max:
                with DRAW_LOCK:
                    stdscr.move(y + 1, x)
        elif c == ord('d'):
            if board_x + 1 < x_max:
                with DRAW_LOCK:
                    stdscr.move(y, x + 1)
        elif c == ord('e'):
            if curr_square.visited:
                with DRAW_LOCK:
                    stdscr.refresh()
                continue
            curr_square.visited = True
            if not curr_square.marked_mine:
                if curr_square.is_mine:
                    # Lose
                    lose(stdscr)
                    clock.killClock()
                    with DRAW_LOCK:
                        stdscr.getch()
                    break
                curr_square.marked_not_mine = True
                if curr_square.char == ' ':
                    removeZeros(stdscr, _board, board_y, board_x)
                stdscr.addch(str(curr_square.char))
                stdscr.move(y, x)
        elif c == ord('q'):
            clock.killClock()
            sys.exit(0)
        stdscr.refresh()

if __name__ == "__main__":
    if debug:
        b = Board()
        b.buildBoard()
        displayBoard(None, b)
        sys.exit(0)
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--difficulty", help="Difficulty. Either a 0, 1, or 2 for easy, medium, and hard.")
    args = parser.parse_args()
    try:
        difficulty = int(args.difficulty)
    except:
        print("Difficulty must be a 0, 1, or 2.")
    if difficulty not in [0, 1, 2]:
        print("Difficulty must be a 0, 1, or 2.")
        sys.exit(1)
    DIFFICULTY = difficulty
    y_max = SIZES[DIFFICULTY][0]
    x_max = SIZES[DIFFICULTY][1]
    wrapper(main)



