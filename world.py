import pygame
import random
import assets
from settings import LUNGHEZZA, GRANDEZZA_TILES, OFFSET_Y

# Definizione dei tile camminabili
WALKABLE_TILES = {1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 16, 17}

class Mondo:
    def __init__(self, matrice, finestra):
        self.matrice = matrice
        self.num_righe = len(matrice)
        self.num_colonne = len(matrice[0])
        self.lista_tiles = []
        self.lista_fontanelle = []
        self.lista_fiori = []  # Lista per i fiori
        self.lista_log = []    # Lista per i tronchi
        self.finestra = finestra
        self.sfondo = pygame.image.load('assets/[SFONDI]/bg.png')  # Cambia il percorso con il tuo file
        self.sfondo = pygame.transform.scale(self.sfondo, (LUNGHEZZA, self.finestra.get_height()))


        # Definizione degli offset per il rendering isometrico
        self.offset_x = LUNGHEZZA // 2
        self.offset_y = OFFSET_Y

        for riga in range(self.num_righe):
            for col in range(self.num_colonne):
                tile_val = self.matrice[riga][col]
                if tile_val in assets.TILE_IMAGES:
                    screen_x, screen_y = self.tile_to_screen(col, riga)
                    if tile_val in [7, 8, 9, 10]:
                        screen_y -= 10
                    if tile_val == 18:
                        # Disegna il terreno sottostante e poi la fontanella
                        img_ground = pygame.transform.scale(assets.TILE_IMAGES[3], (GRANDEZZA_TILES, GRANDEZZA_TILES))
                        rect_ground = img_ground.get_rect(topleft=(screen_x, screen_y))
                        self.lista_tiles.append((img_ground, rect_ground))
                        img_font = pygame.transform.scale(assets.TILE_IMAGES[tile_val], (100, 100))
                        bottom_center = (screen_x + GRANDEZZA_TILES // 2, screen_y + GRANDEZZA_TILES // 2)
                        rect_font = img_font.get_rect(midbottom=bottom_center)
                        self.lista_fontanelle.append((img_font, rect_font))
                    else:
                        img = pygame.transform.scale(assets.TILE_IMAGES[tile_val], (GRANDEZZA_TILES, GRANDEZZA_TILES))
                        rect = img.get_rect(topleft=(screen_x, screen_y))
                        self.lista_tiles.append((img, rect))
                        
                        # Generazione casuale dei fiori sui pezzi di erba
                        if tile_val in [3, 4, 5] and random.random() < 0.1:
                            img_fiore = pygame.transform.scale(assets.TILE_IMAGES[6], (GRANDEZZA_TILES // 2, GRANDEZZA_TILES // 2))
                            rect_fiore = img_fiore.get_rect(center=(screen_x + GRANDEZZA_TILES // 2,
                                                                      screen_y + GRANDEZZA_TILES // 2))
                            self.lista_fiori.append((img_fiore, rect_fiore))

                        # Generazione casuale dei log (tronchi) sui pezzi di erba
                        if tile_val in [3, 4, 5] and random.random() < 0.05:
                            img_log = pygame.transform.scale(assets.TILE_IMAGES[16], (GRANDEZZA_TILES // 2, GRANDEZZA_TILES // 2))
                            rect_log = img_log.get_rect(center=(screen_x + GRANDEZZA_TILES // 2,
                                                                  screen_y + GRANDEZZA_TILES // 2))
                            self.lista_log.append((img_log, rect_log))

    def tile_to_screen(self, tile_x, tile_y):
        screen_x = (tile_x - tile_y) * (GRANDEZZA_TILES // 2) + self.offset_x
        screen_y = (tile_x + tile_y) * (GRANDEZZA_TILES // 4) + self.offset_y
        return screen_x, screen_y

    def screen_to_tile(self, screen_x, screen_y):
        x_prime = screen_x - self.offset_x
        y_prime = screen_y - self.offset_y
        half_w = GRANDEZZA_TILES / 2
        quarter_w = GRANDEZZA_TILES / 4
        tile_x = int(round(((x_prime / half_w) + (y_prime / quarter_w)) / 2))
        tile_y = int(round(((y_prime / quarter_w) - (x_prime / half_w)) / 2))
        return tile_x, tile_y

    def is_tile_walkable(self, tile_x, tile_y):
        if 0 <= tile_y < self.num_righe and 0 <= tile_x < self.num_colonne:
            tile = self.matrice[tile_y][tile_x]
            return tile in WALKABLE_TILES
        return False

    def disegna(self):
        self.finestra.blit(self.sfondo, (0, 0))  # Disegna prima lo sfondo
        for img, rect in self.lista_tiles:
            self.finestra.blit(img, rect)
        for img, rect in self.lista_fontanelle:
            self.finestra.blit(img, rect)
        for img, rect in self.lista_fiori:
            self.finestra.blit(img, rect)
        for img, rect in self.lista_log:
            self.finestra.blit(img, rect)
    
    def trova_fontanella(self):
        for riga in range(self.num_righe):
            for col in range(self.num_colonne):
                if self.matrice[riga][col] == 18:
                    return col, riga  
        return None, None
