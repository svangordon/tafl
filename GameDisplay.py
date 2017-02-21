import math
import curses

class GameDisplay():

    def __init__(self, window, game, computer_opponent=1):
        self.window = window
        self.computer_opponent = computer_opponent
        self.game = game
        self.cursor_loc = (math.floor(game.row_size / 2), math.floor(game.row_size / 2))
        self.active_square = None
        self.highlighted_squares = []
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_RED)
        # previous_move
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.window.move(*self.cursor_loc)
        self.window.cursyncup()
        self.game_board = self.game.get_board()
        # if self.computer_opponent == self.game.game_state.active_player:
            # self.handle_computer_move()

    def handle_input(self, c):
        if c == curses.KEY_UP:
            self.cursor_loc = (max(0, self.cursor_loc[0] - 1), self.cursor_loc[1])
        elif c == curses.KEY_RIGHT:
            self.cursor_loc = (self.cursor_loc[0], min(self.game_board["row_size"] - 1, self.cursor_loc[1] + 1))
        elif c == curses.KEY_DOWN:
            self.cursor_loc = (min(self.game_board["row_size"] - 1, self.cursor_loc[0] + 1), self.cursor_loc[1])
        elif c == curses.KEY_LEFT:
            self.cursor_loc = (self.cursor_loc[0], max(0, self.cursor_loc[1] - 1))
        elif c == ord(' '):
            self.select_square(self.cursor_loc)

    # def handle_computer_move(self):
    #     if self.computer_opponent == self.game_state.active_player:
    #         self.print_board()
    #         curses.napms(1500)
    #         self.game_state.set_child_node(self.game_state.best_move)
    #         self.game_state = self.game_state.child_node

    def select_square(self, square):
        try:
            square = square[0]*self.game_board["row_size"] + square[1]
        except:
            pass
        if self.active_square == None:
            if self.game_board["board"][square]["owner"] == self.game_board["active_player"]:
                self.active_square = square
        elif square in self.game_board["possible_moves"][self.active_square]:
            #make a move
            self.game.make_move((self.active_square, square))
            # self.game_state.set_child_node((self.active_square, square))
            # self.game_state = self.game_state.child_node
            self.active_square = None
            # self.handle_computer_move()
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

        for i in range(self.game_board["row_size"] ** 2):
            attr = 0
            if self.active_square:
                if i == self.active_square:
                    attr = curses.color_pair(2)
                    # attr.append(curses.color_pair(2))
                elif i in self.game_board["possible_moves"][self.active_square]:
                    attr = curses.color_pair(1)
                    # attr.append(curses.color_pair(1))
            # raise
            try:
                if i in self.game_board["previous_move"]:
                    # attr.append(curses.color_pair(3))
                    attr = curses.color_pair(3)
            except IndexError:
                pass

            self.window.addch(math.floor(i / self.game_board["row_size"]), i % self.game_board["row_size"], ord(char_converter(self.game_board["board"][i]["content"])), attr)

        # self.window.addstr(9,0,str(self.game_board["active_player"]))
        # Really look into this, and if it's the best way to do it
        self.window.move(*self.cursor_loc)
        self.window.refresh()
