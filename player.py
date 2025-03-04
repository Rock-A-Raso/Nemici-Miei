import pygame
import random
import assets
from npc import Npc
from enemy import Enemy
from settings import GRANDEZZA_TILES

class Giocatore:
    def __init__(self, tile_x, tile_y, mondo, finestra, nemico):
        self.mondo = mondo
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.finestra = finestra
        self.enemy = nemico
        img = pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[DOWN]/walkd1.png')
        self.image = pygame.transform.scale(img, (GRANDEZZA_TILES // 2, GRANDEZZA_TILES // 2))
        sx, sy = self.mondo.tile_to_screen(tile_x, tile_y)
        center = (sx + GRANDEZZA_TILES // 2, sy + GRANDEZZA_TILES // 2)
        self.rect = self.image.get_rect(center=center)
        self.dest_x, self.dest_y = self.rect.topleft
        self.rect = self.image.get_rect(midbottom=center)
        self.dest_x, self.dest_y = self.rect.topleft
        self.velocita = 4
        self.in_movimento = False
        self.fountain_x, self.fountain_y = self.mondo.trova_fontanella()
        self.thirsty = True
        self.direction = "down"
        self.frame_index = 0
        self.frame_counter = 0
        self.vita = 100
        self.vita_max = 100
        self.monete = 0
        self.level = 1
        self.exp = 0
        self.next_level_exp = 100
        self.last_attack_time = 0
        self.attack_cooldown = 500

    def update(self):
        # Se il player non ha ancora raggiunto la destinazione, muovi il rettangolo
        if self.rect.topleft != (self.dest_x, self.dest_y):
            dx = self.dest_x - self.rect.x
            dy = self.dest_y - self.rect.y
            if dx:
                self.rect.x += self.velocita if dx > 0 else -self.velocita
                if abs(dx) < self.velocita:
                    self.rect.x = self.dest_x
            if dy:
                self.rect.y += self.velocita if dy > 0 else -self.velocita
                if abs(dy) < self.velocita:
                    self.rect.y = self.dest_y
            self.animate()
        else:
            # Gestisci l'input per cambiare tile
            self.in_movimento = False
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

            if self.mondo.is_tile_walkable(new_tx, new_ty):
                self.tile_x, self.tile_y = new_tx, new_ty
                sx, sy = self.mondo.tile_to_screen(new_tx, new_ty)
                bottom_center = (sx + GRANDEZZA_TILES // 2, sy + GRANDEZZA_TILES // 2)
                self.dest_x = bottom_center[0] - self.rect.width // 2
                self.dest_y = bottom_center[1] - self.rect.height
                if self.in_movimento:
                    random.choice(assets.grass_sounds).play(maxtime=300, fade_ms=50)
            if not self.in_movimento:
                self.idle()
            else:
                self.image = assets.PLAYER_FRAMES[self.direction][self.frame_index]

        # Gestione cambio livello, attacco e disegno
        if self.mondo.matrice[self.tile_y][self.tile_x] == 20 and not self.thirsty:
            self.mondo.nuovo_livello(2)
            self.level += 1

        self.image = assets.PLAYER_FRAMES[self.direction][self.frame_index]
        offset = 15
        draw_rect = self.rect.copy()
        draw_rect.y -= offset

        self.attacca()

        self.finestra.blit(self.image, draw_rect)


    def animate(self):
        if not self.in_movimento:
            self.frame_index = 0
            return
        self.frame_counter += 1
        if self.frame_counter >= 10:
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(assets.PLAYER_FRAMES[self.direction])
        self.image = assets.PLAYER_FRAMES[self.direction][self.frame_index]

    def idle(self):
        if self.direction not in assets.PLAYER_IDLE:
            self.direction = "down"
        if self.frame_index >= len(assets.PLAYER_IDLE[self.direction]):
            self.frame_index = 0
        self.frame_counter += 1
        if self.frame_counter >= 30:
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(assets.PLAYER_IDLE[self.direction])
        self.image = assets.PLAYER_IDLE[self.direction][self.frame_index]

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

    def controlla_fontanella(self):
        keys = pygame.key.get_pressed()
        if self.is_near_fountain() and self.thirsty and keys[pygame.K_e]:
            self.monete += 1
            print("[Hai trovato una monetina nella fontanella]")
            self.thirsty = False
            assets.coin_sound.play()

    def take_damage(self, amount):
        self.vita -= amount
        if self.vita < 0:
            self.vita = 0

    def is_near_npc(self, npc):
        adjacent_npc = [
            (npc.tile_x, npc.tile_y + 1),
            (npc.tile_x + 1, npc.tile_y),
            (npc.tile_x - 1, npc.tile_y + 1),
            (npc.tile_x + 1, npc.tile_y - 1)
        ]
        return (self.tile_x, self.tile_y) in adjacent_npc
    
    def attacca(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if abs(self.tile_x - self.enemy.tile_x) <= 1 and abs(self.tile_y - self.enemy.tile_y) <= 1:
            if current_time - self.last_attack_time >= self.attack_cooldown:
                if keys[pygame.K_r]:
                    self.enemy.take_damage(20)
                    self.last_attack_time = current_time
 
