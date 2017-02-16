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

# curses.initscr()
# curses.start_color()
# curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

def piece_constructor(input_char):
    def __constructor(content, name, owner, sides_to_capture=None):
        return { #TODO: make this more pythonic
            "content": content,
            "name": name,
            "owner": owner,
            "sides_to_capture": sides_to_capture
        }
    if input_char == 0:
        return __constructor(0, 'empty', None)
    elif input_char == 1:
        return __constructor(1, 'attacker', 0, 2)
    elif input_char == 2:
        return __constructor(2, 'defender', 1, 2)
    elif input_char == 3:
        return __constructor(3, 'king', 1, 4)
    elif input_char == 4:
        return __constructor(4, 'throne', None)
    elif input_char == 5:
        return __constructor(5, 'throned_king', 1, 4)
    else:
        raise Exception('bad char input')

def board_constructor(board_layout, board_size=9):
    return list(map(piece_constructor, board_layout))
    # return {
    #     "board_size": board_size,
    #     "board_layout": map(piece_constructor, board_layout)
    # }

def main(stdscr):

    # clear screen
    # stdscr.nodelay(True)
    stdscr.clear()

    # Init color pairs
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_WHITE)

    board_size = 9

    # 0 = empty, 1 = attacker, 2 = defender, 3 = king
    # 4 = unoccupied throne, 5 = king on throne
    # active_player = 0
    board = [4, 0, 0, 1, 1, 1, 0, 0, 4,
             0, 0, 0, 0, 1, 0, 0, 0, 0,
             0, 0, 0, 0, 2, 0, 0, 0, 0,
             1, 0, 0, 0, 2, 0, 0, 0, 1,
             1, 1, 2, 2, 4, 2, 2, 1, 1,
             1, 0, 0, 0, 2, 0, 0, 0, 1,
             0, 0, 0, 0, 2, 0, 0, 0, 0,
             0, 0, 0, 0, 1, 0, 1, 3, 1,
             4, 0, 0, 1, 1, 1, 0, 1, 4]
    game_state = {"active_player": 0, "board": board_constructor(board)}
    highlighted_squares = []

    def get_moves_in_range(board, start, end, step):
        found_moves = []
        for i in range(start, end, step):
            if board[i]["content"] == 0:
                found_moves.append(i)
            elif board[i]["content"] == 4:
                continue
            else:
                break
        return found_moves

    def get_moves_for_piece(coord):
        size = board_size # unnecessary
        legal_moves = []
        # print(range(coord, math.ceil(coord / size) * size))
        # Check row looking to the right if we're not in the last column
        if (coord + 1) % size != 0:
            legal_moves.extend(get_moves_in_range(
                game_state["board"],
                coord + 1,
                math.ceil(coord / size) * size if coord % size != 0
                else coord + size,
                1))

        # Check row looking to the left if we're not in the first column
        if coord % size != 0:
            legal_moves.extend(get_moves_in_range(
                game_state["board"],
                coord - 1,
                math.floor(coord / size) * size - 1,
                -1))

        if coord - size >= 0:
            legal_moves.extend(get_moves_in_range(
                game_state["board"],
                coord - size,
                -1,
                -size))

        if coord + size <= len(board):
            legal_moves.extend(get_moves_in_range(
                game_state["board"],
                coord + size,
                board_size * board_size,
                size))

        return legal_moves

    def print_board():
        def char_converter(char):
            char = char["content"] #TODO: char converter can be moved to piece_constructor
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

        for i in range(board_size * board_size):
            attr = []
            if i in highlighted_squares:
                attr.append(curses.color_pair(1))
            stdscr.addstr(math.floor(i / board_size), i % board_size, char_converter(game_state["board"][i]), *attr)

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

    def complete_move(game_state, move_start, move_end):
        def check_capture(moving_piece, adjacent_square, bounding_square):
            # TODO: add support for kings, thrones
            if adjacent_square == None:
                return False
            elif adjacent_square["content"] in [1, 2]:
                return adjacent_square["owner"] != moving_piece["owner"] \
                    and bounding_square != None \
                    and (bounding_square["owner"] == moving_piece["owner"] \
                        or bounding_square["content"] == 4)
        # check to see if enemy pieces need removed, remove them
        # check square to left
        moving_piece = game_state["board"][move_start]
        new_game_state = copy.deepcopy(game_state)
        new_game_state["board"][move_start] = piece_constructor(4) if moving_piece["content"] == 5 else piece_constructor(0)
        new_game_state["board"][move_end] = moving_piece if moving_piece["content"] != 5 else piece_constructor(3)
        new_game_state["active_player"] = (new_game_state["active_player"] + 1) % 2
        # check to the left
        adjacent_square = game_state["board"][move_end - 1] if move_end % board_size != 0 else None
        bounding_square = game_state["board"][move_end - 2] if (move_end - 1) % board_size != 0 else None
        if check_capture(moving_piece, adjacent_square, bounding_square):
            new_game_state["board"][move_end - 1] = piece_constructor(0)
        # check to the right
        adjacent_square = game_state["board"][move_end + 1] if (move_end + 1) % board_size != 0 else None
        bounding_square = game_state["board"][move_end + 2] if (move_end + 2) % board_size != 0 else None
        if check_capture(moving_piece, adjacent_square, bounding_square):
            new_game_state["board"][move_end + 1] = piece_constructor(0)
        # check a row above
        adjacent_square = game_state["board"][move_end - board_size] if (move_end - board_size) >= 0 else None
        bounding_square = game_state["board"][move_end - board_size * 2] if (move_end - board_size * 2) >= 0 else None
        if check_capture(moving_piece, adjacent_square, bounding_square):
            new_game_state["board"][move_end - board_size] = piece_constructor(0)
        # check a row below
        adjacent_square = game_state["board"][move_end + board_size] if (move_end + board_size) < board_size * board_size else None
        bounding_square = game_state["board"][move_end + board_size * 2] if (move_end + board_size * 2) < board_size * board_size else None
        if check_capture(moving_piece, adjacent_square, bounding_square):
            new_game_state["board"][move_end + board_size] = piece_constructor(0)
        return new_game_state
