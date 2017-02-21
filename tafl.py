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
from Game import Game
from GameState import GameState
from GameDisplay import GameDisplay

def main(stdscr):
    stdscr.clear()

    game_state = GameState([])

    game = Game(game_state)

    game_screen = stdscr.subwin(11, 11, 1, 1)
    game_display = GameDisplay(window=game_screen, game=game)

    game.game_display = game_display


    while True:
        game_display.print_board()
        c = stdscr.getch()
        game_display.handle_input(c)

wrapper(main)
