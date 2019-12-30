import argparse
import sys
import curses
import locale
from curses import wrapper
from board import Board
from consts import SIZES
from debug import DEBUG

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

debug = False
DIFFICULTY = -1

y_min = 0
y_max = None
x_min = 0
x_max = None


def displayBoard(window, b):
    window.move(1, 1)
    for row in b.board:
        for column in row:
            # window.addch(curses.ACS_CKBOARD)
            if column.char == None:
                window.addch(curses.ACS_CKBOARD)
            else:
                window.addch(str(column.char))
        y, x = window.getyx() 
        window.move(y + 1, 1)
    window.refresh()

def zeroHelper(stdscr, queue, sq, y, x):
    sq.marked_not_mine = True
    stdscr.move(y + 1, x + 1)
    stdscr.addch(' ')
    queue.append((y, x))

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

def main(stdscr):
    game = stdscr.subwin(SIZES[DIFFICULTY][0] + 2, SIZES[DIFFICULTY][1] + 2, 0, 0)
    curses.cbreak()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    
    _board = Board(curses.ACS_CKBOARD, DIFFICULTY)
    game.box(curses.ACS_VLINE, curses.ACS_HLINE) 
    _board.buildBoard()


    displayBoard(stdscr, _board)
    stdscr.move(1, 1)

    while True:
        # Only use y and x when moving the cursor.
        # All other math should be done using board_y, board_x
        c = stdscr.getch()

        y, x = stdscr.getyx()
        board_y, board_x = y - 1, x - 1
        board_y, board_x = check_y_x(board_y, board_x)

        stdscr.move(y, x)
        stdscr.refresh()

        # Adjusts for the game indexing from (1, 1) to 
        # the underlying data structure indexing from (0, 0)
        curr_square = _board.board[board_y][board_x]
        if c == ord(' '):
            # Unmarked square being marked.
            if not curr_square.marked_mine and not curr_square.marked_not_mine:
                stdscr.addch('x')
                curr_square.marked_mine = True
            else:
                # Removing the x mark
                if not curr_square.marked_not_mine:
                    stdscr.addch(curses.ACS_CKBOARD)
                curr_square.marked_mine = False
            stdscr.move(y, x)
        elif c == ord('w'):
            if board_y - 1 >= y_min:
                stdscr.move(y - 1, x)
        elif c == ord('a'):
            if board_x - 1 >= x_min:
                stdscr.move(y, x - 1)
        elif c == ord('s'):
            if board_y + 1 < y_max:
                stdscr.move(y + 1, x)
        elif c == ord('d'):
            if board_x + 1 < x_max:
                stdscr.move(y, x + 1)
        elif c == ord('e'):
            if not curr_square.marked_mine:
                if curr_square.is_mine:
                    stdscr.addstr("YOU LOSE. Press any key to continue")
                    stdscr.getch()
                    break
                curr_square.marked_not_mine = True
                '''
                if curr_square.char == ' ':
                    removeZeros(stdscr, _board, board_y, board_x)
                '''
                stdscr.addch(str(curr_square.char))
                stdscr.move(y, x)
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



