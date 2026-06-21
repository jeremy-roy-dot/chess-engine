import pygame
import board
import os

pygame.init()
gs = board.GameState()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True

assets = os.listdir("assets")

images = {}

for file in assets:
    piece = file.strip(".png")
    images[piece] = pygame.image.load(f"assets/{file}").convert_alpha()
    images[piece] = pygame.transform.scale(images[piece], (100, 100))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            coordinates = event.pos
            x, y = coordinates
            x = int(((x - 560)/100)) #board x coordinate
            y = int((y - 140)/100) #board y coordinate
            print(y, x)

            if gs[y][x] != "--":
                selected = True
                board.highlight(y, x)

    screen.fill("Black")

    pygame.draw.rect(screen, (133, 203, 51), (510, 90, 900, 900))
    pygame.draw.rect(screen, (16, 11, 0), (550, 130, 820, 820))

    pixel_x = 560
    pixel_y = 140
    color = None

    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            if (row + col) % 2:
                color = (239, 255, 200)
            else:
                color = (59, 52, 31)
            
            pygame.draw.rect(screen, color, (pixel_x, pixel_y, 100, 100))

            if gs.board[row][col] != "--":
                screen.blit(images[gs.board[row][col]], (pixel_x, pixel_y))
            pixel_x += 100    
        
        pixel_y += 100
        pixel_x = 560

    pygame.display.flip()

    clock.tick(60)

pygame.quit()