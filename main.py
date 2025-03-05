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

clock = pygame.time.Clock()

# funzione per caricare tutti gli assets
assets.load_assets()
img1 = pygame.image.load('assets/[NPC]/1.png')
img2 = pygame.image.load('assets/[NPC]/1.png')

# schermo
finestra = pygame.display.set_mode((LUNGHEZZA, ALTEZZA))
pygame.display.set_caption("Nemici Miei | Rock A' Raso")

# istanze
mondo = Mondo(1, finestra, livelli)
player = Giocatore(0, 0, mondo, finestra, None, None)
nemico = Enemy(3, 4, mondo, finestra, player)
player.enemy = nemico
npc = Npc(8, 8, mondo, finestra, img1)
npc2 = Npc(0, 2, mondo, finestra, img2)
portale = portals(8, 0, mondo, finestra)
hud = HUD(finestra, player, npc)
player.hud = hud

# loop musica
mixer.music.play(loops=-1)

# loop principale
run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            run = False

    mondo.disegna()
    player.controlla_fontanella()
    if player.vita > 0:
        player.update()
    if mondo.livello_id == 1:
        if nemico.vita > 0:
            nemico.update()
        npc.update()
        portale.update()
    if mondo.livello_id == 2:
         portale.update()
         npc2.update()

    hud.draw(events)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()