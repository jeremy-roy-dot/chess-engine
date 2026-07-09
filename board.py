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
        self.move_history = {}  # stores move in the following form: { wP *piece* : [(2, 1) *origin*, (2, 3) *endpoint*] }

def moves(y_coordinate, x_coordinate):
    pass

# Determines the piece, set the valid move rules, calls on all relevant logics, output a list of valid coordinates
def logic_coordinators(y, x, board_state, move_history):
    pass

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

def pawn_logic(y, x, move_history, board_state):
    coordinates = []
    
    if y == 1:
        if board_state[y + 1][x] == "--" and board_state[y + 2][x] == "--":
            coordinates.append((y + 2, x))

    if board_state[y + 1][x] == "--":
        coordinates.append((y + 1, x))

    if x < 7:
        if board_state[y + 1][x + 1] != "--":
            coordinates.append((y + 1, x + 1))
    if x > 0:
        if board_state[y + 1][x - 1] != "--":
            coordinates.append((y + 1, x - 1))
    
    return coordinates
    

