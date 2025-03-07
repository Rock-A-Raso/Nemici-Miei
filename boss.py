import pygame
import assets
from settings import GRANDEZZA_TILES

class Boss:
    def __init__(self, tile_x, tile_y, mondo, finestra, player, img, damage, hp):
        self.start(tile_x, tile_y, mondo, finestra, player, img, damage, hp)
        
    def start(self, tile_x, tile_y, mondo, finestra, player, img, damage, hp):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.hp = hp
        self.mondo = mondo
        self.finestra = finestra
        self.player = player
        self.img = img
        self.speed = 6
        self.damage = damage
        self.direction = "down"
        self.frame = 0
        self.frame_index = 0
        self.counter = 0
        self.last_attack_time = 0
        self.reg_tile_x = 0
        self.reg_tile_y = 0
        self.in_movimento = False
        self.rigenerando = False
        self.counter_reg = 0
        self.hp_max = 200
        sx, sy = self.mondo.tile_to_screen(tile_x, tile_y)
        bottom_center = (sx + GRANDEZZA_TILES // 2, sy + GRANDEZZA_TILES)
        self.rect = self.img.get_rect(midbottom=bottom_center)
        self.dest_x, self.dest_y = self.rect.topleft

    def update(self):
        if self.rect.topleft != (self.dest_x, self.dest_y):
            dx = self.dest_x - self.rect.x
            dy = self.dest_y - self.rect.y
            if dx:
                self.rect.x += self.speed if dx > 0 else -self.speed
                if abs(dx) < self.speed:
                    self.rect.x = self.dest_x
            if dy:
                self.rect.y += self.speed if dy > 0 else -self.speed
                if abs(dy) < self.speed:
                    self.rect.y = self.dest_y
            self.animate()
        else:
            self.in_movimento = False
            self.calcola_prossima_mossa()

        if self.rigenerando and self.counter_reg <= 600 and self.hp != 0 and self.tile_x == self.reg_tile_x and self.tile_y == self.reg_tile_y:
            self.hp += 0.05
            self.counter_reg += 1
            if self.hp >= self.hp_max:
                self.hp = self.hp_max
            if self.counter_reg == 180:
                self.rigenerando = False
                self.attacca()

        if self.hp <= 100:
            self.img = pygame.transform.scale(self.img, (GRANDEZZA_TILES, GRANDEZZA_TILES))
            self.velocita = 8
            self.hp_max = 100
        self.attacca()
        self.finestra.blit(self.img, self.rect)

    def attacca(self):
        if  ((self.tile_x == self.player.tile_x or self.tile_x == self.player.tile_x + 1 or self.tile_x == self.player.tile_x + 2) and (self.tile_y == self.player.tile_y or self.tile_x == self.player.tile_x + 1 or self.tile_x == self.player.tile_x + 2)) and not self.rigenerando:
                self.player.take_damage(self.damage)
                self.rigenerando = True

    def calcola_prossima_mossa(self):
        if self.rigenerando:
            dx = self.reg_tile_x - self.tile_x
            dy = self.reg_tile_y - self.tile_y
        else:
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
        self.frame += 1
        if self.frame >= 60:
            self.frame = 0
        frame = assets.BOSS_FRAMES[self.direction][self.frame_index]
        self.img = frame
    
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
            assets.sounds["morte"].play()    
            