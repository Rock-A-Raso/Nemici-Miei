import pygame
from pygame.locals import QUIT
from pygame import mixer
from settings import LUNGHEZZA, ALTEZZA, FPS
import assets
from world import Mondo
from player import Giocatore
from hud import HUD
from livelli import livelli

pygame.init()
# Crea la finestra di gioco
finestra = pygame.display.set_mode((LUNGHEZZA, ALTEZZA))
pygame.display.set_caption("Rock A' Raso")

# Loading degli assets
assets.load_assets()

# Crea il mondo, il giocatore e la HUD
mondo = Mondo(1, finestra, livelli)
player = Giocatore(0, 0, mondo, finestra)
hud = HUD(finestra, player)  # Creazione della HUD

clock = pygame.time.Clock()
mixer.music.play(loops=-1)

run = True
while run:
    finestra.fill((0, 0, 0))
    mondo.disegna()
    player.controlla_fontanella()
    player.update()
    hud.draw()  # Disegna la HUD sopra il resto
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
    clock.tick(FPS)

pygame.quit()
