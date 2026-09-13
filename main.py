import pygame
import board
import engine
import os

pygame.init()
gs = board.GameState()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True
turn = "w"
player = "w"
started = False
checkmate = False
promotion = False
pinned = None
attackers = None


assets = os.listdir("assets")

images = {}

selected = False
coordinates = []
coordinate = (-1, -1)

for file in assets:
    piece = file.strip(".png")
    images[piece] = pygame.image.load(f"assets/{file}").convert_alpha()
    images[piece] = pygame.transform.scale(images[piece], (100, 100))

circle_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
pygame.draw.circle(circle_surface, (127, 127, 127, 180), (50, 50), 20)  

game_font = pygame.font.Font(None, 50)
select_surface = game_font.render("Choose your side :",True, (255, 255, 255))

while running:
    for event in pygame.event.get():

        #Close game button
        if event.type == pygame.QUIT:
            running = False

        #Selection screen options
        if not started:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if 455 <= x <= 495 and 95 <= y <= 135:
                    player = "b"
                    turn = "w"
                    started = True
                    checkmate = False
                    gs = board.GameState()

                elif 530 <= x <= 570 and 95 <= y <= 135:
                    player = "w"
                    turn = "w"
                    started = True
                    checkmate = False
                    gs = board.GameState()
            continue

        #bot moves
        if turn != player:
            bot_move = engine.bot_logic(gs.board, gs.move_history, turn)
            gs.board, gs.move_history = board.move(bot_move[1][0], bot_move[1][1], bot_move[2][0], bot_move[2][1], gs.board, gs.move_history)

            if bot_move[2][0] == 7 or bot_move[2][0] == 0:
                if "P" in gs.board[bot_move[2][0]][bot_move[2][1]]:
                    gs.board[bot_move[2][0]][bot_move[2][1]] = turn + "Q"

            if turn == "w":
                turn = "b"
            else: 
                turn = "w"

            checkmate = board.is_checkmate(gs.board, gs.move_history, turn)
            if checkmate:
                started = False

        #Piece selection detection
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            x = (x - 560)/100 #board x coordinate
            y = (y - 140)/100 #board y coordinate

            if 0 > x or 0 > y:
                x = -1
                y = -1
            else:
                x = int(x)
                y = int(y)
            
            if 0 <= x <= 7 and 0 <= y <= 7:

                if selected and (y, x) in coordinates:
                    y1, x1 = coordinate
                    gs.board, gs.move_history = board.move(y1, x1, y, x, gs.board, gs.move_history)
                    selected = False
                    attackers = None
                    pinned = None
                    coordinates = []
                    coordinate = (-1, -1)

                    if y == 7 or y == 0:
                        if "P" in gs.board[y][x]:
                            gs.board[y][x] = turn + "Q"
                            
                    if turn == "w":
                        turn = "b"
                    else: 
                        turn = "w"

                    checkmate = board.is_checkmate(gs.board, gs.move_history, turn)
                    if checkmate:
                        started = False
                
                elif turn in gs.board[y][x]:
                    #Calls on move logic and highlights the selected piece, puts dots on valid squares and captures
                    coordinates, pinned, attackers = board.logic_coordinators(y, x, gs.board, gs.move_history, turn, pinned, attackers)
                    selected = True
                    coordinate = (y, x)
                else:
                    coordinates = []
                    selected = False
                    coordinate = (-1, -1)
            else:
                coordinates = []
                selected = False
                    
    screen.fill("Black")

    pygame.draw.rect(screen, (255, 0, 0), (510, 90, 900, 900))
    pygame.draw.rect(screen, (16, 11, 0), (550, 130, 820, 820))

    pixel_x = 560
    pixel_y = 140
    color = None

    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            if (row + col) % 2:
                color = (59, 52, 31)
            else:
                color = (255, 239, 200)
            
            pygame.draw.rect(screen, color, (pixel_x, pixel_y, 100, 100))

            if gs.board[row][col] != "--":
                screen.blit(images[gs.board[row][col]], (pixel_x, pixel_y))
            pixel_x += 100    
        
        pixel_y += 100
        pixel_x = 560

    if selected:
        for y, x in coordinates:
            y = y * 100 + 140
            x = x * 100 + 560
            screen.blit(circle_surface, (x, y))

    if not started:
        pygame.draw.rect(screen, (0, 0, 0), (510, 90, 900, 900))
        screen.blit(select_surface, (100, 100))
        pygame.draw.rect(screen, (255, 0, 0), (450, 90, 50, 50))
        pygame.draw.rect(screen, (0, 0, 0), (455, 95, 40, 40))
        pygame.draw.rect(screen, (255, 0, 0), (525, 90, 50, 50))
        pygame.draw.rect(screen, (255, 255, 255), (530, 95, 40, 40))     
    
    pygame.display.flip()

    clock.tick(60)

pygame.quit()