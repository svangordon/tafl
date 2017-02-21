from GameState import GameState
from GameDisplay import GameDisplay

class Game():

    def __init__(self, game_state=GameState([]), game_display=None, players={0: 'human', 1: 'cpu'}):
        self._game_state = game_state
        self.game_display = game_display
        self.players = players
        self.row_size = game_state.row_size
        test_node = self.game_state

    @property
    def game_state(self):
        def last_child(node):
            if node.child_node:
                return last_child(node.child_node)
            return node
        return last_child(self._game_state)

    def get_board(self):
        """ Return a board suitable for the game_display to show"""
        if self.game_state.previous_moves:
            m = self.game_state.previous_moves[-1]
        else:
            m = ()
        return {
            "active_player": self.game_state.active_player,
            "board": self.game_state.board,
            "possible_moves": self.game_state.possible_moves,
            "previous_move": (),
            "row_size": self.game_state.row_size
        }

    def make_move(self, move):
        self.game_state.set_child_node(move)
        # self.game_state = self.game_state.child_node
        #TODO: remove the below line
        self.game_display.game_board = self.get_board()
        if self.players[self.game_state.active_player] == 'cpu':
            self.make_move(self.game_state.best_move)
