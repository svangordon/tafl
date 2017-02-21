#!/usr/bin/env python3
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
from GameState import GameState
from GameDisplay import GameDisplay

def main(stdscr):
    stdscr.clear()

    # # Main Menu
    # stdscr.addstr("Welcome to tafl, the ancient Norse game of Vikings. \n Computer opponent? y/n")
    # c = stdscr.getch()
    # while True:
    #     if c == ord('y'):
    #         computer_opponent = True
    #         break
    #     elif c == ord('n'):
    #         computer_opponent = False
    #         break
    # stdscr.clear()

    game_state = GameState([])
    game_screen = stdscr.subwin(10, 9, 1, 1)
    game_display = GameDisplay(window=game_screen, game_state=game_state)

    while True:
        game_display.print_board()
        c = stdscr.getch()
        game_display.handle_input(c)

wrapper(main)
