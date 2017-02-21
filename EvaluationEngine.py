
class EvaluationEngine():
    """ Give the evaluation engine a position, it will evaluate it, and on
        request it will give you the best move
    """

    def __init__(self, game_state):
        self.game_state = game_state

    def make_move(self, move_tuple):
        """ updates the gamestate to the appropriate child_node """
        self.game_state.add_child_node(move_tuple)
        self.game_state = self.game_state.child

    def set_best_move(self):
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


    def evaluate_position(self, board, row_size=9):
        # checking for win / loss should be consolidated in one place
        positional_evaluation = 0
        material_balance = 0
        for piece in board:
            if piece["content"] == 1:
                material_balance += 1
            elif piece["content"] == 2:
                material_balance -= 2

        king_position = None
        for i in range(row_size ** 2):
            if king_position == None and board[i]["content"] in [3, 5]:
                king_position = i
            elif board[i]["owner"] == 1:
                neighbors = []
                if i % row_size != 0:
                    neighbors.extend([i - row_size - 1, i - 1, i + row_size - 1])
                if (i + 1) % row_size != 0:
                    neighbors.extend([i - row_size + 1, i + 1, i + row_size + 1])
                neighbors.extend([i - row_size, i + row_size])
                neighbor_count = len(list(filter(lambda n: n >= 0 and n < row_size, neighbors)))
                if neighbor_count == 2:
                    positional_evaluation += 1/16
                if neighbor_count == 0 or neighbor_count >= 4:
                    positional_evaluation += -1/16


        # check to see if defender can escape this turn
        defender_can_escape = False
        defender_captured = False
        if king_position - row_size < 0 \
            or king_position % row_size == 0 \
            or (king_position + 1) % row_size == 0 \
            or king_position + row_size >= row_size ** 2:
                defender_can_escape = True
        elif (king_position - row_size < 0 or board[king_position - row_size]["content"] in [1, 4]) \
            and ((king_position + 1) % row_size == 0 or board[king_position + 1]["content"] in [1, 4]) \
            and (king_position % row_size == 0 or board[king_position - 1]["content"] in [1, 4]) \
            and (king_position + row_size >= row_size ** 2 or board[king_position + row_size]["content"] in [1, 4]):
                defender_captured = True

        #positional adjustments
        #   Attackers would like to have each piece in contact with exactly two other attackers

        if defender_can_escape:
            return -100
        elif defender_captured:
            return 100
        else:
            return material_balance + positional_evaluation

def evaluate_position(board, row_size=9):
    # checking for win / loss should be consolidated in one place
    positional_evaluation = 0
    material_balance = 0
    for piece in board:
        if piece["content"] == 1:
            material_balance += 1
        elif piece["content"] == 2:
            material_balance -= 2

    king_position = None
    for i in range(row_size ** 2):
        if king_position == None and board[i]["content"] in [3, 5]:
            king_position = i
        elif board[i]["owner"] == 1:
            neighbors = []
            if i % row_size != 0:
                neighbors.extend([i - row_size - 1, i - 1, i + row_size - 1])
            if (i + 1) % row_size != 0:
                neighbors.extend([i - row_size + 1, i + 1, i + row_size + 1])
            neighbors.extend([i - row_size, i + row_size])
            neighbor_count = len(list(filter(lambda n: n >= 0 and n < row_size, neighbors)))
            if neighbor_count == 2:
                positional_evaluation += 1/16
            if neighbor_count == 0 or neighbor_count >= 4:
                positional_evaluation += -1/16


    # check to see if defender can escape this turn
    defender_can_escape = False
    defender_captured = False
    if king_position - row_size < 0 \
        or king_position % row_size == 0 \
        or (king_position + 1) % row_size == 0 \
        or king_position + row_size >= row_size ** 2:
            defender_can_escape = True
    elif (king_position - row_size < 0 or board[king_position - row_size]["content"] in [1, 4]) \
        and ((king_position + 1) % row_size == 0 or board[king_position + 1]["content"] in [1, 4]) \
        and (king_position % row_size == 0 or board[king_position - 1]["content"] in [1, 4]) \
        and (king_position + row_size >= row_size ** 2 or board[king_position + row_size]["content"] in [1, 4]):
            defender_captured = True

    #positional adjustments
    #   Attackers would like to have each piece in contact with exactly two other attackers

    if defender_can_escape:
        return -100
    elif defender_captured:
        return 100
    else:
        return material_balance + positional_evaluation
