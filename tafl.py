import math

board_size = 9

# 0 = empty, 1 = attacker, 2 = defender, 3 = king, 4 = unoccupied throne, 5 = king on throne
board = [0, 0, 0, 1, 1, 1, 0, 0, 0,
         0, 0, 0, 0, 1, 0, 0, 0, 0,
         0, 0, 0, 0, 2, 0, 0, 0, 0,
         1, 0, 0, 0, 2, 0, 0, 0, 1,
         1, 1, 2, 2, 5, 2, 2, 1, 1,
         1, 0, 0, 0, 2, 0, 0, 0, 1,
         0, 0, 0, 0, 2, 0, 0, 0, 0,
         0, 0, 0, 0, 1, 0, 0, 0, 0,
         0, 0, 0, 1, 1, 1, 0, 0, 0 ]

def get_moves_in_range(board, start, end, step):
    found_moves = []
    for i in range(start, end, step):
        if board[i] == 0:
            found_moves.append( i )
        elif board[i] == 4:
            continue
        else:
            break
    return found_moves

def get_moves_for_piece(board, coord):
    size = int(math.sqrt(len(board))) # TODO: store this instead of recalculating
    legal_moves = []
    # print(range(coord, math.ceil(coord / size) * size))
    # Check row looking to the right if we're not in the last column
    if (coord + 1) % size != 0:
        legal_moves.extend(get_moves_in_range(board,
            coord + 1,
            math.ceil(coord / size) * size if coord % size != 0 else coord + size,
            1))

    # Check row looking to the left if we're not in the first column
    if coord % size != 0:
        legal_moves.extend(get_moves_in_range(board,
            coord - 1,
            math.floor(coord / size) * size - 1,
            -1))

    if coord - size >= 0:
        legal_moves.extend(get_moves_in_range(board,
            coord - size,
            -1,
            -size))

    if coord + size <= len(board):
        legal_moves.extend(get_moves_in_range(board,
            coord + size,
            len(board),
            size))

    return legal_moves

print(get_moves_for_piece(board, 27))
#
#     def get_rank(rank):
#         return board[rank*size:size]
#     def get_column(column):
#         return board[column::size]
# class TaflGame:
#     def __init__(self, board, size):
#         if (size == 9):
#             self.board = board
#             self.size = 9
#         self.active_player = 'attacker'
#
#     def get_moves_for_piece(self, coord):
#         # piece_rank = self.point_to_xy(coord)[1]
#         # piece_column = self.point_to_xy[0]
#         def get_rank(rank):
#             return self.board[rank*self.size:self.size]
#         def get_column(column):
#             return self.board[column::self.size]
#         print('fifth column: ')
#         print(get_column(4))
#         print('first rank: ')
#         print(get_rank(0))
#
#     # Add / rempve pieces
#     def remove_piece(self, coord):
#         try:
#             if self.board[coord] == 0 or self.board[coord] == 4:
#                 raise Exception('attempting to remove piece from empty square')
#             self.board[coord] = 0
#         except Exception as error:
#             print('caught error: ' + error)
#
#     def add_piece(self, coord, piece):
#         try:
#             if self.board[coord] != 0:
#                 raise Exception('attempting to place piece on occupied square')
#             self.board[coord] = piece
#         except Exception as error:
#             print('caught error: ' + error)
#
#     # Utility functions to convert to/from one/two dimensional array
#     def xy_to_point(self, xy):
#         return xy[0] * self.size + xy[1]
#
#     def point_to_xy(self, point):
#         return (math.floor(point / self.size), point % self.size)
#
#     # Outut the board to the console so that I can look at it
#     def print_board(self):
#         def char_converter(char):
#             if char == 0:
#                 return u"\u2B1C"
#             elif char == 1:
#                 return u'\u265f'
#             elif char == 2:
#                 return u'\u2659'
#             elif char == 3:
#                 return u'\u26C1'
#             elif char == 4:
#                 return u'\u25A0'
#             elif char == 5:
#                 return u"\u2654"
#             raise Exception('bad character')
#
#         for n in range(self.size):
#             print(''.join([ char_converter(char) for char in self.board[n * self.size : (n+1) * self.size]]))
#         print('\n')
#
#     # convert nums to nice unicode characters
#     def char_converter(char):
#         if char == 0:
#             return u"\u2B1C"
#         elif char == 1:
#             return u'\u265f'
#         elif char == 2:
#             return u'\u2659'
#         elif char == 3:
#             return u'\u26C1'
#         elif char == 4:
#             return u'\u25A0'
#         elif char == 5:
#             return u"\u2654"
#         raise Exception('bad character')
#
# class Piece:
#     """Responsible for getting their own legal moves"""
#     def __init__(self, type, owner, position):
#         self.type = type
#         self.owner = owner
#         self.position = position
#
# class Square:
#     """  """
#     def __init__(self, board, contents, throne=false):
#         self.board = board # reference to the game board
#         self.contents = contents
#         self.throne = throne
#
#     def set_contents(self, piece=None):
#         self.contents = piece
#
# game = TaflGame(board, 9)
# # print(game.xy_to_point((0,1)))
# # print(game.point_to_xy(10))
# game.remove_piece(3)
# game.print_board()
# game.get_moves_for_piece(5)
