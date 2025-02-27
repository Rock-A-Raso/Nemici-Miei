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
        bottom_center = (screen_x + GRANDEZZA_TILES // 2, screen_y + GRANDEZZA_TILES // 2)
        img = pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[DOWN]/walkd1.png')
        self.image = pygame.transform.scale(img, (int(GRANDEZZA_TILES / 2), int(GRANDEZZA_TILES / 2)))
        self.rect = self.image.get_rect(midbottom=bottom_center)
        self.dest_x, self.dest_y = self.rect.topleft
        self.velocita = 8
        self.in_movimento = False
        self.fountain_x, self.fountain_y = self.mondo.trova_fontanella()
        self.thirsty = True
        self.direction = "down"
        self.frame_index = 0
        self.frame_counter = 0

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
            keys = pygame.key.get_pressed()
            new_tile_x, new_tile_y = self.tile_x, self.tile_y
            if keys[pygame.K_a]:
                new_tile_x -= 1
                self.direction = "left"
                self.in_movimento = True
            if keys[pygame.K_d]:
                new_tile_x += 1
                self.direction = "right"
                self.in_movimento = True
            if keys[pygame.K_w]:
                new_tile_y -= 1
                self.direction = "up"
                self.in_movimento = True
            if keys[pygame.K_s]:
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
                    # Scegliamo un suono casuale dalla lista
                    random.choice(assets.grass_sounds).play(maxtime=300, fade_ms=50)

            if not self.in_movimento:
                self.idle()
            else:
                self.image = assets.PLAYER_FRAMES[self.direction][self.frame_index]
            self.finestra.blit(self.image, self.rect)

        self.image = assets.PLAYER_FRAMES[self.direction][self.frame_index]
        self.finestra.blit(self.image, self.rect)

    def animate(self):
        self.frame_counter += 1
        if self.frame_counter >= 15:
            self.frame_counter = 0
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
        self.finestra.blit(self.image, self.rect)

    def is_near_fountain(self):
        if self.fountain_x is None or self.fountain_y is None:
            return False
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
        if self.is_near_fountain() and self.thirsty:
            print("Biv.")
            self.thirsty = False
