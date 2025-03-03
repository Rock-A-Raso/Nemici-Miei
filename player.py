import pygame
import random
import assets
from settings import GRANDEZZA_TILES
from pygame.locals import *

class Giocatore:
    def __init__(self, tile_x, tile_y, mondo, finestra):
        self.mondo = mondo
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.finestra = finestra

        screen_x, screen_y = self.mondo.tile_to_screen(tile_x, tile_y)
        bottom_center = (screen_x + GRANDEZZA_TILES // 2, screen_y + GRANDEZZA_TILES)
        img = pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[DOWN]/walkd1.png')
        self.image = pygame.transform.scale(img, (int(GRANDEZZA_TILES // 2), int(GRANDEZZA_TILES // 2)))
        self.rect = self.image.get_rect(midbottom=bottom_center)
        self.dest_x, self.dest_y = self.rect.topleft
        self.velocita = 4
        self.in_movimento = False
        self.fountain_x, self.fountain_y = self.mondo.trova_fontanella()
        self.thirsty = True
        self.direction = "down"
        self.frame_index = 0
        self.frame_counter = 0

        # Statistiche per la HUD
        self.vita = 100
        self.vita_max = 100
        self.monete = 0
        self.level = 1
        self.exp = 0
        self.next_level_exp = 100

    def update(self):
        # Movimento verso la destinazione
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
            # Se non ci sono movimenti, controlla l'input
            self.in_movimento = False
            keys = pygame.key.get_pressed()
            new_tile_x, new_tile_y = self.tile_x, self.tile_y
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                new_tile_x -= 1
                self.direction = "left"
                self.in_movimento = True
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                new_tile_x += 1
                self.direction = "right"
                self.in_movimento = True
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                new_tile_y -= 1
                self.direction = "up"
                self.in_movimento = True
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                new_tile_y += 1
                self.direction = "down"
                self.in_movimento = True

            if self.mondo.is_tile_walkable(new_tile_x, new_tile_y):
                self.tile_x, self.tile_y = new_tile_x, new_tile_y
                screen_x, screen_y = self.mondo.tile_to_screen(new_tile_x, new_tile_y)
                bottom_center = (screen_x + GRANDEZZA_TILES // 2, screen_y + GRANDEZZA_TILES // 2)
                self.dest_x = bottom_center[0] - self.rect.width // 2
                self.dest_y = bottom_center[1] - self.rect.height
                if self.in_movimento:
                    random.choice(assets.grass_sounds).play(maxtime=300, fade_ms=50)
            # Se non ci sono input di movimento, usa l'animazione idle
            if not self.in_movimento:
                self.idle()
            else:
                self.image = assets.PLAYER_FRAMES[self.direction][self.frame_index]

        if self.mondo.matrice[self.tile_y][self.tile_x] == 20 and self.thirsty == False:
            self.mondo.nuovo_livello(2)
            self.level += 1

        self.image = assets.PLAYER_FRAMES[self.direction][self.frame_index]
        offset = 15
        draw_rect = self.rect.copy()
        draw_rect.y -= offset
        self.finestra.blit(self.image, draw_rect)

    def animate(self):
        self.frame_counter += 1
        if self.frame_counter >= 15:
            self.frame_counter = 15
            self.frame_index = (self.frame_index + 1) % len(assets.PLAYER_FRAMES[self.direction])
    
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
        # Nota: il blit verrà fatto alla fine di update()

    def is_near_fountain(self):
        adjacent_tiles = [
            (self.fountain_x, self.fountain_y - 2),
            (self.fountain_x, self.fountain_y + 1),
            (self.fountain_x - 2, self.fountain_y),
            (self.fountain_x + 1, self.fountain_y),
            (self.fountain_x - 1, self.fountain_y - 2),
            (self.fountain_x - 1, self.fountain_y + 1),
            (self.fountain_x - 2, self.fountain_y - 1),
            (self.fountain_x + 1, self.fountain_y - 1)
        ]
        return (self.tile_x, self.tile_y) in adjacent_tiles

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