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
# curses.initscr()
# curses.start_color()
# curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

def main(stdscr):
    def print_board(game_state, window, highlighted_squares=[]):
        def char_converter(char):
            # char = char["content"] #TODO: char converter can be moved to piece_constructor
            if char == 0:
                return "."
            elif char == 1:
                return 'x'
            elif char == 2:
                return 'o'
            elif char == 3:
                return 'O'
            elif char == 4:
                return '_'
            elif char == 5:
                return '\u0332O'
            else:
                raise Exception('bad character')

        for i in range(game_state.row_size ** 2):
            attr = []
            if i in highlighted_squares:
                attr.append(curses.color_pair(1))
            window.addstr(math.floor(i / game_state.row_size), i % game_state.row_size, char_converter(game_state.board[i]["content"]), *attr)
        window.refresh()

    # clear screen
    # stdscr.nodelay(True)
    stdscr.clear()
    # # Init color pairs
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_WHITE)
    #
    game_screen = stdscr.subwin(10, 9, 1, 1)
    highlighted_squares = []

    game_state = GameState([])

    print_board(game_state, game_screen)

    cursor_loc = (math.floor(game_state.row_size / 2), math.floor(game_state.row_size / 2))

    active_square = None

    # # . 1 .
    # # 4 . 2
    # # . 3 .
    #
    while True:
        stdscr.addstr(11,0, str(game_state))
        game_screen.move(*cursor_loc)
        game_screen.cursyncup()
        c = stdscr.getch()
        stdscr.addstr(10, 0, str(c))
        game_screen.move(*cursor_loc)
        ####
        # Handle direction keys
        ####
        if c == curses.KEY_UP:
            game_screen.move(max(0, game_screen.getyx()[0] - 1), game_screen.getyx()[1])
        elif c == curses.KEY_RIGHT:
            game_screen.move(game_screen.getyx()[0], min(game_state.row_size - 1, game_screen.getyx()[1] + 1))
        elif c == curses.KEY_DOWN:
            game_screen.move(min(game_state.row_size - 1, game_screen.getyx()[0] + 1), game_screen.getyx()[1])
        elif c == curses.KEY_LEFT:
            game_screen.move(game_screen.getyx()[0], max(0, game_screen.getyx()[1] - 1))

        ####
        # Space key to select
        ####
        if c == ord(' '):
            selected_square = game_screen.getyx()[0]*game_state.row_size + game_screen.getyx()[1]
            if active_square == None:
                if game_state.board[selected_square]["owner"] == game_state.active_player:
                    active_square = selected_square
                    highlighted_squares = game_state.possible_moves[selected_square]
                    # stdscr.addstr(10,0, ','.join(map(str, highlighted_squares)))
            elif selected_square in highlighted_squares:
                # complete move
                highlighted_squares = []
                # game_state = complete_move(game_state, active_square, selected_square)
                game_state.set_child_node((active_square, selected_square))
                game_state = game_state.child_node
                active_square = None
            else:
                highlighted_squares = []
                active_square = None

        # check for victory / defeat
        if game_state.status == "attacker_wins":
            stdscr.addstr(11, 0, "Attacker wins")
            stdscr.getch()
            return
        elif game_state.status == "defender_wins":
            stdscr.addstr(11, 0, "Defender wins")
            stdscr.getch()
            return

        cursor_loc = game_screen.getyx()

        print_board(game_state, game_screen, highlighted_squares)

wrapper(main)
