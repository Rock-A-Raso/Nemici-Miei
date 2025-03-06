import pygame
import random
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

# assets
assets.load_assets()
img1 = assets.NPC_IMAGES[1]
img2 = assets.NPC_IMAGES[1]
bat_img = assets.ENEMY_FRAMES["down"][0]

# schermo
finestra = pygame.display.set_mode((LUNGHEZZA, ALTEZZA))
pygame.display.set_caption("Nemici Miei | Rock A' Raso")

# istanze
mondo = Mondo(1, finestra, livelli)
player = Giocatore(0, 0, mondo, finestra, None, None)
# pipistrelli random
n_bat = random.randint(3, 5)
bats = []
for _ in range(n_bat):
    x = random.randint(0, mondo.num_righe - 1)  
    y = random.randint(0, mondo.num_colonne - 1)
    bats.append(Enemy(x, y, mondo, finestra, player, bat_img, 50, 1000, 2, 10))
player.enemy = bats
npc = Npc(8, 8, mondo, finestra, img1)
npc2 = Npc(0, 2, mondo, finestra, img2)
portale = portals(8, 0, mondo, finestra)
hud = HUD(finestra, player, npc)
player.hud = hud

# musica
mixer.music.play(loops=-1)

# loop principale
run = True
while run:
    events = pygame.event.get()  
    for event in events:
        if event.type == pygame.QUIT:
            run = False  
    
    mondo.disegna()
    player.controlla_fontanella()
    
    if player.vita > 0:
        player.update()

    if mondo.livello_id == 1:
        for bat in bats:
            bat.update()
        npc.update()
        portale.update()

    if mondo.livello_id == 2:
        portale.update()
        npc2.update()
        

    hud.draw(events)

    for bat in bats.copy():
        if bat.hp <= 0:
            bats.remove(bat)
            
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
