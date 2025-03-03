import pygame
from pygame.locals import QUIT
from pygame import mixer
from settings import LUNGHEZZA, ALTEZZA, FPS
import assets
from world import Mondo
from player import Giocatore
from hud import HUD
from livelli import livelli
from enemy import Enemy

pygame.init()
finestra = pygame.display.set_mode((LUNGHEZZA, ALTEZZA))
pygame.display.set_caption("Rock A' Raso")

assets.load_assets()

tile_x = 0
tile_y = 0
tile_x_enemy = 8
tile_y_enemy = 8
mondo = Mondo(1, finestra, livelli)
player = Giocatore(tile_x, tile_y, mondo, finestra)
nemico = Enemy(tile_x_enemy, tile_y_enemy, mondo, finestra, player)
hud = HUD(finestra, player)

clock = pygame.time.Clock()
mixer.music.play(loops=-1)

run = True
while run:
    finestra.fill((0, 0, 0))
    mondo.disegna()
    player.controlla_fontanella()
    player.update()
    nemico.update() 
    hud.draw()  
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    clock.tick(FPS)

pygame.quit()