import main
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

def highlight(y, x):
    piece = main.gs[y][x]

def straights_logic(y, x) -> list: #outputs list of tuples that represent possible moves
    coordinates = []
    for i in range(x + 1, 8): #checks columns to the right
        if main.gs[y][i] == "--":
            coordinates.append((y, i))
        else:
            coordinates.append((y, i))
            break

    for i in range(x - 1, -1, -1): #checks columns to the left
        if main.gs[y][i] == "--":
            coordinates.append((y, i))
        else:
            coordinates.append((y, i))
            break

    for i in range(y + 1, 8): #checks row below
        if main.gs[i][x] == "--":
            coordinates.append((i, x))
        else:
            coordinates.append((i, x))
            break
    
    for i in range(y - 1, -1, -1): #checks row above
        if main.gs[i][x] == "--":
            coordinates.append((i, x))
        else:
            coordinates.append((i, x))
            break
        
    return coordinates

def diagonals_logic(y, x):
    pass

def horse_logic(y, x):
    pass

