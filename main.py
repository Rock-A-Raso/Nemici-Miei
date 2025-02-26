import pygame
from pygame.locals import *

pygame.init()

# Costanti
ALTEZZA = 720
LUNGHEZZA = 960
GRANDEZZA_TILES = 72
FPS = 60

# Finestra di gioco
finestra = pygame.display.set_mode((LUNGHEZZA, ALTEZZA))
pygame.display.set_caption("Rock A' Raso")

# Caricamento immagini
TILE_IMAGES = {
    1: pygame.image.load('assets/[BLOCCHI]/tile_000.png'), # terreno 
    2: pygame.image.load('assets/[BLOCCHI]/tile_003.png'), # terreno 1
    3: pygame.image.load('assets/[BLOCCHI]/tile_022.png'), # terreno erba
    4: pygame.image.load('assets/[BLOCCHI]/tile_023.png'), # terreno erba media
    5: pygame.image.load('assets/[BLOCCHI]/tile_036.png'), # erba alta
    6: pygame.image.load('assets/[BLOCCHI]/tile_044.png'), # fiori tulipani
    7: pygame.image.load('assets/[BLOCCHI]/tile_046.png'), # fiori misti
    8: pygame.image.load('assets/[BLOCCHI]/tile_104.png'), # mare no bordi
    9: pygame.image.load('assets/[BLOCCHI]/tile_112.png'), # mare bordo destra e giù
    10: pygame.image.load('assets/[BLOCCHI]/tile_107.png'), # mare bordo giù
    11: pygame.image.load('assets/[BLOCCHI]/tile_061.png'), # ciottoli
    12: pygame.image.load('assets/[BLOCCHI]/tile_063.png'), # pietra liscia
    13: pygame.image.load('assets/[BLOCCHI]/tile_064.png'), # pila rocce
    14: pygame.image.load('assets/[BLOCCHI]/tile_077.png'), # scogli
    15: pygame.image.load('assets/[BLOCCHI]/tile_053.png'), # roccia arancione
    16: pygame.image.load('assets/[BLOCCHI]/tile_049.png'), # pila tronchi
    17: pygame.image.load('assets/[BLOCCHI]/tile_050.png'), # tronco
    18: pygame.image.load('assets/[BLOCCHI]/fontanella.png') # fontanella test
}

class HUD():
    def __init__(self):
        pass

class Mondo():
    def __init__(self, matrice):
        self.lista_tiles = []
        self.lista_fontanelle = []
        
        for riga_cont, riga in enumerate(matrice):
            for cal_cont, tile in enumerate(riga):
                if tile in TILE_IMAGES:
                    iso_x = (cal_cont - riga_cont) * (GRANDEZZA_TILES // 2)
                    iso_y = (cal_cont + riga_cont) * (GRANDEZZA_TILES // 4)
                    
                    if tile == 18:
                        img_sotto = pygame.transform.scale(TILE_IMAGES[3], (GRANDEZZA_TILES, GRANDEZZA_TILES))
                        img_sotto_ratt = img_sotto.get_rect(topleft=(iso_x, iso_y))
                        self.lista_tiles.append((img_sotto, img_sotto_ratt))

                        # Ora creiamo la fontanella
                        img = pygame.transform.scale(TILE_IMAGES[tile], (100, 100))
                        img_ratt = img.get_rect(midbottom=(iso_x + GRANDEZZA_TILES // 2, iso_y + GRANDEZZA_TILES))
                        self.lista_fontanelle.append((img, img_ratt))
                    else:
                        img = pygame.transform.scale(TILE_IMAGES[tile], (GRANDEZZA_TILES, GRANDEZZA_TILES))
                        img_ratt = img.get_rect(topleft=(iso_x, iso_y))
                        self.lista_tiles.append((img, img_ratt))
    
    def disegna(self):
        for img, img_ratt in self.lista_tiles:
            finestra.blit(img, img_ratt)
        for img, img_ratt in self.lista_fontanelle:  # Disegna la fontanella sopra il terreno
            finestra.blit(img, img_ratt)

# Istanza del mondo
matrice = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 18, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]

mondo = Mondo(matrice)
clock = pygame.time.Clock()
run = True

# Loop di gioco
while run:
    finestra.fill((0, 0, 0))  # Sfondo nero
    mondo.disegna()
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    clock.tick(FPS)

pygame.quit()