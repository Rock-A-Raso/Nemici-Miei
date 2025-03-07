import pygame
import random
import assets
from npc import Npc
from enemy import Enemy
from settings import GRANDEZZA_TILES

class Giocatore:
    def __init__(self, tile_x, tile_y, mondo, finestra, nemici, hud):
        self.start(tile_x, tile_y, mondo, finestra, nemici, hud)
    
    def start(self, tile_x, tile_y, mondo, finestra, nemici, hud):
        self.mondo = mondo
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.finestra = finestra
        self.nemici = nemici
        self.hud = hud

        img = assets.PLAYER_FRAMES["down"][0]
        self.image = pygame.transform.scale(img, (GRANDEZZA_TILES // 2, GRANDEZZA_TILES // 2))

        # converte le coordinate del tile in coordinate pixel sullo schermo
        sx, sy = self.mondo.tile_to_screen(tile_x, tile_y)

        # calcola il centro del tile per posizionare correttamente il giocatore
        center = (sx + GRANDEZZA_TILES // 2, sy + GRANDEZZA_TILES // 2)
        # rettangolo dell'immagine
        self.rect = self.image.get_rect(center=center)
        # imposta la destinazione iniziale pari a quella attuale
        self.dest_x, self.dest_y = self.rect.topleft

        self.velocita = 4
        self.in_movimento = False

        self.fountain_x, self.fountain_y = self.mondo.trova_fontanella()
        self.thirsty = True
        self.direction = "down"
        self.frame_index = 0
        self.frame_counter = 0

        self.ugo_vita_counter = 0

        # statistiche del giocatore
        self.vita = 100           # Salute 
        self.vita_max = 100       # Salute massima
        self.monete = 0           # Numero di monete raccolte
        self.level = 1            # Livello 
        self.last_attack_time = 0 # Tempo dell'ultimo attacco 
        self.attack_cooldown = 1000  # Cooldown dell'attacco 
        self.attaccato = False    # Flag per indicare se il giocatore è stato danneggiato 
        self.attaccato_timer = 0  # Timer per la durata dell'effetto "attaccato"

    def update(self):
        # se il giocatore non ha raggiunto la destinazione, muovilo gradualmente
        if self.rect.topleft != (self.dest_x, self.dest_y):
            # calcola la differenza tra la posizione attuale e la destinazione
            dx = self.dest_x - self.rect.x
            dy = self.dest_y - self.rect.y
            # movimento orizzontale
            if dx:
                self.rect.x += self.velocita if dx > 0 else -self.velocita
                if abs(dx) < self.velocita:
                    self.rect.x = self.dest_x
            # movimento verticale
            if dy:
                self.rect.y += self.velocita if dy > 0 else -self.velocita
                if abs(dy) < self.velocita:
                    self.rect.y = self.dest_y
            # aggiorna l'animazione
            self.animate()
        else:
            # se il giocatore ha raggiunto la destinazione, non è in movimento
            self.in_movimento = False

            # gestione degli input
            keys = pygame.key.get_pressed()
            new_tx, new_ty = self.tile_x, self.tile_y
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                new_tx -= 1
                self.direction = "left"
                self.in_movimento = True
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                new_tx += 1
                self.direction = "right"
                self.in_movimento = True
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                new_ty -= 1
                self.direction = "up"
                self.in_movimento = True
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                new_ty += 1
                self.direction = "down"
                self.in_movimento = True
            
            # verifica se il nuovo tile è attraversabile
            if self.mondo.is_tile_walkable(new_tx, new_ty):
                # aggiorna la posizione del giocatore
                self.tile_x, self.tile_y = new_tx, new_ty
                # converte la nuova posizione in coordinate pixel
                sx, sy = self.mondo.tile_to_screen(new_tx, new_ty)
                bottom_center = (sx + GRANDEZZA_TILES // 2, sy + GRANDEZZA_TILES // 2)
                # imposta la nuova destinazione in base al centro 
                self.dest_x = bottom_center[0] - self.rect.width // 2
                self.dest_y = bottom_center[1] - self.rect.height

                # riproduce suoni e imposta la velocità in base al tipo di terreno:
                if self.in_movimento and self.mondo.matrice[self.tile_y][self.tile_x] in [3, 4]:
                    assets.sounds["grass"].play(maxtime=300, fade_ms=50)
                    self.velocita = 4
                if self.in_movimento and self.mondo.matrice[self.tile_y][self.tile_x] in [7, 8]:
                    assets.sounds["acqua"].play(maxtime=300, fade_ms=50)
                    self.velocita = 2
                if self.in_movimento and self.mondo.matrice[self.tile_y][self.tile_x] in [11, 12]:
                    assets.sounds["stone"].play(maxtime=300, fade_ms=50)
                    self.velocita = 4

            # esegue l'animazione idle
            if not self.in_movimento:
                self.idle()
            else:
                # aggiorna l'immagine corrente in base alla direzione e al frame
                self.image = assets.PLAYER_FRAMES[self.direction][self.frame_index]

        # se il valore del tile è 20 e il giocatore non ha sete, cambia livello
        if self.mondo.matrice[self.tile_y][self.tile_x] == 20 and not self.thirsty:
            self.mondo.nuovo_livello(2)
            self.level += 1
            
        # aggiorna l'immagine del giocatore in base alla direzione e all'animazione corrente
        self.image = assets.PLAYER_FRAMES[self.direction][self.frame_index]

        draw_rect = self.rect.copy()
        draw_rect.y -= 15

        # incrementa la vita parlando con ugo
        if self.hud is not None and self.hud.dialogue_index == 2 and self.ugo_vita_counter < 1 and self.vita < 100:
            self.vita += 15
            self.ugo_vita_counter += 1


        if self.vita > 100:
            self.vita = 100

        self.attacca()

        self.finestra.blit(self.image, draw_rect)

        # disegna un rettangolo rosso quando viene attaccato
        if self.attaccato:
            self.attaccato_timer += 1
            if self.attaccato_timer > 15:
                self.attaccato = False
                self.attaccato_timer = 0
            else:
                overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
                overlay.fill((255, 0, 0, 75))
                self.finestra.blit(overlay, draw_rect.topleft)

    def animate(self):
        if not self.in_movimento:
            self.frame_index = 0
            return
        else:
            self.frame_counter += 1
        if self.frame_counter >= 10:
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(assets.PLAYER_FRAMES[self.direction])
        self.image = assets.PLAYER_FRAMES[self.direction][self.frame_index]

    def idle(self):
        # posizione down di default
        if self.direction not in assets.PLAYER_IDLE:
            self.direction = "down"
        if self.frame_index >= len(assets.PLAYER_IDLE[self.direction]):
            self.frame_index = 0
        self.frame_counter += 1
        if self.frame_counter >= 30:
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(assets.PLAYER_IDLE[self.direction])
        self.image = assets.PLAYER_IDLE[self.direction][self.frame_index]
    
    # controlla se il giocatore è vicino alla fontanella
    def is_near_fountain(self):
        adjacent = [
            (self.fountain_x, self.fountain_y - 2),
            (self.fountain_x, self.fountain_y + 1),
            (self.fountain_x - 2, self.fountain_y),
            (self.fountain_x + 1, self.fountain_y),
            (self.fountain_x - 1, self.fountain_y - 2),
            (self.fountain_x - 1, self.fountain_y + 1),
            (self.fountain_x - 2, self.fountain_y - 1),
            (self.fountain_x + 1, self.fountain_y - 1)
        ]
        return (self.tile_x, self.tile_y) in adjacent

    # controlla l' interazione del giocatore con la fontanella
    def controlla_fontanella(self):
        keys = pygame.key.get_pressed()
        if self.is_near_fountain() and self.thirsty and keys[pygame.K_e] and self.hud.giaparlato:
            self.monete += 1
            self.thirsty = False
            assets.sounds["coin"].play()

    # prende danno
    def take_damage(self, amount):
        self.vita -= amount
        assets.sounds["player_dmg"].play(maxtime=300, fade_ms=50)
        if self.vita < 0:
            self.vita = 0
        self.attaccato = True

    # controlla se il giocatore è vicino a un nemico
    def is_near_npc(self, npc):
        adjacent_npc = [
            (npc.tile_x, npc.tile_y + 1),
            (npc.tile_x + 1, npc.tile_y),
            (npc.tile_x - 1, npc.tile_y + 1),
            (npc.tile_x + 1, npc.tile_y - 1)
        ]
        return (self.tile_x, self.tile_y) in adjacent_npc
    
    # attacca i nemici vicini
    def attacca(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown and pygame.mouse.get_pressed()[0]:
            for enemy in self.enemy:
                if abs(self.tile_x - enemy.tile_x) <= 1 and abs(self.tile_y - enemy.tile_y) <= 1:
                    enemy.take_damage(20)
                    assets.sounds["attack"].play()
            self.last_attack_time = current_time
