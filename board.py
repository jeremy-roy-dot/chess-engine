class GameState():
    def __init__(self):
        self.board = [["bR", "bN","bB","bQ","bK","bB","bN","bR"],
                 ["bP", "bP","bP","bP","bP","bP","bP","bP"],
                 ["--", "--","--","--","--","--","--","--"],
                 ["--", "--","--","--","--","--","--","--"],
                 ["--", "--","--","--","--","--","--","--"],
                 ["--", "--","--","--","--","--","--","--"],
                 ["wP", "wP","wP","wP","wP","wP","wP","wP"],
                 ["wR", "wN","wB","wQ","wK","wB","wN","wR"]]
        self.move_history = []

# Determines the piece, set the valid move rules, calls on all relevant logics, output a list of valid coordinates
def logic_coordinators(y, x, board_state, move_history, turn):
    piece = board_state[y][x]
    coordinates = []
    output = []
    
    if not turn in piece:
        return []

    if "P" in piece:
        coordinates += pawn_logic(y, x, board_state, turn)
        coordinates += en_passant_logic(y, x, move_history, turn)
    elif "R" in piece:
        coordinates += straights_logic(y, x, board_state)
    elif "B" in piece:
        coordinates += diagonals_logic(y, x, board_state)
    elif "Q" in piece:
        coordinates += straights_logic(y, x, board_state)
        coordinates += diagonals_logic(y, x, board_state)
    elif "N" in piece:
        coordinates += horse_logic(y, x)
    elif "K" in piece:
        coordinates += king_logic(y, x)
        row = 7 if turn == "w" else 0
        castling_left, castling_right = castling_logic(y, x, board_state, move_history, turn, row)
        if castling_left:
            coordinates.append((row, 2))
        if castling_right:
            coordinates.append((row, 6))

    for coordinate in coordinates:
        y, x = coordinate
        if not turn in board_state[y][x]:
            output.append(coordinate)

    return output

def straights_logic(y, x, board_state) -> list:

    coordinates = []
    directions = [1, -1]

    for direction in directions:

        current_x = x + direction
        current_y = y + direction

        while 0 <= current_x <= 7:
            if board_state[y][current_x] == "--":
                coordinates.append((y, current_x))
                current_x += direction
            else:
                coordinates.append((y, current_x))
                break
            
        while 0 <= current_y <= 7:
            if board_state[current_y][x] == "--":
                coordinates.append((current_y, x))
                current_y += direction
            else:
                coordinates.append((current_y, x))
                break

    return coordinates

# When clicking something on the side of the screen it logs a case that is out of boung (doesnt crash tho) (like 6, -1)
def diagonals_logic(y, x, board_state):
    coordinates = []
    
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for dy, dx in directions:

        current_y  = y + dy
        current_x = x + dx

        while 0 <= current_y <= 7 and 0 <= current_x <= 7:
            if board_state[current_y][current_x] == "--":
                coordinates.append((current_y, current_x))
                current_x += dx
                current_y += dy
            else:
                coordinates.append((current_y, current_x))
                break

    return coordinates

def horse_logic(y, x):
    directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    coordinates = []

    for dy, dx in directions:
        cy = y + dy
        cx = x + dx

        if (0 <= cy <= 7 and 0 <= cx <= 7):
            coordinates.append((cy, cx))
            
    return coordinates

def pawn_logic(y, x, board_state, turn):
    coordinates = []
    direction = -1 if turn == "b" else 1

    if direction == 1:
        if y == 0:
            return []
        if y == 6:
            if board_state[y - 1][x] == "--" and board_state[y - 2][x] == "--":
                coordinates.append((y - 2, x))
    else:
        if y == 7:
            return []
        if y == 1:
            if board_state[y + 1][x] == "--" and board_state[y + 2][x] == "--":
                coordinates.append((y + 2, x))

    if board_state[y - (direction * 1)][x] == "--":
        coordinates.append((y - (direction * 1), x))

    if x < 7:
        if board_state[y - (direction * 1)][x + 1] != "--" and not turn in board_state[y - (direction * 1)][x + 1]:
            coordinates.append((y - (direction * 1), x + 1))
    if x > 0:
        if board_state[y - (direction * 1)][x - 1] != "--" and not turn in board_state[y - (direction * 1)][x - 1]:
            coordinates.append((y - (direction * 1), x - 1))

    return coordinates

def king_logic(y, x):

    coordinates = []
    moves = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]

    for dy, dx in moves:
        cy = y + dy
        cx = x + dx

        if 0 <= cy <= 7 and 0 <= cx <= 7:
            coordinates.append((cy, cx))

    return coordinates

def castling_logic(y, x, board_state, move_history, turn, row):
    if any(move[0] == turn + "K" for move in move_history):
        return False, False

    castling_left = True
    castling_right = True

    if any(move[0] == turn + "R" and move[1] == (row, 0) for move in move_history):
        castling_left = False
    if any(move[0] == turn + "R" and move[1] == (row, 7) for move in move_history):
        castling_right = False

    for n in range(1, 3):
        if not board_state[row][x + n] == "--":
            castling_right = False
    for n in range(1, 4):
        if not board_state[row][x - n] == "--":
            castling_left = False

    return castling_left, castling_right

def en_passant_logic(y, x, move_history, turn):

    coordinates = []
    direction = -1 if turn == "w" else 1

    if not move_history:
        return coordinates

    if "P" in move_history[-1][0] and not turn in move_history[-1][0] and abs(move_history[-1][1][0] - move_history[-1][2][0]) == 2:
        if move_history[-1][2][0] == y:
            if x < 7 and move_history[-1][2][1] + 1 == x:
                coordinates.append((y + direction, x - 1))
            if x > 0 and move_history[-1][2][1] - 1 == x:
                coordinates.append((y + direction, x + 1))

    return coordinates
        
def move(y1, x1, y2, x2, board_state, move_history):
    piece = board_state[y1][x1]
    turn = piece[0]
    row = 0 if turn == "b" else 7

    if "K" in piece: #Castling
        if (x1 - x2) == 2:
            board_state[row][x1] = "--"
            board_state[row][x2] = piece
            board_state[row][0] = "--"
            board_state[row][x2 + 1] = turn + "R"
            move_history.append([piece, (y1, x1), (y2, x2)])
            return (board_state, move_history)
        elif (x1 - x2) == -2:
            board_state[row][x1] = "--"
            board_state[row][x2] = piece
            board_state[row][7] = "--"
            board_state[row][x2 - 1] = turn + "R"
            move_history.append([piece, (y1, x1), (y2, x2)])
            return (board_state, move_history)

    if "P" in piece: #En Passant
        if x1 != x2:
            if board_state[y2][x2] == "--":
                board_state[y1][x1] = "--"
                board_state[y2][x2] = piece
                board_state[y1][x2] = "--"
                move_history.append([piece, (y1, x1), (y2, x2)])

    #Normal moves
    board_state[y1][x1] = "--"
    board_state[y2][x2] = piece
    move_history.append([piece, (y1, x1), (y2, x2)])
    return (board_state, move_history)