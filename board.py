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

def moves(y_coordinate, x_coordinate):
    pass

def highlight(y, x, board_state):
    piece = board_state[y][x]
    coordinates = straights_logic(y, x, board_state)
    coordinates.append(diagonals_logic(y, x, board_state))
    return coordinates

#Bug when clicking on boarder it will try to get to an index that is out of range and crash the app (bug happens when clicking top or bottom)
def straights_logic(y, x, board_state) -> list: #outputs list of tuples that represent possible moves

    coordinates = []
    
    directions = [1, -1]

    for direction in directions:

        current_x = x + direction
        current_y = y + direction

        vertical_done = False
        horizontal_done = False

        while 0 <= current_x <= 7 or 0 <= current_y <= 7:
            
            if not horizontal_done:
                if board_state[y][current_x] == "--":
                    coordinates.append((y, current_x))
                    current_x += direction
                else:
                    coordinates.append((y, current_x))
                    horizontal_done = True
            
            if not vertical_done:
                if board_state[current_y][x] == "--":
                    coordinates.append((current_y, x))
                    current_y += direction
                else:
                    vertical_done = True
            
            if horizontal_done and vertical_done:
                break

    return coordinates

# When clicking something on the side of the screen it logs a case that is out of boung (doesnt crash tho) (like 6, -1)
def diagonals_logic(y, x, board_state):
    coordinates = []
    
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for dy, dx in directions:

        current_y  = y + dy
        current_x = x + dx

        while 0 <= current_y <= 7 or 0 <= current_x <= 7:
            if board_state[current_y][current_x] == "--":
                coordinates.append((current_y, current_x))
                current_x += dx
                current_y += dy
            else:
                coordinates.append((current_y, current_x))
                break

    return coordinates

def horse_logic(y, x):
    pass