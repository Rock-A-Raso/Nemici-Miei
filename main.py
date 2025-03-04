import pygame
from pygame.locals import QUIT
from pygame import mixer
from settings import LUNGHEZZA, ALTEZZA, FPS
import assets
from world import Mondo
from player import Giocatore
from hud import HUD
from enemy import Enemy
from assets import livelli
from npc import NPC
from portal import portals

pygame.init()
finestra = pygame.display.set_mode((LUNGHEZZA, ALTEZZA))
pygame.display.set_caption("Rock A' Raso")
assets.load_assets()
mondo = Mondo(1, finestra, livelli)
player = Giocatore(0, 0, mondo, finestra)
nemico = Enemy(3, 4, mondo, finestra, player)
NPCS = NPC(8, 8, mondo, finestra)
portale = portals(9, 0.010, mondo, finestra)
hud = HUD(finestra, player)
clock = pygame.time.Clock()
mixer.music.play(loops=-1)
run = True
while run:
    finestra.fill((0, 0, 0))
    mondo.disegna()
    player.controlla_fontanella()
    player.update()
    if mondo.livello_id == 1:
        nemico.update()
        NPCS.update()
        portale.update()
    hud.draw()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
    if player.vita <= 0:
        run = False
    clock.tick(FPS)
pygame.quit()
    