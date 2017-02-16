def main():
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

    board = [4, 0, 0, 1, 1, 1, 0, 0, 4,
             0, 0, 0, 0, 1, 0, 0, 0, 0,
             0, 0, 0, 0, 2, 0, 0, 0, 0,
             1, 0, 0, 0, 2, 0, 0, 0, 1,
             1, 1, 2, 2, 5, 2, 2, 1, 1,
             1, 0, 0, 0, 2, 0, 0, 0, 1,
             0, 0, 0, 0, 2, 0, 0, 0, 0,
             0, 0, 0, 0, 1, 0, 0, 0, 0,
             4, 0, 0, 1, 1, 1, 0, 0, 4]
    game_state = {"active_player": 0, "board": board_constructor(board)}


    def position_analyzer(game_state):
        """ Takes a game position and returns a +/- value for it """
        # positive values for attacker, negative values for defender
        attacking_pawn = piece_constructor(1)
        defending_pawn = piece_constructor(2)
        pawn_counts = (
            len([ pawn for pawn in game_state["board"] if pawn["content"] == 1]),
            len([ pawn for pawn in game_state["board"] if pawn["content"] == 2]),
        )

        print(pawn_counts)
    position_analyzer(game_state)

main()
