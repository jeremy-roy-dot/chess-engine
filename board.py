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
    checkmate = False
    piece = board_state[y][x]
    coordinates = []
    legal_moves = []
    
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
        coordinates += king_pseudo_move(y, x, board_state)
        row = 7 if turn == "w" else 0
        castling_left, castling_right = castling_logic(y, x, board_state, move_history, turn, row)
        if castling_left:
            coordinates.append((row, 2))
        if castling_right:
            coordinates.append((row, 6))

    #Gets King's coordinates
    ky, kx = (-1, -1)
    for move in reversed(move_history):
        if move[0] == turn + "K":
            ky, kx = move[2]
            break
    if (ky, kx) == (-1, -1):
        if turn == "b":
            ky, kx, = 0, 4
        else:
            ky, kx = 7, 4

    pinned, attackers = king_safety_protocol(ky, kx, board_state, turn)
    
    #If the selected piece is the king the move calculator already calculated all the moves possible so just send the coordinates
    if piece == turn + "K":
        return coordinates

    if len(attackers) == 2:
        return []

    #The full pinned move filtering
    if (y ,x) in pinned:     
        #Filters moves that puts the king in check if the piece is pinned straight
        if ky == y: 
            for cy, cx in coordinates:
                if cy != y:
                    continue
                legal_moves.append((cy, cx))
        elif kx == x:
            for cy, cx in coordinates:
                if cx != x:
                    continue
                legal_moves.append((cy, cx))
    
        #Filters moves that puts the king in check if the piece is pinned diagonally
        elif (y - x) == (ky - kx):
            for cy, cx in coordinates:
                if (cy - cx) != (y - x):
                    continue
                legal_moves.append((cy, cx))
        else:
            for cy, cx in coordinates:
                if (cy - cx) != (y - x):
                    continue
                legal_moves.append((cy, cx))
        coordinates = legal_moves

    if len(attackers) == 1:
        enemy_piece, ay, ax = attackers[0]
        side = -1

        if (ay, ax) in coordinates:
            legal_moves.append((ay, ax))

        #Straights
        if ay == ky:
            #Side allows me to evaluate which one between kx and ax is bigger and thus set the proper conditionals to block moves that shouldn't be allowed
            side = 1 if kx > ax else 0
            for cy, cx in coordinates:
                if side:
                    if not cx < kx or not cx > ax:
                        continue
                else:
                    if not cx > kx or not cx < ax:
                        continue
                if cy != ay:
                    continue
                legal_moves.append((cy, cx))
        elif ax == kx:
            side = 1 if ky > ay else 0
            for cy, cx in coordinates:
                if side:
                    if not cy < ky or not cy > ay:
                        continue
                else:
                    if not cy > ky or not cy < ay:
                        continue
                if cx != ax:
                    continue
                legal_moves.append((cy, cx))

        #Diagonals
        elif (ay - ax) == (ky - kx):
            side = 1 if ay > ky else 0
            for cy, cx in coordinates:
                if side:
                    if cy < ky:
                        continue
                else:
                    if cy > ky:
                        continue
                if (cy - cx) != (ay - ax):
                    continue
                legal_moves.append((cy, cx))
        elif (ay + ax) == (ky + kx):
            side = 1 if ay > ky else 0
            for cy, cx in coordinates:
                if side:
                    if cy < ky:
                        continue
                else:
                    if cy > ky:
                        continue
                if (cy + cx) != (ay + ax):
                    continue
                legal_moves.append((cy, cx))
        #Knight
        else:
            for cy, cx in coordinates:
                if (cy, cx) != (ax, ay):
                    continue
                legal_moves.append((cy, cx))

        coordinates = legal_moves

    #Filters the move list to remove all moves that takes piece's on the same
    legal_moves = []
    for cy, cx in coordinates:
        if turn in board_state[cy][cx]:
            continue
        legal_moves.append((cy, cx))

    return legal_moves

