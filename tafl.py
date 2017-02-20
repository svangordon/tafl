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
    def print_board(game_state, window):
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

        # i = 0
        # for char in [char_converter(char["content"]) for char in game_state.board]:
            # window.addstr(math.floor(i / board_size), i % board_size, char_converter(game_state["board"][i]), *attr)
        # window.addstr('subWindow')
        for i in range(game_state.row_size ** 2):
            attr = []
            if i in highlighted_squares:
                attr.append(curses.color_pair(1))
            # window.addstr(math.floor(i / game_state.row_size), i % game_state.row_size, char_converter(game_state.board[i]["content"]), *attr)
            # window.addstr(math.floor(i / game_state.row_size), i % game_state.row_size, '.')
            # window.addstr(math.floor(i / game), i % game_state.row_size, '.')
            window.addstr(math.floor(i / game_state.row_size), i % game_state.row_size, '.')
            # k = 1 if i == 1 else 2
            # try:
            # window.addstr(type(int(math.floor(i / game_state.row_size))))
            # except
            # window.addstr(k, i % game_state.row_size, '.')
        # window.addstr('hi')

    # clear screen
    # stdscr.nodelay(True)
    stdscr.clear()
    # stdscr.addstr("wasdfasdf")
    # # Init color pairs
    # curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_WHITE)
    #
    game_screen = stdscr.subwin(10, 10, 1, 1)
    # game_screen.addstr('adfsdfsdf')
    highlighted_squares = []

    game_state = GameState([])

    print_board(game_state, game_screen)
    while True:
        c = stdscr.getch()


###
    # Set the board up

    # print_board()
    # cursor_loc = (math.floor(board_size / 2), math.floor(board_size / 2))
    #
    # active_square = None
    #
    # # . 1 .
    # # 4 . 2
    # # . 3 .
    #
    # while True:
    #     stdscr.move(*cursor_loc)
    #     c = stdscr.getch()
    #     ####
    #     # Handle direction keys
    #     ####
    #     if c == curses.KEY_UP:
    #         stdscr.move(max(0, stdscr.getyx()[0] - 1), stdscr.getyx()[1])
    #     elif c == curses.KEY_RIGHT:
    #         stdscr.move(stdscr.getyx()[0], min(board_size - 1, stdscr.getyx()[1] + 1))
    #     elif c == curses.KEY_DOWN:
    #         stdscr.move(min(board_size - 1, stdscr.getyx()[0] + 1), stdscr.getyx()[1])
    #     elif c == curses.KEY_LEFT:
    #         stdscr.move(stdscr.getyx()[0], max(0, stdscr.getyx()[1] - 1))
    #
    #     ####
    #     # Space key to select
    #     ####
    #     if c == ord(' '):
    #         selected_square = yx_to_point(*stdscr.getyx())
    #         if active_square == None:
    #             if game_state["board"][selected_square]["owner"] == game_state["active_player"]:
    #                 active_square = yx_to_point(*stdscr.getyx())
    #                 highlighted_squares = get_moves_for_piece(active_square)
    #         elif yx_to_point(*stdscr.getyx()) in highlighted_squares:
    #             # complete move
    #             highlighted_squares = []
    #             game_state = complete_move(game_state, active_square, selected_square)
    #             active_square = None
    #         else:
    #             highlighted_squares = []
    #             active_square = None
    #
    #     # check for victory / defeat
    #     if game_state["status"] == "attacker_wins":
    #         stdscr.addstr(10, 0, "Attacker wins")
    #         stdscr.getch()
    #         return
    #     elif game_state["status"] == "defender_wins":
    #         stdscr.addstr(10, 0, "Defender wins")
    #         stdscr.getch()
    #         return
    #
    #     cursor_loc = stdscr.getyx()
    #
    #     print_board()

wrapper(main)
