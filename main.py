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
from npc import Npc
from portal import portals
pygame.init()

# funzione per caricare tutti gli assets
assets.load_assets()

# schermo
finestra = pygame.display.set_mode((LUNGHEZZA, ALTEZZA))
pygame.display.set_caption("Rock A' Raso")

# istanze
mondo = Mondo(1, finestra, livelli)
player = Giocatore(0, 0, mondo, finestra, None)
nemico = Enemy(3, 4, mondo, finestra, player)
player.enemy = nemico
npc = Npc(8, 8, mondo, finestra)
portale = portals(8, 0, mondo, finestra)
hud = HUD(finestra, player, npc)

clock = pygame.time.Clock()

# loop musica
mixer.music.play(loops=-1)

# loop di gioco
run = True
while run:
    mondo.disegna()
    player.controlla_fontanella()
    player.update()
    if mondo.livello_id == 1:
        if nemico.vita > 0:
            nemico.update()
        npc.update()
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
    