# Minesweeper
NOTE THERE ARE STILL SOME BUGS IN THIS. I'M WORKING ON IT.
## How To
```
python3 game.py -d [0, 1, 2] [-s] <integer other than -1>
```
Difficulty:
* 0 | 8x8 with 10 mines
* 1 | 16x16 with 40 mines
* 2 | 16x32 with 99 mines 

## TODO
* Zero discovery algorithm sometimes marks a bomb as empty when it shouldn't.
* Zero discovery algorithm sometimes overwrites the border.
* Clock updates whenever a player moves, not whenever a time unit has passed.
* * This is due to the BFL on updateBox. If I remove it, there are some issues with
    sychronizing drawing on the board, so some artifacts get written to the screen that I don't want.
    That's an issue. Not sure how to fix it right now. I'm going to address this after I refactor the code
    so that only a couple of functions will draw.
