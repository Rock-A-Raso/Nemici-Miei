import pygame
import random
import assets
from pygame import mixer
from settings import LUNGHEZZA, ALTEZZA, FPS
from world import Mondo
from player import Giocatore
from hud import HUD
from enemy import Enemy
from boss import Boss
from npc import Npc
from portal import portals
from menu import Menu
from win import Win
from riprova import Try

pygame.init()
clock = pygame.time.Clock()

# musica di background
canzone = 'assets/audio/soundtrack.mp3'
mixer.music.load(canzone)
mixer.music.set_volume(0.2)
mixer.music.play(-1)

# carica gli assets 
assets.load_assets()

img1 = assets.NPC_IMAGES[1]
bat_img = assets.ENEMY_FRAMES["down"][0]
boss_img = assets.BOSS_FRAMES["down"][0]

# finestra di gioco
finestra = pygame.display.set_mode((LUNGHEZZA, ALTEZZA))
pygame.display.set_caption("Nemici Miei | Rock A' Raso")

# istanze
menu = Menu(finestra)
win = Win(finestra)
riprova = Try(finestra)

# loop principale del gioco
run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False

    # menu è attivo
    if menu.show_menu:
        menu.handle_events(events)
        menu.draw()
    else:
        # inizializza dopo la chiusura del menu
        if 'mondo' not in locals():
            mondo = Mondo(1, finestra, assets.livelli)
            player = Giocatore(0, 0, mondo, finestra, None, None)
            n_bat = random.randint(3, 5)
            bats = [Enemy(random.randint(0, mondo.num_righe - 1),
                          random.randint(0, mondo.num_colonne - 1),
                          mondo, finestra, player, bat_img, 50, 2500, 2, 10)
                    for _ in range(n_bat)]
            player.enemy = bats
            npc = Npc(8, 8, mondo, finestra, img1)
            portale = portals(8, 0, mondo, finestra)
            bosses = [Boss(0, 0, mondo, finestra, player, boss_img, 10, 150)]
            hud = HUD(finestra, player, npc, bosses[0], mondo)
            player.hud = hud

        mondo.disegna()
        player.controlla_fontanella()

        # controlla se il giocatore è vivo
        if player.vita > 0:
            player.update()
        else:
            # try again
            riprova.handle_events(events)
            riprova.draw()  
            if riprova.restart_requested:
                # restarta tutto
                mondo.start(1, finestra, assets.livelli)
                player.start(0, 0, mondo, finestra, None, None)
                hud.start(finestra, player, npc, bosses[0], mondo)
                bosses = [Boss(0, 0, mondo, finestra, player, boss_img, 10, 150)]
                n_bat = random.randint(3, 5)
                bats = [Enemy(random.randint(0, mondo.num_righe - 1),
                          random.randint(0, mondo.num_colonne - 1),
                          mondo, finestra, player, bat_img, 50, 2500, 2, 10)
                    for _ in range(n_bat)]
                livello_id = 1
                hud.start(finestra, player, npc, bosses[0], mondo)
                player.hud = hud
                riprova.restart_requested = False

        # livello 1
        if mondo.livello_id == 1:
            canzone = 'assets/audio/soundtrack.mp3'
            for bat in bats:
                if bat.hp > 0:
                    bat.update()
            npc.update()
            portale.update()
            player.enemy = bats

        # livello 2
        if mondo.livello_id == 2:
            nuova_canzone = 'assets/audio/boss_soundtrack.mp3'
            if nuova_canzone != canzone:
                mixer.music.stop()
                mixer.music.load(nuova_canzone)
                mixer.music.set_volume(1)
                mixer.music.play(loops=-1)
                canzone = nuova_canzone
            portale.update()
            for boss in bosses:
                if boss.hp > 0:
                    boss.update()
                else:
                    win.update()
            player.enemy = bosses
        hud.draw(events)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
