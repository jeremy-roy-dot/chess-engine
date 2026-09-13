import board
import copy

class Boards:
    def __init__(self):
        self.calculated_boards = {} #points: board_state
        self.best_move = None #(points, (y1, x1), (y2, x2))
        self.boards = []

def bot_logic(board_state, move_history, turn):
    moves = move_finders(board_state, move_history, turn)
    best_move = board_maker(board_state, move_history, moves, turn)

    return best_move

def position_evaluation(board_state, move_history): #evaluates with the system and returns an int between roughly -30000 and 30000 where -30000 to -1 is a black advantage, 0 is perfectly equal, and 1 to 30000 is a white advantage
    points = 0
    side = 0
    wKy, wKx = (-1, -1)
    bKy, bKx = (-1, -1)
    w_pinned = None
    w_attackers = None
    b_pinned = None
    b_attackers = None

    for y in range(8):
        for x in range(8):
            piece = board_state[y][x]

            if "--" in piece:
                continue

            #determines how to multiply the points
            if "b" in piece:
                side = -1
            else:
                side = 1

            #Raw points for the pieces are the points with no conditionnals

            #Pawn points logic
            if "P" in piece:
                points += 100 * side
                #Connected pawn evaluator
                if x > 0:
                    if y > 0 and piece in board_state[y - 1][x - 1]:
                        points += 25 * side
                    if y < 7 and piece in board_state[y + 1][x - 1]:
                        points += 25 * side
                    if piece in board_state[y][x - 1]:
                        points += 10 * side
                if x < 7:
                    if y > 0 and piece in board_state[y - 1][x + 1]:
                        points += 25 * side
                    if y < 7 and piece in board_state[y + 1][x + 1]:
                        points += 25 * side
                    if piece in board_state[y][x + 1]:
                        points += 10 * side

                #Checks for doubled pawns
                doubled_pawn = 0
                for n in range(0, 8):
                    if n == x:
                        continue
                    if piece in board_state[y][n] and doubled_pawn > 1:
                        points -= 50 * side

            elif "B" in piece or "N" in piece:
                points += 300 * side
            elif "R" in piece:
                points += 500 * side
            elif "Q" in piece:
                points += 900 * side
            else:
                #stores the king position for later
                if side == -1:
                    bKy, bKx = (y, x)

                    #Checks if the king is in a corner
                    if x >= 6 or x <= 1:
                        if y == 0:
                            points += 100 * side
                else:
                    wKy, wKx = (y, x)

                    #Checks if the king is in a corner
                    if x >= 6 or x <= 1:
                        if y == 0:
                            points += 100 * side

                #Checks if the king has protection
                king_moves = board.king_pseudo_move(y, x, board_state)
                if len(king_moves) < 2:
                    points -= 100 * side
                elif 2 <= len(king_moves) <= 3:
                    points += 100 * side
                else:
                    points -= 100 * side

            legal_moves, pinned, attackers = board.logic_coordinators(y, x, board_state, move_history, turn="b" if side == -1 else "w", pinned = b_pinned if side == -1 else w_pinned, attackers = b_attackers if side == -1 else w_attackers)

            if side == -1:
                b_pinned = pinned
                b_attackers = attackers
            else:
                w_pinned = pinned
                w_attackers = attackers

            #Adds points for each possible moves, if the move is in the center of the board you get more
            for mx, my in legal_moves:
                if not 2 <= mx <= 5:
                    if side == -1:
                        if not 0 <= my <= 5:
                            points += 20 * side
                    else:
                        if not 2 <= my <= 7:
                            points += 20 * side
                    points += 15 * side
                points += 10 * side
    return points

def move_finders(board_state, move_history, turn):
    pieces = [] #stores piece same side
    moves = [] #stores moves ((y1, x1) (y2, x2))
    pinned = None
    attackers = None

    for y in range(8):
        for x in range(8):
            if turn in board_state[y][x]:
                pieces.append((y, x))

    for y, x in pieces:
        legal_moves, pinned, attackers = board.logic_coordinators(y, x, board_state, move_history, turn, pinned, attackers)
        for y2, x2 in legal_moves:
            moves.append(((y, x), (y2, x2)))

    return moves

def board_maker(board_state, move_history, moves, turn):
    best_move = None
    for pos1, pos2 in moves:
        trial_board = copy.deepcopy(board_state)
        trial_history = copy.deepcopy(move_history)
        trial_board, trial_history = board.move(pos1[0], pos1[1], pos2[0], pos2[1], trial_board, trial_history)
        points = position_evaluation(trial_board, trial_history)

        if turn == "w":
            if best_move is None or points > best_move[0]:
                best_move = (points, pos1, pos2)
        else:
            if best_move is None or points < best_move[0]:
                best_move = (points, pos1, pos2)

    return best_move