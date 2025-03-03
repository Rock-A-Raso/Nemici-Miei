import pygame
import assets
from settings import GRANDEZZA_TILES
from pygame.locals import *

class Enemy:
    def __init__(self, tile_x, tile_y, mondo, finestra, player):
        self.mondo = mondo
        self.finestra = finestra
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.player = player

        screen_x, screen_y = self.mondo.tile_to_screen(tile_x, tile_y)
        bottom_center = (screen_x + GRANDEZZA_TILES // 2, screen_y + GRANDEZZA_TILES)

        img = pygame.image.load('assets/[MOBS]/[BAT]/[UP]/1.png')
        self.image = pygame.transform.scale(img, (int(GRANDEZZA_TILES // 2), int(GRANDEZZA_TILES // 2)))
        self.rect = self.image.get_rect(midbottom=bottom_center)
        self.dest_x, self.dest_y = self.rect.topleft

        self.velocita = 2  
        self.in_movimento = False
        self.direction = "down"
        self.frame_index = 0
        self.frame_counter = 0

        self.last_attack_time = 0 
        self.attack_cooldown = 1000  

    def update(self):
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
            self.in_movimento = False
            self.calcola_prossima_mossa()

        self.attacca()
        self.finestra.blit(self.image, self.rect)

    def attacca(self):
        current_time = pygame.time.get_ticks()
        if self.tile_x == self.player.tile_x and self.tile_y == self.player.tile_y:
            if current_time - self.last_attack_time >= self.attack_cooldown:
                self.player.take_damage(3)
                self.last_attack_time = current_time

    def calcola_prossima_mossa(self):
        delta_x = self.player.tile_x - self.tile_x
        delta_y = self.player.tile_y - self.tile_y

        new_tile_x, new_tile_y = self.tile_x, self.tile_y
        if abs(delta_x) > abs(delta_y):
            if delta_x > 0:
                new_tile_x += 1
                self.direction = "right"
            else:
                new_tile_x -= 1
                self.direction = "left"
        else:
            if delta_y > 0:
                new_tile_y += 1
                self.direction = "down"
            else:
                new_tile_y -= 1
                self.direction = "up"

        if self.mondo.is_tile_walkable(new_tile_x, new_tile_y):
            self.tile_x, self.tile_y = new_tile_x, new_tile_y
            screen_x, screen_y = self.mondo.tile_to_screen(new_tile_x, new_tile_y)
            bottom_center = (screen_x + GRANDEZZA_TILES // 2, screen_y + GRANDEZZA_TILES // 2)
            self.dest_x = bottom_center[0] - self.rect.width // 2
            self.dest_y = bottom_center[1] - self.rect.height
            self.in_movimento = True

        self.image = assets.ENEMY_FRAMES[self.direction][self.frame_index]

    def animate(self):
        self.frame_counter += 1
        if self.frame_counter >= 15:
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(assets.ENEMY_FRAMES[self.direction])
        self.image = assets.ENEMY_FRAMES[self.direction][self.frame_index]
