import math
import copy
import random
from pprint import pprint

init_board = [4, 0, 0, 0, 1, 1, 0, 0, 4,
             0, 1, 0, 0, 1, 0, 0, 0, 0,
             0, 3, 1, 0, 2, 1, 0, 0, 0,
             1, 1, 0, 0, 2, 0, 0, 0, 1,
             0, 0, 2, 2, 4, 2, 2, 1, 1,
             1, 0, 0, 0, 2, 0, 0, 0, 1,
             0, 0, 0, 0, 2, 0, 0, 0, 0,
             0, 0, 0, 0, 1, 0, 0, 0, 0,
             4, 0, 0, 1, 1, 1, 0, 0, 4]

init_game_state = {
    "active_player": 0,
    "board": init_board,
    "ply": 0,
    "previous_moves": [],
    "row_size": 9,
    "status": "in-play"
    }

class GameState:
    max_ply = 2
    default_board = [
                 4, 0, 0, 1, 1, 1, 0, 0, 4,
                 0, 0, 0, 0, 1, 0, 0, 0, 0,
                 0, 0, 0, 0, 2, 0, 0, 0, 0,
                 1, 0, 0, 0, 2, 0, 0, 0, 1,
                 1, 1, 2, 2, 5, 2, 2, 1, 1,
                 1, 0, 0, 0, 2, 0, 0, 0, 1,
                 0, 0, 0, 0, 2, 0, 0, 0, 0,
                 0, 0, 0, 0, 1, 0, 0, 0, 0,
                 4, 0, 0, 1, 1, 1, 0, 0, 4]
    def __init__(self, active_player, board, ply, previous_moves, row_size, status):
        # Polymorphically set the board
        try:
            board[0]
        except IndexError:
            board = self.default_board
        try:
            dict(board[0])
        except TypeError:
            board = list(map(self.piece_constructor, board))
        self.active_player = active_player
        self.board = board
        self.child_nodes = []
        self.ply = ply
        self.possible_moves = {}
        self.previous_moves = previous_moves
        self.row_size = row_size
        self.status = status
        self.set_possible_moves()
        if self.ply < self.max_ply and self.status == 'in-play':
            for i in self.possible_moves:
                for k in self.possible_moves[i]:
                    self.generate_child_node(i, k)
        # self.evaluation = 0 #self.evaluate_position()

    @property
    def evaluation(self):
        # checking for win / loss should be consolidated in one place
        if self.status == "defender_wins":
            return -100
        if self.status == "attacker_wins":
            return 100
        material_balance = 0
        for piece in self.board:
            if piece["content"] == 1:
                material_balance += 1
            elif piece["content"] == 2:
                material_balance -= 2

        king_position = None
        for i in range(len(self.board)):
            if self.board[i]["content"] in [3, 5]:
                king_position = i
        # check to see if defender can escape this turn
        defender_can_escape = False
        if king_position - self.row_size < 0 \
            or king_position % self.row_size == 0 \
            or (king_position + 1) % self.row_size == 0 \
            or king_position + self.row_size >= self.row_size ** 2:
                defender_can_escape = True
        if defender_can_escape:
            # print('defender can escape\n')
            return -100
        else:
            # print('defender CANNOT escape\n')
            return material_balance

    @staticmethod
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

    def generate_child_node(self, move_start, move_end):
        def check_capture(moving_piece, adjacent_square, bounding_square):
            # TODO: add support for kings, thrones
            if adjacent_square == None:
                return False
            elif adjacent_square["content"] in [1, 2]:
                return adjacent_square["owner"] != moving_piece["owner"] \
                    and bounding_square != None \
                    and (bounding_square["owner"] == moving_piece["owner"] \
                        or bounding_square["content"] == 4)

        moving_piece = self.board[move_start]
        new_game_board = copy.deepcopy(self.board)
        new_game_status = self.status
        new_active_player = None
        new_previous_moves = copy.copy(self.previous_moves)
        new_previous_moves.append((move_start, move_end))
        new_game_board[move_start] = self.piece_constructor(4) if moving_piece["content"] == 5 else self.piece_constructor(0)
        new_game_board[move_end] = moving_piece if moving_piece["content"] != 5 else self.piece_constructor(3)
        # check to the left
        adjacent_square = self.board[move_end - 1] if move_end % self.row_size != 0 else None
        bounding_square = self.board[move_end - 2] if (move_end - 1) % self.row_size != 0 else None
        if check_capture(moving_piece, adjacent_square, bounding_square):
            new_game_board[move_end - 1] = self.piece_constructor(0)
        # check to the right
        adjacent_square = self.board[move_end + 1] if (move_end + 1) % self.row_size != 0 else None
        bounding_square = self.board[move_end + 2] if (move_end + 2) % self.row_size != 0 else None
        if check_capture(moving_piece, adjacent_square, bounding_square):
            new_game_board[move_end + 1] = self.piece_constructor(0)
        # check a row above
        adjacent_square = self.board[move_end - self.row_size] if (move_end - self.row_size) >= 0 else None
        bounding_square = self.board[move_end - self.row_size * 2] if (move_end - self.row_size * 2) >= 0 else None
        if check_capture(moving_piece, adjacent_square, bounding_square):
            new_game_board[move_end - self.row_size] = self.piece_constructor(0)
        # check a row below
        adjacent_square = self.board[move_end + self.row_size] if (move_end + self.row_size) < self.row_size * self.row_size else None
        bounding_square = self.board[move_end + self.row_size * 2] if (move_end + self.row_size * 2) < self.row_size * self.row_size else None
        if check_capture(moving_piece, adjacent_square, bounding_square):
            new_game_board[move_end + self.row_size] = self.piece_constructor(0)

        # Check king position for victory
        for i in range(self.row_size ** 2):
            if new_game_board[i]["content"] in [3,5]:
                king_position = i
                break
        if king_position in range(0, self.row_size) \
            or king_position in range(self.row_size * (self.row_size - 1), self.row_size ** 2) \
            or king_position % self.row_size == 0 \
            or (king_position + 1) % self.row_size == 0:
                new_game_status = 'defender_wins'
                #: in the process of debugging why it thinks 35, 34 kills the king
        # print('king_position == {0}'.format(king_position))
        if (king_position - self.row_size < 0 or new_game_board[king_position - self.row_size]["content"] in [1, 4]) \
            and ((king_position + 1) % self.row_size == 0 or new_game_board[king_position + 1]["content"] in [1, 4]) \
            and (king_position % self.row_size == 0 or new_game_board[king_position - 1]["content"] in [1, 4]) \
            and (king_position + self.row_size >= self.row_size ** 2 or new_game_board[king_position + self.row_size]["content"] in [1, 4]):
                    new_game_status = 'attacker_wins'

        new_active_player = (self.active_player + 1) % 2

        self.child_nodes.append(GameState(new_active_player, new_game_board, self.ply + 1, new_previous_moves, self.row_size, new_game_status))

    def get_best_move(self):
        def evaluate_children(child_nodes):
            best_eval = None
            best_node = None
            for node in [child_node.get_best_move() for child_node in child_nodes]:
                if best_eval == None:
                    best_eval = node.evaluation
                    best_node = node
                elif self.active_player == 0 and node.evaluation > best_eval:
                    best_eval = node.evaluation
                    best_node = node
                elif self.active_player == 1 and node.evaluation < best_eval:
                    best_eval = node.evaluation
                    best_node = node
            return best_node
        if not self.child_nodes or self.status in ['attacker_wins', 'defender_wins']:
            return self # has no children or the game is over, so returns self
        else:
            return evaluate_children(self.child_nodes)

    def set_possible_moves(self):
        def get_moves_in_range(start, end, step):
            found_moves = []
            for i in range(start, end, step):
                if self.board[i]["content"] == 0:
                    found_moves.append(i)
                elif self.board[i]["content"] == 4:
                    continue
                else:
                    break
            return found_moves
        for coord in range(self.row_size ** 2):
            if self.board[coord]["owner"] == self.active_player:
                legal_moves = []
                # Check row looking to the right if we're not in the last column
                if (coord + 1) % self.row_size != 0:
                    legal_moves.extend(get_moves_in_range(
                        coord + 1,
                        math.ceil(coord / self.row_size) * self.row_size if coord % self.row_size != 0
                        else coord + self.row_size,
                        1))
                # Check row looking to the left if we're not in the first column
                if coord % self.row_size != 0:
                    legal_moves.extend(get_moves_in_range(
                        coord - 1,
                        math.floor(coord / self.row_size) * self.row_size - 1,
                        -1))
                if coord - self.row_size >= 0:
                    legal_moves.extend(get_moves_in_range(
                        coord - self.row_size,
                        -1,
                        -self.row_size))
                if coord + self.row_size <= self.row_size ** 2:
                    legal_moves.extend(get_moves_in_range(
                        coord + self.row_size,
                        self.row_size * self.row_size,
                        self.row_size))
                if not len(legal_moves) == 0:
                    self.possible_moves[coord] = legal_moves


game_state = GameState(**init_game_state)
# game_state.get_best_move()
# pprint([(child_node.previous_moves, child_node.get_best_move().evaluation) for child_node in game_state.child_nodes])
# pprint([(child_node.previous_moves, child_node.evaluation) for child_node in game_state.child_nodes])
# game_state.get_best_move()
pprint(vars(game_state.get_best_move()))
# print(game_state.get_best_move().previous_moves[-1])
# print(str([(node.previous_moves[-1], node.evaluation) for node in game_state.child_nodes]))
# print(str(game_state.get_best_move()))
# print(str(game_state.child_nodes[0]))
