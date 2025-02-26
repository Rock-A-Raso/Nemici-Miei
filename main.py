import pygame
from pygame.locals import * 
from engine.game_loop import Game

pygame.init()

# costanti schermo
SCREEN_WIDTH = 0
SCREEN_LENGTH = 0
FPS = 60
DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH))
pygame.display.set_caption("Rock A' Raso")

# istanza di gioco
game = Game(DISPLAY)

run = True
clock = pygame.time.Clock()

# loop di gioco
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT():
            run = False
            pygame.quit()
    
    # funzioni
    game.update()
    game.render()

    clock.tick(FPS)

pygame.quit()