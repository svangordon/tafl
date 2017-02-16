import math
import copy

def _board_constructor(board_layout):
    return list(map(_piece_constructor, board_layout))

def _piece_constructor(input_char):
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

init_board = [4, 0, 0, 1, 1, 1, 0, 0, 4,
             0, 0, 0, 0, 1, 0, 0, 0, 0,
             0, 0, 0, 0, 2, 0, 0, 0, 0,
             1, 0, 0, 0, 2, 0, 0, 0, 1,
             1, 1, 2, 2, 5, 2, 2, 1, 1,
             1, 0, 0, 0, 2, 0, 0, 0, 1,
             0, 0, 0, 0, 2, 0, 0, 0, 0,
             0, 0, 0, 0, 1, 0, 0, 0, 0,
             4, 0, 0, 1, 1, 1, 0, 0, 4]

init_game_state = {
    "active_player": 0,
    "board": _board_constructor(init_board),
    # "child_nodes": [],
    # "possible_moves": {},
    "parents": 0,
    "row_size": 9,
    "status": "in-play"
    }

class GameState:

    def __init__(self, active_player, board, parents, row_size, status):
        self.active_player = active_player
        self.board = board
        self.child_nodes = []
        self.parents = parents
        self.possible_moves = {}
        self.row_size = row_size
        self.status = status
        self.set_possible_moves()
        if self.parents < 3:
            for i in self.possible_moves:
                for k in self.possible_moves[i]:
                    self.generate_child_node(i, k)

    def set_possible_moves(self):
        for i in range(len(self.board)):
            if self.board[i]["owner"] == self.active_player:
                self.get_moves_for_piece(i)

    def get_moves_for_piece(self, coord):
        def get_moves_in_range(board, start, end, step):
            found_moves = []
            for i in range(start, end, step):
                if self.board[i]["content"] == 0:
                    found_moves.append(i)
                elif self.board[i]["content"] == 4:
                    continue
                else:
                    break
            return found_moves
        legal_moves = []
        # Check row looking to the right if we're not in the last column
        if (coord + 1) % self.row_size != 0:
            legal_moves.extend(get_moves_in_range(
                self.board,
                coord + 1,
                math.ceil(coord / self.row_size) * self.row_size if coord % self.row_size != 0
                else coord + self.row_size,
                1))

        # Check row looking to the left if we're not in the first column
        if coord % self.row_size != 0:
            legal_moves.extend(get_moves_in_range(
                self.board,
                coord - 1,
                math.floor(coord / self.row_size) * self.row_size - 1,
                -1))

        if coord - self.row_size >= 0:
            legal_moves.extend(get_moves_in_range(
                self.board,
                coord - self.row_size,
                -1,
                -self.row_size))

        if coord + self.row_size <= len(self.board):
            legal_moves.extend(get_moves_in_range(
                self.board,
                coord + self.row_size,
                self.row_size * self.row_size,
                self.row_size))
        if not len(legal_moves) == 0:
            self.possible_moves[coord] = legal_moves
        # return legal_moves

    def board_constructor(self, board_layout):
        return list(map(self.piece_constructor, board_layout))

    def piece_constructor(self, input_char):
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

        # Check for victory
        # check for victory / defeat
        #!!!: We're grabbing board_size here, from the main. should do that better
        for i in range(len(new_game_board)):
            if new_game_board[i]["content"] in [3, 5]:
                if i in range(0, self.row_size + 1) \
                    or i in range(self.row_size * self.row_size - self.row_size, self.row_size * self.row_size) \
                    or i % self.row_size == 0 \
                    or (i + 1) % self.row_size == 0:
                        new_game_status = 'defender_wins'
                if (i - self.row_size < 0 or new_game_board[i - self.row_size]["content"] in [1, 4]) \
                    and ((i + 1) % self.row_size == 0 or new_game_board[i + 1]["content"] in [1, 4]) \
                    and ((i - 1) % self.row_size == 0 or new_game_board[i - 1]["content"] in [1, 4]) \
                    and (i + self.row_size >= self.row_size * self.row_size or new_game_board[i + self.row_size]["content"] in [1, 4]):
                        new_game_status = 'attacker_wins'

        new_active_player = (self.active_player + 1) % 2

        self.child_nodes.append(GameState(new_active_player, new_game_board, self.parents + 1, self.row_size, new_game_status))

game_state = GameState(**init_game_state)
print(str(game_state))
