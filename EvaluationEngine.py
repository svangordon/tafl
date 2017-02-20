
def evaluate_position(board, row_size=9):
    # checking for win / loss should be consolidated in one place
    material_balance = 0
    for piece in board:
        if piece["content"] == 1:
            material_balance += 1
        elif piece["content"] == 2:
            material_balance -= 2

    king_position = None
    for i in range(row_size ** 2):
        if board[i]["content"] in [3, 5]:
            king_position = i
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
    if defender_can_escape:
        return -100
    elif defender_captured:
        return 100
    else:
        return material_balance
