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

# Inizializza la musica di background
canzone = 'assets/audio/soundtrack.mp3'
mixer.music.load(canzone)
mixer.music.set_volume(0.2)
mixer.music.play(-1)

# Carica gli assets (immagini, suoni, dati di livello, ecc.)
assets.load_assets()

# Imposta alcuni riferimenti alle immagini caricate
img1 = assets.NPC_IMAGES[1]
bat_img = assets.ENEMY_FRAMES["down"][0]
boss_img = assets.BOSS_FRAMES["down"][0]

# Crea la finestra di gioco
finestra = pygame.display.set_mode((LUNGHEZZA, ALTEZZA))
pygame.display.set_caption("Nemici Miei | Rock A' Raso")

# Crea le istanze per il menu, la schermata di vittoria e il Try Again (riprova)
menu = Menu(finestra)
win = Win(finestra)
riprova = Try(finestra)

# Loop principale del gioco
run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False

    # Se il menu è attivo, gestiscilo e disegnalo
    if menu.show_menu:
        menu.handle_events(events)
        menu.draw()
    else:
        # Inizializza il mondo e il giocatore dopo la chiusura del menu
        if 'mondo' not in locals():
            # Crea il mondo di gioco usando i dati di livello caricati
            mondo = Mondo(1, finestra, assets.livelli)
            # Crea il giocatore
            player = Giocatore(0, 0, mondo, finestra, None, None)
            # Crea un numero casuale di nemici "bat"
            n_bat = random.randint(3, 5)
            bats = [Enemy(random.randint(0, mondo.num_righe - 1),
                          random.randint(0, mondo.num_colonne - 1),
                          mondo, finestra, player, bat_img, 50, 2500, 2, 10)
                    for _ in range(n_bat)]
            # Assegna la lista di nemici al giocatore
            player.enemy = bats
            # Crea un NPC
            npc = Npc(8, 8, mondo, finestra, img1)
            # Crea un portale
            portale = portals(8, 0, mondo, finestra)
            # Crea il boss
            bosses = [Boss(0, 0, mondo, finestra, player, boss_img, 20, 200)]
            # Crea l'HUD passando i riferimenti necessari
            hud = HUD(finestra, player, npc, bosses[0], mondo)
            player.hud = hud

        # Disegna il mondo di gioco
        mondo.disegna()
        # Controlla eventuali interazioni del giocatore (ad es. con una fontanella)
        player.controlla_fontanella()

        if player.vita > 0:
            player.update()
        else:
            riprova.handle_events(events)
            riprova.draw()  # Disegna la schermata "Try Again"
            # Controlla se il pulsante "Riprova" è stato premuto
            if riprova.restart_requested:
                mondo.start(1, finestra, assets.livelli)
                player.start(0, 0, mondo, finestra, None, None)
                hud.start(finestra, player, npc, bosses[0], mondo)
                bosses = [Boss(0, 0, mondo, finestra, player, boss_img, 20, 200)]
                n_bat = random.randint(3, 5)
                bats = [Enemy(random.randint(0, mondo.num_righe - 1),
                          random.randint(0, mondo.num_colonne - 1),
                          mondo, finestra, player, bat_img, 50, 2500, 2, 10)
                    for _ in range(n_bat)]
                livello_id = 1
                hud.start(finestra, player, npc, bosses[0], mondo)
                riprova.restart_requested = False

        # Se siamo al livello 1, aggiorna i nemici, l'NPC e il portale
        if mondo.livello_id == 1:
            canzone = 'assets/audio/soundtrack.mp3'
            for bat in bats:
                if bat.hp > 0:
                    bat.update()
            npc.update()
            portale.update()
            player.enemy = bats

        # Se siamo al livello 2, aggiorna il boss e cambia la musica se necessario
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
            # Imposta i nemici del giocatore al boss
            player.enemy = bosses
        # Disegna l'HUD (ad es. la barra della vita)
        hud.draw(events)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
