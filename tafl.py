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

    # stdscr.clear()
    # stdscr.addstr('Welcome to tafl! There will be one computer opponent. Press any key...')
    # computer_opponent = 1
    # stdscr.getch()
    # stdscr.clear()

    game_state = GameState([])
    stdscr.clear()
    # curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_WHITE)
    game_screen = stdscr.subwin(10, 9, 1, 1)
    highlighted_squares = []
    print_board(game_state, game_screen)
    cursor_loc = (math.floor(game_state.row_size / 2), math.floor(game_state.row_size / 2))
    active_square = None
    game_display = GameDisplay(window=game_screen, game_state=game_state)
    game_screen.cursyncup()

    while True:
        # print_board(game_state, game_screen, highlighted_squares)
        # stdscr.addstr(11,0, str(game_state.active_player))
        # game_screen.move(*cursor_loc)
        game_display.print_board()
        c = stdscr.getch()
        game_display.handle_input(c)
        # # if game_state.active_player == computer_opponent:
        # #     game_state.set_child_node(game_state.best_move)
        # #     game_state = game_state.child_node
        #     # stdscr.addstr(12,0, 'new active_player == {0}'.format(game_state.active_player))
        #     # stdscr.getch()
        # # stdscr.addstr(10, 0, str(c))
        # # game_screen.move(*cursor_loc)
        # ####
        # # Handle direction keys
        # ####
        # if c == curses.KEY_UP:
        #     cursor_loc = (max(0, cursor_loc[0] - 1), cursor_loc[1])
        # elif c == curses.KEY_RIGHT:
        #     cursor_loc = (cursor_loc[0], min(game_state.row_size - 1, cursor_loc[1] + 1))
        # elif c == curses.KEY_DOWN:
        #     cursor_loc = (min(game_state.row_size - 1, cursor_loc[0] + 1), cursor_loc[1])
        # elif c == curses.KEY_LEFT:
        #     cursor_loc = (cursor_loc[0], max(0, cursor_loc[1] - 1))
        #
        # ####
        # # Space key to select
        # ####
        # elif c == ord(' '):
        #     selected_square = cursor_loc[0]*game_state.row_size + cursor_loc[1]
        #     if active_square == None:
        #         if game_state.board[selected_square]["owner"] == game_state.active_player:
        #             active_square = selected_square
        #             highlighted_squares = game_state.possible_moves[selected_square]
        #             # stdscr.addstr(10,0, ','.join(map(str, highlighted_squares)))
        #     elif selected_square in highlighted_squares:
        #         # complete move
        #         highlighted_squares = []
        #         # game_state = complete_move(game_state, active_square, selected_square)
        #         game_state.set_child_node((active_square, selected_square))
        #         game_state = game_state.child_node
        #         # make_move((active_square, selected_square))
        #         active_square = None
        #     else:
        #         highlighted_squares = []
        #         active_square = None
        #
        # # check for victory / defeat
        # if game_state.status == "attacker_wins":
        #     stdscr.addstr(11, 0, "Attacker wins")
        #     stdscr.getch()
        #     return
        # elif game_state.status == "defender_wins":
        #     stdscr.addstr(11, 0, "Defender wins")
        #     stdscr.getch()
        #     return


wrapper(main)
