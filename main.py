import pygame
from pygame.locals import QUIT
from pygame import mixer
from settings import LUNGHEZZA, ALTEZZA, FPS
import assets
from world import Mondo
from player import Giocatore
from hud import HUD  # Import della HUD

pygame.init()

# Crea la finestra di gioco
finestra = pygame.display.set_mode((LUNGHEZZA, ALTEZZA))
pygame.display.set_caption("Rock A' Raso")

# Carica gli asset (ricorda di aver già chiamato pygame.init())
assets.load_assets()

# Definisci la matrice della mappa
matrice = [
    [3, 7, 7, 7, 7, 7, 7, 3, 3, 3],
    [4, 8, 8, 8, 8, 8, 8, 3, 3, 3],
    [3, 3, 8, 8, 8, 8, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 19, 19, 4, 3, 3, 3],
    [3, 3, 4, 3, 19, 18, 4, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 4, 3, 3, 3, 4, 3],
    [3, 3, 3, 4, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]

# Crea il mondo e il giocatore
mondo = Mondo(matrice, finestra)
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