def straights_logic(y, x, board_state, directions=[1, -1]) -> list:

    coordinates = []

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
def diagonals_logic(y, x, board_state, directions=[(1, 1), (1, -1), (-1, 1), (-1, -1)]):
    coordinates = []

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
        if board_state[y - direction][x + 1] != "--" and not turn in board_state[y - direction][x + 1]:
            coordinates.append((y - direction, x + 1))
    if x > 0:
        if board_state[y - direction][x - 1] != "--" and not turn in board_state[y - direction][x - 1]:
            coordinates.append((y - direction, x - 1))

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
        _, attackers = king_safety_protocol(row, x + n, board_state, turn)
        if attackers:
            castling_right = False
    for n in range(1, 4):
        if not board_state[row][x - n] == "--":
            castling_left = False
        _, attackers = king_safety_protocol(row, x - n, board_state, turn)
        if attackers:
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
                return board_state, move_history

    #Normal moves
    board_state[y1][x1] = "--"
    board_state[y2][x2] = piece
    move_history.append([piece, (y1, x1), (y2, x2)])

    return board_state, move_history


def king_safety_protocol(y, x, board_state, turn):

    checker = 0
    attackers = [] #[piece, y, x]
    pinned = [] #[piece, y, x]
    direction = 1 if turn == "b" else -1

    diagonals = diagonals_logic(y, x, board_state)
    straights = straights_logic(y, x, board_state)
    horse = horse_logic(y, x)

    #Pawn check checker
    if x < 7 and "P" in board_state[y + direction][x + 1] and not turn in board_state[y + direction][x + 1]:
        checker += 1
        attackers.append([board_state[y + direction][x + 1], y + direction, x + 1])
    if x > 0 and "P" in board_state[y + direction][x - 1] and not turn in board_state[y + direction][x - 1]:
        checker += 1
        attackers.append([board_state[y + direction][x - 1], y + direction, x - 1])

    #Horse check checker
    for cy, cx in horse:
        if "N" in board_state[cy][cx] and not turn in board_state[cy][cx]:
            checker += 1
            attackers.append([board_state[cy][cx], cy, cx])

    #Bishop and Queen check checker
    for cy, cx in diagonals:
        if "B" in board_state[cy][cx] and not turn in board_state[cy][cx]:
            checker += 1
            attackers.append([board_state[cy][cx], cy, cx])
        elif "Q" in board_state[cy][cx] and not turn in board_state[cy][cx]:
            checker += 1
            attackers.append([board_state[cy][cx], cy, cx])

        #While running the check for the diagonals, if we hit a same color piece we just continue the ray to see if it is pinned
        if turn in board_state[cy][cx]:
            if pins(y, x, cy, cx, board_state, turn, "diagonal"):
                pinned.append((cy, cx))

    #Rook and Queen check checker
    for cy, cx in straights:
        if "R" in board_state[cy][cx] and not turn in board_state[cy][cx]:
            checker += 1
            attackers.append([board_state[cy][cx], cy, cx])
        elif "Q" in board_state[cy][cx] and not turn in board_state[cy][cx]:
            checker += 1
            attackers.append([board_state[cy][cx], cy, cx])

        #While running the check for the straights, if we hit a same color piece we just continue the ray to see if it is pinned
        if turn in board_state[cy][cx]:
            if pins(y, x, cy, cx, board_state, turn, "straight"):
                pinned.append(( cy, cx))
    
    if checker == 2: #Only moves legal are the king moves
        return pinned, attackers

    if checker == 1: #Only moves legal are king moves, capturing the attacker, getting in between the attacker and the king
        return pinned, attackers

    if checker == 0: #Anything other than moving pinned pieces or the king to death
        return pinned, attackers
    
