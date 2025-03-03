import pygame
import random
import assets
from settings import GRANDEZZA_TILES, LUNGHEZZA, ALTEZZA  # Assicurati di importare ALTEZZA
# Definizione dei tile camminabili
WALKABLE_TILES = {1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 16, 17, 20, 21}

class Mondo:
    def __init__(self, livello_id, finestra, livelli):
        self.livello_id = livello_id
        self.finestra = finestra
        self.livelli = livelli  # Dizionario dei livelli
        self.sfondo = pygame.image.load('assets/[SFONDI]/bg.png')
        self.sfondo = pygame.transform.scale(self.sfondo, (LUNGHEZZA, self.finestra.get_height()))
        
        # Offset iniziali (saranno ricalcolati)
        self.offset_x = 0
        self.offset_y = 0
        
        self.carica_mondo()

    def calcola_offset(self):
        """
        Calcola gli offset per centrare il mondo nell'area di gioco, escludendo la HUD.
        La trasformazione isometrica è:
        x = (tile_x - tile_y) * (GRANDEZZA_TILES/2)
        y = (tile_x + tile_y) * (GRANDEZZA_TILES/4)
        """
        HUD_HEIGHT = 100  # Altezza della HUD
        ALTEZZA_eff = ALTEZZA - HUD_HEIGHT  # Altezza effettiva dell'area di gioco

        ncols = self.num_colonne
        nrows = self.num_righe
        tile_w = GRANDEZZA_TILES  # Base per le dimensioni dei tile

        # Calcola le coordinate (senza offset) dei quattro angoli del livello
        angoli = []
        for (tile_x, tile_y) in [(0, 0), (ncols - 1, 0), (0, nrows - 1), (ncols - 1, nrows - 1)]:
            x = (tile_x - tile_y) * (tile_w / 2)
            y = (tile_x + tile_y) * (tile_w / 4)
            angoli.append((x, y))
        xs = [p[0] for p in angoli]
        ys = [p[1] for p in angoli]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        centro_x = (min_x + max_x) / 2
        centro_y = (min_y + max_y) / 2

        # Imposta gli offset in modo che il centro del mondo (senza HUD) coincida con il centro dell'area di gioco
        self.offset_x = LUNGHEZZA / 2 - centro_x
        self.offset_y = ALTEZZA_eff / 2 - centro_y


    def carica_mondo(self):
        self.matrice = self.livelli[self.livello_id]
        self.num_righe = len(self.matrice)
        self.num_colonne = len(self.matrice[0])
        self.lista_tiles = []
        self.lista_fontanelle = []
        self.lista_fiori = []  # Lista per i fiori
        self.lista_log = []    # Lista per i tronchi
        self.lista_tulipani = []    # Lista per i tulipani
        self.lista_ciottoli = []    # Lista per i ciottoli

        # Calcola gli offset per centrare il mondo
        self.calcola_offset()

        for riga in range(self.num_righe):
            for col in range(self.num_colonne):
                tile_val = self.matrice[riga][col]
                if tile_val in assets.TILE_IMAGES:
                    screen_x, screen_y = self.tile_to_screen(col, riga)
                    if tile_val in [7, 8, 9, 10]:
                        screen_y -= 10
                    if tile_val == 18:
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
                        
                        if tile_val in [3, 4, 5] and random.random() < 0.1:
                            img_fiori = pygame.transform.scale(assets.TILE_IMAGES[6], (GRANDEZZA_TILES // 2, GRANDEZZA_TILES // 2))
                            rect_fiori = img_fiori.get_rect(center=(screen_x + GRANDEZZA_TILES // 2,
                                                                      screen_y + GRANDEZZA_TILES // 2))
                            self.lista_fiori.append((img_fiori, rect_fiori))
                        if tile_val in [3, 4, 5] and random.random() < 0.05:
                            img_log = pygame.transform.scale(assets.TILE_IMAGES[17], (GRANDEZZA_TILES // 2, GRANDEZZA_TILES // 2))
                            rect_log = img_log.get_rect(center=(screen_x + GRANDEZZA_TILES // 2,
                                                                  screen_y + GRANDEZZA_TILES // 2))
                            self.lista_log.append((img_log, rect_log))
                        if tile_val in [3, 4, 5] and random.random() < 0.03:
                            img_tulipani = pygame.transform.scale(assets.TILE_IMAGES[21], (GRANDEZZA_TILES // 2, GRANDEZZA_TILES // 2))
                            rect_tulipani = img_tulipani.get_rect(center=(screen_x + GRANDEZZA_TILES // 2,
                                                                  screen_y + GRANDEZZA_TILES // 2))
                            self.lista_tulipani.append((img_tulipani, rect_tulipani))
                        if tile_val in [3, 4, 5] and random.random() < 0.02:
                            img_ciottoli = pygame.transform.scale(assets.TILE_IMAGES[15], (GRANDEZZA_TILES // 2, GRANDEZZA_TILES // 2))
                            rect_ciottoli = img_ciottoli.get_rect(center=(screen_x + GRANDEZZA_TILES // 2,
                                                                  screen_y + GRANDEZZA_TILES // 2))
                            self.lista_ciottoli.append((img_ciottoli, rect_ciottoli))


    def tile_to_screen(self, tile_x, tile_y):
        # Usa divisione float per maggiore precisione
        screen_x = (tile_x - tile_y) * (GRANDEZZA_TILES / 2) + self.offset_x
        screen_y = (tile_x + tile_y) * (GRANDEZZA_TILES / 4) + self.offset_y
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
        self.finestra.blit(self.sfondo, (0, 0))
        for img, rect in self.lista_tiles:
            self.finestra.blit(img, rect)
        for img, rect in self.lista_fontanelle:
            self.finestra.blit(img, rect)
        for img, rect in self.lista_fiori:
            self.finestra.blit(img, rect)
        for img, rect in self.lista_log:
            self.finestra.blit(img, rect)
        for img, rect in self.lista_tulipani:
            self.finestra.blit(img, rect)
        for img, rect in self.lista_ciottoli:
            self.finestra.blit(img, rect)
    
    def trova_fontanella(self):
        for riga in range(self.num_righe):
            for col in range(self.num_colonne):
                if self.matrice[riga][col] == 18:
                    return col, riga  
        return None, None

    def nuovo_livello(self, nuovo_livello):
        if nuovo_livello in self.livelli:
            self.livello_id = nuovo_livello
            self.carica_mondo()