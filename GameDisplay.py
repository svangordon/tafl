import math
import curses

class GameDisplay():

    def __init__(self, window, game_state, computer_opponent=True):
        self.window = window
        self.computer_opponent = computer_opponent
        self.game_state = game_state
        self.cursor_loc = (math.floor(game_state.row_size / 2), math.floor(game_state.row_size / 2))
        self.active_square = None
        self.highlighted_squares = []
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_RED)
        self.window.move(*self.cursor_loc)
        self.window.cursyncup()

    def handle_input(self, c):
        if c == curses.KEY_UP:
            self.cursor_loc = (max(0, self.cursor_loc[0] - 1), self.cursor_loc[1])
        elif c == curses.KEY_RIGHT:
            self.cursor_loc = (self.cursor_loc[0], min(self.game_state.row_size - 1, self.cursor_loc[1] + 1))
        elif c == curses.KEY_DOWN:
            self.cursor_loc = (min(self.game_state.row_size - 1, self.cursor_loc[0] + 1), self.cursor_loc[1])
        elif c == curses.KEY_LEFT:
            self.cursor_loc = (self.cursor_loc[0], max(0, self.cursor_loc[1] - 1))
        elif c == ord(' '):
            self.select_square(self.cursor_loc)

    def select_square(self, square):
        try:
            square = square[0]*self.game_state.row_size + square[1]
        except:
            pass
        if self.active_square == None:
            if self.game_state.board[square]["owner"] == self.game_state.active_player:
                self.active_square = square
        elif square in self.game_state.possible_moves[self.active_square]:
            #make a move
            self.game_state.set_child_node((self.active_square, square))
            self.game_state = self.game_state.child_node
            self.active_square = None
            if self.computer_opponent:
                self.print_board()
                curses.napms(1500)
                self.game_state.set_child_node(self.game_state.best_move)
                self.game_state = self.game_state.child_node
        else:
            self.active_square = None

    def print_board(self):
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
                return '0'
            else:
                raise Exception('bad character')

        for i in range(self.game_state.row_size ** 2):
            attr = []
            if self.active_square:
                if i == self.active_square:
                    attr.append(curses.color_pair(2))
                elif i in self.game_state.possible_moves[self.active_square]:
                    attr.append(curses.color_pair(1))
            # try:
            #     if i in self.game_state.possible_moves[self.active_square]:
            # except KeyError:
            #     pass
            self.window.addch(math.floor(i / self.game_state.row_size), i % self.game_state.row_size, ord(char_converter(self.game_state.board[i]["content"])), *attr)
        # Really look into this, and if it's the best way to do it
        self.window.move(*self.cursor_loc)
        self.window.refresh()
