import pygame
import assets
from settings import GRANDEZZA_TILES

class Enemy:
    def __init__(self, tile_x, tile_y, mondo, finestra, player, img, hp, cooldown, velocita, dmg):
        self.mondo = mondo
        self.finestra = finestra
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.player = player
        self.img = img
        self.hp = hp
        self.cooldown = cooldown
        self.velocita = velocita
        self.dmg = dmg
        sx, sy = self.mondo.tile_to_screen(tile_x, tile_y)
        bottom_center = (sx + GRANDEZZA_TILES // 2, sy + GRANDEZZA_TILES)

        self.scale_factor = 1.5
        new_size = (int(GRANDEZZA_TILES * self.scale_factor), int(GRANDEZZA_TILES * self.scale_factor))
        self.img = pygame.transform.scale(self.img, new_size)
        self.rect = self.img.get_rect(midbottom=bottom_center)    
        self.dest_x, self.dest_y = self.rect.topleft
        self.in_movimento = False
        self.direction = "down"
        self.frame_index = 0
        self.frame_counter = 0
        self.last_attack_time = 0

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
        self.finestra.blit(self.img, self.rect)

    def attacca(self):
        current_time = pygame.time.get_ticks()
        if self.tile_x == self.player.tile_x and self.tile_y == self.player.tile_y:
            if current_time - self.last_attack_time >= self.cooldown:
                self.player.take_damage(self.dmg)
                self.last_attack_time = current_time

    def calcola_prossima_mossa(self):
        dx = self.player.tile_x - self.tile_x
        dy = self.player.tile_y - self.tile_y
        new_tx, new_ty = self.tile_x, self.tile_y
        if abs(dx) > abs(dy):
            if dx > 0:
                new_tx += 1
                self.direction = "right"
            else:
                new_tx -= 1
                self.direction = "left"
        else:
            if dy > 0:
                new_ty += 1
                self.direction = "down"
            else:
                new_ty -= 1
                self.direction = "up"
                
        if self.mondo.is_tile_walkable(new_tx, new_ty):
            self.tile_x, self.tile_y = new_tx, new_ty
            sx, sy = self.mondo.tile_to_screen(new_tx, new_ty)
            bottom_center = (sx + GRANDEZZA_TILES // 2, sy + GRANDEZZA_TILES // 2)
            self.dest_x = bottom_center[0] - self.rect.width // 2
            self.dest_y = bottom_center[1] - self.rect.height
            self.in_movimento = True
        self.animate()

    def animate(self):
        self.frame_counter += 1
        if self.frame_counter >= 15:
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(assets.ENEMY_FRAMES[self.direction])
        frame = assets.ENEMY_FRAMES[self.direction][self.frame_index]
        new_size = (int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor))
        self.img = pygame.transform.scale(frame, new_size)
        self.rect = self.img.get_rect(midbottom=self.rect.midbottom)

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
            assets.morte_sound.play()