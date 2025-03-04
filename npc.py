import pygame
import assets
from settings import GRANDEZZA_TILES

class Npc:
    def __init__(self, tile_x, tile_y, mondo, finestra):
        self.mondo = mondo
        self.finestra = finestra
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.parlando = False
        sx, sy = self.mondo.tile_to_screen(tile_x, tile_y)
        bottom_center = (sx + GRANDEZZA_TILES // 2, sy + GRANDEZZA_TILES)
        
        img = pygame.image.load('assets/[NPC]/1.png')
        self.scale_factor = 0.75
        new_size = (int(GRANDEZZA_TILES * self.scale_factor), int(GRANDEZZA_TILES * self.scale_factor))
        self.image = pygame.transform.scale(img, new_size)
        self.rect = self.image.get_rect(midbottom=bottom_center)
        self.nome = "Npc1"
    
    def update(self):
        self.finestra.blit(self.image, self.rect)

    def dialogo(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.parlando = True