def pins(ky, kx, y, x, board_state, turn, type):

    dy = y - ky
    dx = x - kx

    if type == "diagonal":
        direction = (dy // abs(dy), dx // abs(dx))
        coordinates = diagonals_logic(y, x, board_state, [direction])
        for ay, ax in coordinates:
            if "Q" in board_state[ay][ax] or "B" in board_state[ay][ax]:
                if not turn in board_state[ay][ax]:
                    return True

    elif type == "straight":
        if dy:
            direction = [dy // abs(dy)]
            coordinates = straights_logic(y, x, board_state, direction)
            for ay, ax in coordinates:
                if ay == ky:
                    continue
                if "Q" in board_state[ay][ax] or "R" in board_state[ay][ax]:
                    if not turn in board_state[ay][ax]:
                        return True
        else:
            direction = [dx // abs(dx)]
            coordinates = straights_logic(y, x, board_state, direction)
            for ay, ax in coordinates:
                if ax == kx:
                    continue
                if "Q" in board_state[ay][ax] or "R" in board_state[ay][ax]:
                    if not turn in board_state[ay][ax]:
                        return True
    return False

def king_pseudo_move(y, x, board_state):
    valid_moves = king_logic(y, x)
    turn = "b" if "b" in board_state[y][x] else "w"
    enemy = "b" if turn == "w" else "w"
    direction = 1 if "b" in board_state[y][x] else -1
    legal_moves = []
    enemyK_coordinates = []

    #Enemy king detection logic
    squares_difference = [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-1, -2), (-1, 2), (0, -2), (0, 2), (1, -2), (1, 2), (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)]
    for dy, dx in squares_difference:
        cy = y + dy
        cx = x + dx

        #Prevents running the full check for no reason/prevents index out of range
        if not (0 <= cy <= 7) or not (0 <= cx <= 7):
            continue

        #Filters the squares to only do square with enemy king in it
        if turn in board_state[cy][cx] or not "K" in board_state[cy][cx]:
            continue

        #gets the enemy king moves
        enemyK_coordinates = king_logic(cy, cx)
        break

    for ky, kx in valid_moves:
        valid = True
        if turn in board_state[ky][kx]:
            continue
        
        #Pawn checker
        if ky + direction <= 7 and ky + direction >= 0:
            if kx < 7:
                if board_state[ky + direction][kx + 1] == enemy + "P":
                    valid = False
                    continue
            if kx > 0:
                if board_state[ky + direction][kx - 1] == enemy + "P":
                    valid = False
                    continue

        #Horse Checker
        for ty, tx in horse_logic(ky, kx):
            if board_state[ty][tx] == enemy + "N":
                valid = False
                break
        if not valid:
            continue

        #Rook and queen checker
        board_state[y][x] = "--" #Removes king to solve no x-ray problem
        for ty, tx in straights_logic(ky, kx, board_state):
            if enemy + "R" in board_state[ty][tx] or enemy + "Q" in board_state[ty][tx]:
                valid = False
        if not valid:
            board_state[y][x] = turn + "K"
            continue

        #Bishop and queen checker
        for ty, tx in diagonals_logic(ky, kx, board_state):
            if enemy + "B" in board_state[ty][tx] or enemy + "Q" in board_state[ty][tx]:
                valid = False
        if not valid:
            board_state[y][x] = turn + "K"
            continue

        board_state[y][x] = turn + "K"

        if (ky, kx) in enemyK_coordinates:
            valid = False
            continue

        legal_moves.append((ky, kx))
        
    return legal_moves

def is_checkmate(board_state, move_history, turn):

    #Gets King's coordinates
    ky, kx = (-1, -1)
    for move in reversed(move_history):
        if move[0] == turn + "K":
            ky, kx = move[2]
            break
        if (ky, kx) == (-1, -1):
            if turn == "b":
                ky, kx, = 0, 4
            else:
                ky, kx = 7, 4
    pinned, attackers = king_safety_protocol(ky, kx, board_state, turn)

    if len(attackers) == 0:
        return False
    if king_pseudo_move(ky, kx, board_state):
        return False

    