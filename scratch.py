#!/usr/bin/env python
# coding=utf-8

    # board = [4, 0, 0, 1, 1, 1, 0, 0, 4,
    #          0, 0, 0, 0, 1, 0, 0, 0, 0,
    #          0, 0, 0, 0, 2, 0, 0, 0, 0,
    #          1, 0, 0, 0, 2, 0, 0, 0, 1,
    #          1, 1, 2, 2, 4, 2, 2, 1, 1,
    #          1, 0, 0, 0, 2, 0, 0, 0, 1,
    #          0, 0, 0, 0, 2, 0, 0, 0, 0,
    #          0, 0, 0, 0, 1, 0, 0, 0, 0,
    #          4, 0, 0, 1, 1, 1, 0, 0, 4]

import math
import copy
import curses
from curses import wrapper

curses.initscr()
# curses.start_color()
# curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

def board_constructor(board_layout, board_size=9):
    return list(map(piece_constructor, board_layout))

def main(stdscr):

    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_WHITE)
    # clear screen
    # stdscr.nodelay(True)
    stdscr.clear()

    game_screen = stdscr.subwin(9, 9, 1, 1)
    game_screen.addstr('game_screen')

    # Init color pairs

    while True:
        # stdscr.move(*cursor_loc)
        c = stdscr.getch()
        # stdscr.addstr("this is yellow", )


wrapper(main)
