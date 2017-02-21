from GameState import GameState
from GameDisplay import GameDisplay

class Game():

    def __init__(self, game_state=GameState([]), game_display, players={0: 'human', 1: 'cpu'}):
        self.game_state = game_state
        self.game_display = game_display
        self.players = players

    def get_board(self):
        """ Return a board suitable for the game_display to show"""
        return {
            "active_player": self.game_state.active_player,
            "board": self.game_state.board,
            "possible_moves": self.game_state.possible_moves
            "row_size": self.game_state.row_size
        }

    def make_move(self, move_start, move_end):
        self.game_state.add_child_node((move_start, move_end))
        self.game_state = self.game_state.child_node
        if self.players[self.game_state.active_player] == 'cpu':
            self.make_move(*self.game_state.best_move)