###
    # Set the board up

    print_board()
    cursor_loc = (math.floor(board_size / 2), math.floor(board_size / 2))

    active_square = None

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

        ####
        # Space key to select
        ####
        if c == ord(' '):
            selected_square = yx_to_point(*stdscr.getyx())
            if active_square == None:
                if game_state["board"][selected_square]["owner"] == game_state["active_player"]:
                    active_square = yx_to_point(*stdscr.getyx())
                    highlighted_squares = get_moves_for_piece(active_square)
            elif yx_to_point(*stdscr.getyx()) in highlighted_squares:
                # complete move
                highlighted_squares = []
                game_state = complete_move(game_state, active_square, selected_square)
                active_square = None
            else:
                highlighted_squares = []
                active_square = None

        # check for victory / defeat
        for i in range(board_size * board_size):
            if game_state["board"][i]["content"] in [3, 5]:
                if i in range(0, board_size + 1) \
                    or i in range(board_size * board_size - board_size, board_size * board_size) \
                    or i % board_size == 0 \
                    or (i + 1) % board_size == 0:
                        stdscr.addstr(10, 0, "Defender wins")
                        stdscr.getch()
                        return
                if (i - board_size < 0 or game_state["board"][i - board_size]["content"] in [1, 4]) \
                    and ((i + 1) % board_size == 0 or game_state["board"][i + 1]["content"] in [1, 4]) \
                    and ((i - 1) % board_size == 0 or game_state["board"][i - 1]["content"] in [1, 4]) \
                    and (i + board_size >= board_size * board_size or game_state["board"][i + board_size]["content"] in [1, 4]):
                        stdscr.addstr(10, 0, "Attacker wins")
                        stdscr.getch()
                        return

        cursor_loc = stdscr.getyx()

        print_board()

wrapper(main)
