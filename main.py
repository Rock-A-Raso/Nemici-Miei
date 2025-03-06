import pygame
import random
from pygame import mixer
from settings import LUNGHEZZA, ALTEZZA, FPS
import assets
from world import Mondo
from player import Giocatore
from hud import HUD
from enemy import Enemy
from boss import Boss
from npc import Npc
from portal import portals
from effect import blood_effect
from menu import Menu

pygame.init()
clock = pygame.time.Clock()

# musica
canzone = 'assets/audio/soundtrack.mp3'
mixer.music.load(canzone)
mixer.music.set_volume(1)
mixer.music.play(-1)
# assets
assets.load_assets()
img1 = assets.NPC_IMAGES[1]
img2 = assets.NPC_IMAGES[1]
bat_img = assets.ENEMY_FRAMES["down"][0]
boss_img = assets.BOSS_FRAMES["down"][0]

# schermo
finestra = pygame.display.set_mode((LUNGHEZZA, ALTEZZA))
pygame.display.set_caption("Nemici Miei | Rock A' Raso")

# Menu
menu = Menu(finestra)

# Loop principale
run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
    
    if menu.show_menu:
        menu.handle_events(events)
        menu.draw()
    else:
        # inizializza il mondo e il giocatore solo dopo che il menu è chiuso
        if 'mondo' not in locals():
            mondo = Mondo(1, finestra, assets.livelli)
            player = Giocatore(0, 0, mondo, finestra, None, None)
            n_bat = random.randint(3, 5)
            bats = [Enemy(random.randint(0, mondo.num_righe - 1),
                          random.randint(0, mondo.num_colonne - 1),
                          mondo, finestra, player, bat_img, 50, 2500, 2, 7.) 
                    for _ in range(n_bat)]
            player.enemy = bats
            npc = Npc(8, 8, mondo, finestra, img1)
            portale = portals(8, 0, mondo, finestra)
            bosses = [Boss(0, 0, mondo, finestra, player, boss_img, 15, 200)]
            hud = HUD(finestra, player, npc, bosses[0], mondo)
            player.hud = hud
        
        mondo.disegna()
        player.controlla_fontanella()
        
        if player.vita > 0:
            player.update()
        
        if mondo.livello_id == 1:
            canzone = 'assets/audio/soundtrack.mp3'
            for bat in bats:
                bat.update()
            npc.update()
            portale.update()
        
        if mondo.livello_id == 2:
            nuova_canzone = 'assets/audio/boss_soundtrack.mp3'
            if nuova_canzone != canzone:
                mixer.music.stop()
                mixer.music.load(nuova_canzone)
                mixer.music.play(loops=-1)
                canzone = nuova_canzone
            portale.update()
            for boss in bosses:
                boss.update()
            player.enemy = bosses
        
        hud.draw(events)
        
        bats = [bat for bat in bats if bat.hp > 0]
        bosses = [boss for boss in bosses if boss.hp > 0]
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
