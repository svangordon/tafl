import math
import copy
import random
from pprint import pprint
from EvaluationEngine import evaluate_position

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
    # "active_player": 0,
    "board": init_board,
    # "ply": 0,
    # "previous_moves": [],
    # "row_size": 9,
    # "status": "in-play"
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
    def __init__(self, board, active_player=0, ply=0, previous_moves=[], row_size=9, parent=None):
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
        self.candidate_nodes = {}
        self.child_node = None
        self.parent = parent
        self.ply = ply
        self.possible_moves = {}
        self.previous_moves = previous_moves
        self.row_size = row_size
        self.evaluation = evaluate_position(board=self.board, row_size=self.row_size)
        if self.evaluation == 1000:
            self.status = 'attacker_wins'
        elif self.evaluation == -1000:
            self.status = 'defender_wins'
        else:
            self.status = 'in-play'
        self.set_possible_moves()
        self.set_candidate_nodes()
        self.best_move = self.get_best_move()
    # @property
    # def evaluation(self):
    #     # checking for win / loss should be consolidated in one place
    #     if self.status == "defender_wins":
    #         return -100
    #     if self.status == "attacker_wins":
    #         return 100
    #     material_balance = 0
    #     for piece in self.board:
    #         if piece["content"] == 1:
    #             material_balance += 1
    #         elif piece["content"] == 2:
    #             material_balance -= 2
    #
    #     king_position = None
    #     for i in range(len(self.board)):
    #         if self.board[i]["content"] in [3, 5]:
    #             king_position = i
    #     # check to see if defender can escape this turn
    #     defender_can_escape = False
    #     if king_position - self.row_size < 0 \
    #         or king_position % self.row_size == 0 \
    #         or (king_position + 1) % self.row_size == 0 \
    #         or king_position + self.row_size >= self.row_size ** 2:
    #             defender_can_escape = True
    #     if defender_can_escape:
    #         return -100
    #     else:
    #         return material_balance

    # @property
    def get_best_move(self):
        def evaluate_children(candidate_nodes):
            best_eval = None
            best_node = None
            # for node in [(move, candidate_node.best_move) for move, candidate_node in candidate_nodes.items()]:
            for move, candidate_node in candidate_nodes.items():
                candidate_best_move = candidate_node.best_move
                if best_eval == None \
                    or self.active_player == 0 and candidate_best_move.evaluation > best_eval \
                    or self.active_player == 1 and candidate_best_move.evaluation < best_eval:
                        best_eval = candidate_best_move.evaluation
                        best_node = move
            return self.candidate_nodes[best_node]
        if not self.candidate_nodes or self.status in ['attacker_wins', 'defender_wins']:
            return self # has no children or the game is over, so returns self
        else:
            return evaluate_children(self.candidate_nodes)

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

    #TODO: handle the case that we've made a move, and want to look further down
    # the child nodes instead of regenerating them all.
    def set_candidate_nodes(self):
        def generate_candidate_node(move_start, move_end):
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
            # new_status = self.status
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
            # if king_position in range(0, self.row_size) \
            #     or king_position in range(self.row_size * (self.row_size - 1), self.row_size ** 2) \
            #     or king_position % self.row_size == 0 \
            #     or (king_position + 1) % self.row_size == 0:
            #         new_status = 'defender_wins'
            # elif (king_position - self.row_size < 0 or new_game_board[king_position - self.row_size]["content"] in [1, 4]) \
            #     and ((king_position + 1) % self.row_size == 0 or new_game_board[king_position + 1]["content"] in [1, 4]) \
            #     and (king_position % self.row_size == 0 or new_game_board[king_position - 1]["content"] in [1, 4]) \
            #     and (king_position + self.row_size >= self.row_size ** 2 or new_game_board[king_position + self.row_size]["content"] in [1, 4]):
            #         new_status = 'attacker_wins'
            new_active_player = (self.active_player + 1) % 2
            # print('active_player ==', self.active_player, ' new_active_player ==', new_active_player)
            self.candidate_nodes[(move_start, move_end)] = GameState(board=new_game_board, active_player=new_active_player, ply=self.ply + 1, previous_moves=new_previous_moves, row_size=self.row_size, parent=self)
        if self.ply < self.max_ply and self.status == 'in-play':
            if not self.candidate_nodes:
                for i in self.possible_moves:
                    for k in self.possible_moves[i]:
                        generate_candidate_node(i, k)
            else:
                for move, candidate_node in self.candidate_nodes.items():
                    candidate_node.ply = self.ply + 1
                    candidate_node.set_candidate_nodes()

    def set_child_node(self, move):
        """
        binds self.child_node to the move(Tuple) in question. This should probably
        be converted to a getter / setter. Possibly there should only be a ref to
        parent, and the make_move method that the display fn's going to use will
        rebind.
        """
        if type(move) == tuple:
            self.child_node = self.candidate_nodes[move]
        else:
            self.child_node = move
        self.child_node.ply = 0
        self.child_node.set_candidate_nodes()

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


# game_state = GameState([])
# print("{0} {1} {2}".format(game_state.active_player, game_state.best_move.active_player, game_state.best_move.best_move.active_player))
# pprint(vars(game_state.best_move))
# game_state = GameState(**init_game_state)
# pprint(vars(game_state))
# game_state.best_move
# game_state.best_move
# game_state.set_child_node(game_state.best_move.previous_moves[-1])
# pprint(vars(game_state.child_node))
# pprint(vars(game_state.best_move))
# game_state.set_child_node((27, 9))
# pprint(vars(game_state.child_node))
# pprint(game_state.previous_moves)
# pprint(vars(game_state))
