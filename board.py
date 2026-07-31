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
def logic_coordinators(y, x, board_state, move_history):
    piece = board_state[y][x]
    coordinates = []
    output = []
    
    if "b" in piece:
        return []

    if "P" in piece:
        coordinates += pawn_logic(y, x, move_history, board_state)
    elif "R" in piece:
        coordinates += straights_logic(y, x, board_state)
    elif "B" in piece:
        coordinates += diagonals_logic(y, x, board_state)
    elif "Q" in piece:
        coordinates += straights_logic(y, x, board_state)
        coordinates += diagonals_logic(y, x, board_state)
    elif "N" in piece:
        coordinates += horse_logic(y, x, board_state)
    else:
        coordinates += king_logic(y, x, board_state)

    for coordinate in coordinates:
        y, x = coordinate
        if not "w" in board_state[y][x]:
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

def horse_logic(y, x, board_state):
    directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    coordinates = []

    for dy, dx in directions:
        cy = y + dy
        cx = x + dx

        if (0 <= cy <= 7 and 0 <= cx <= 7) and not "w" in board_state[cy][cx]:
            coordinates.append((cy, cx))
            
    return coordinates

def pawn_logic(y, x, move_history, board_state):
    coordinates = []
    
    if y == 6:
        if board_state[y - 1][x] == "--" and board_state[y - 2][x] == "--":
            coordinates.append((y - 2, x))

    if board_state[y - 1][x] == "--":
        coordinates.append((y - 1, x))

    if x < 7:
        if board_state[y - 1][x + 1] != "--" and not "w" in board_state[y - 1][x + 1]:
            coordinates.append((y - 1, x + 1))
    if x > 0:
        if board_state[y - 1][x - 1] != "--" and not "w" in board_state[y - 1][x - 1]:
            coordinates.append((y - 1, x - 1))

    return coordinates

def king_logic(y, x, board_state):

    coordinates = []
    moves = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]

    for dy, dx in moves:
        cy = y + dy
        cx = x + dx

        if 0 <= cy <= 7 and 0 <= cx <= 7 and "w" in board_state[cy][cx]:
            coordinates.append((cy, cx))

    return coordinates