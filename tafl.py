#!/usr/bin/env python
# coding=utf-8

import math
import curses
from curses import wrapper

# curses.initscr()
# curses.start_color()
# curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

def main(stdscr):

    # clear screen
    # stdscr.nodelay(True)
    stdscr.clear()

    # Init color pairs
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_WHITE)

    board_size = 9

    # 0 = empty, 1 = attacker, 2 = defender, 3 = king
    # 4 = unoccupied throne, 5 = king on throne
    board = [4, 0, 0, 1, 1, 1, 0, 0, 4,
             0, 0, 0, 0, 1, 0, 0, 0, 0,
             0, 0, 0, 0, 2, 0, 0, 0, 0,
             1, 0, 0, 0, 2, 0, 0, 0, 1,
             1, 1, 2, 2, 5, 2, 2, 1, 1,
             1, 0, 0, 0, 2, 0, 0, 0, 1,
             0, 0, 0, 0, 2, 0, 0, 0, 0,
             0, 0, 0, 0, 1, 0, 0, 0, 0,
             4, 0, 0, 1, 1, 1, 0, 0, 4]

    highlighted_squares = []

    def get_moves_in_range(board, start, end, step):
        found_moves = []
        for i in range(start, end, step):
            if board[i] == 0:
                found_moves.append(i)
            elif board[i] == 4:
                continue
            else:
                break
        return found_moves

    def get_moves_for_piece(coord):
        size = int(math.sqrt(len(board)))  # TODO: store this?
        legal_moves = []
        # print(range(coord, math.ceil(coord / size) * size))
        # Check row looking to the right if we're not in the last column
        if (coord + 1) % size != 0:
            legal_moves.extend(get_moves_in_range(
                board,
                coord + 1,
                math.ceil(coord / size) * size if coord % size != 0
                else coord + size,
                1))

        # Check row looking to the left if we're not in the first column
        if coord % size != 0:
            legal_moves.extend(get_moves_in_range(
                board,
                coord - 1,
                math.floor(coord / size) * size - 1,
                -1))

        if coord - size >= 0:
            legal_moves.extend(get_moves_in_range(
                board,
                coord - size,
                -1,
                -size))

        if coord + size <= len(board):
            legal_moves.extend(get_moves_in_range(
                board,
                coord + size,
                len(board),
                size))

        return legal_moves

    def print_board():
        def char_converter(char):
            if char == 0:
                return "."
            elif char == 1:
                return 'o'
            elif char == 2:
                return 'x'
            elif char == 3:
                return 'O'
            elif char == 4:
                return '_'
            elif char == 5:
                return '\u0332O'
            else:
                raise Exception('bad character')

        for i in range(len(board)):
            attr = []
            if i in highlighted_squares:
                attr.append(curses.color_pair(1))
                stdscr.addstr(11, 0, 'found a thing')
            stdscr.addstr(math.floor(i / board_size), i % board_size, char_converter(board[i]), *attr)

    def move_cursor(direction):
        if direction == 1:
            stdscr.move(max(0, stdscr.getyx()[0] - 1), stdscr.getyx()[1])
        elif direction == 2:
            stdscr.move(stdscr.getyx()[0], min(board_size - 1, stdscr.getyx()[1] + 1))
        elif direction == 3:
            stdscr.move(min(board_size - 1, stdscr.getyx()[0] + 1), stdscr.getyx()[1])
        elif direction == 4:
            # print('left!')
            stdscr.move(stdscr.getyx()[0], max(0, stdscr.getyx()[1] - 1))
        else:
            raise Exception('bad direction: ' + direction)

    def yx_to_point(y, x):
        return y * board_size + x

    # Set the board up

    print_board()
    cursor_loc = (math.floor(board_size / 2), math.floor(board_size / 2))

    # cursor_loc = stdscr.getyx()

    active_square = None
    active_player = None


    # . 1 .
    # 4 . 2
    # . 3 .

    while True:
        direction = None
        stdscr.move(*cursor_loc)
        c = stdscr.getch()
        ####
        # Handle direction keys
        ####
        if c == curses.KEY_UP:
            stdscr.move(max(0, stdscr.getyx()[0] - 1), stdscr.getyx()[1])
        elif c == curses.KEY_RIGHT:
            stdscr.move(stdscr.getyx()[0], min(board_size - 1, stdscr.getyx()[1] + 1))
        elif c == curses.KEY_DOWN:
            stdscr.move(min(board_size - 1, stdscr.getyx()[0] + 1), stdscr.getyx()[1])
        elif c == curses.KEY_LEFT:
            stdscr.move(stdscr.getyx()[0], max(0, stdscr.getyx()[1] - 1))

        if c == ord(' '):
            selected_square = yx_to_point(*stdscr.getyx())
            if active_square == None: #think this is valid...
                if board[selected_square] != (0 and 4):
                    active_square = yx_to_point(*stdscr.getyx())
                    highlighted_squares = get_moves_for_piece(active_square)
            elif yx_to_point(*stdscr.getyx()) in highlighted_squares:
                # complete move
                stdscr.addstr(10,0,'complete move!')
                highlighted_squares = []
                pass
            else:
                highlighted_squares = []
                active_square = None


        cursor_loc = stdscr.getyx()

        print_board()

wrapper(main)
