import board

def position_evaluation(board_state, move_history): #evaluates with the system and returns an int between roughly -30000 and 30000 where -30000 to -1 is a black advantage, 0 is perfectly equal, and 1 to 30000 is a white advantage
    points = 0
    side = 0
    wKy, wKx = (-1, -1)
    bKy, bKx = (-1, -1)

    for row in board_state:
        for column in board_state[row]:
            piece = board_state[row][column]

            #determines how to multiply the points
            if "b" in piece:
                side = -1
            else:
                side = 1

            #Raw points for the pieces
            if "P" in piece:
                points += 100 * side
                #if board_state[row][column was making pawn connection checker
            elif ("B" or "N") in piece:
                points += 300 * side
            elif "R" in piece:
                points += 500 * side
            elif "Q" in piece:
                points += 900 * side
            else:
                #stores the king position for later
                if side == -1:
                    bKy, bKx = (row, column)

                    #Checks if the king is in a corner
                    if column >= 6 or column <= 1:
                        if row == 0:
                            points += 100 * side
                else:
                    wKy, wKx = (row, column)

                    #Checks if the king is in a corner
                    if column >= 6 or column <= 1:
                        if row == 0:
                            points += 100 * side

                #Checks if the king has protection
                king_moves = board.king_pseudo_move(row, column, board_state)
                if len(king_moves) < 2:
                    points -= 100 * side
                elif 2 <= len(king_moves) <= 3:
                    points += 100 * side
                else:
                    points -= 100 * side
                    
            legal_moves = board.logic_coordinators(row, column, board_state, move_history, turn = "b" if side == -1 else "w")

            #Adds points for each possible moves, if the move is in the center of the board you get more
            for x, y in legal_moves:
                if not 2 <= x <= 5:
                    if side == -1:
                        if not 0 <= y <= 5:
                            points += 20 * side
                    else:
                        if not 2 <= y <= 7:
                            points += 20 * side
                    points += 15 * side
                points += 10 * side
            
            
    return points