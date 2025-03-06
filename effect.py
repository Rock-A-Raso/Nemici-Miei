import pygame
import assets
from settings import GRANDEZZA_TILES

class blood_effect:
    def __init__(self, tile_x, tile_y, mondo, finestra, durata):
        self.mondo = mondo
        self.finestra = finestra
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.frame_index = 0
        self.frame_counter = 0
        self.durata = durata  # Durata in frame
        self.timer = 0  # Timer per tenere traccia del tempo trascorso
        sx, sy = self.mondo.tile_to_screen(tile_x, tile_y)
        bottom_center = (sx + GRANDEZZA_TILES // 2, sy + GRANDEZZA_TILES // 2)
        self.scale_factor = 0.75    
        self.new_size = (int(GRANDEZZA_TILES * self.scale_factor), int(GRANDEZZA_TILES * self.scale_factor))
        self.img = assets.BLOOD_FRAMES[self.frame_index]
        self.img = pygame.transform.scale(self.img, self.new_size)
        self.rect = self.img.get_rect(midbottom=bottom_center)
    
    def update(self):
        self.timer += 1
        if self.timer >= self.durata:
            return

        self.frame_counter += 1
        if self.frame_counter >= 10:
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(assets.BLOOD_FRAMES)
            self.img = assets.BLOOD_FRAMES[self.frame_index]
            self.img = pygame.transform.scale(self.img, self.new_size)
        
        self.finestra.blit(self.img, self.rect)