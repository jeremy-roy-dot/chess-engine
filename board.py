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
    for i in range(len(main.gs[y])):
        if i == x:
            continue
        case = main.gs[y][i]
        if case != "--":
            coordinates.append(i)
    if not coordinates:
        for n in range(8):
            if n == x:
                continue
            coordinates.append((y, n))
    else:
        coordinates.append(x)
        coordinates.sort()
        idx = coordinates.index(x)

    return coordinates

def diagonals_logic(y, x):
    pass

def horse_logic(y, x):
    pass

