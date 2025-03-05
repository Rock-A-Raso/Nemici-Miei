import pygame
import assets
from settings import GRANDEZZA_TILES

class portals:
    def __init__(self, tile_x, tile_y, mondo, finestra):
        self.mondo = mondo
        self.finestra = finestra
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.frame_index = 0
        self.frame_counter = 0
        sx, sy = self.mondo.tile_to_screen(tile_x, tile_y)
        bottom_center = (sx + GRANDEZZA_TILES // 2, sy + GRANDEZZA_TILES // 2)
        self.scale_factor = 0.75    
        self.new_size = (int(GRANDEZZA_TILES * self.scale_factor), int(GRANDEZZA_TILES * self.scale_factor))
        self.img = assets.PORTAL_FRAMES[self.frame_index]
        self.img = pygame.transform.scale(self.img, self.new_size)
        self.rect = self.img.get_rect(midbottom=bottom_center)
    
    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= 10:  
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(assets.PORTAL_FRAMES)
            self.img = assets.PORTAL_FRAMES[self.frame_index]
            self.img = pygame.transform.scale(self.img, self.new_size)
        
        self.finestra.blit(self.img, self.rect)