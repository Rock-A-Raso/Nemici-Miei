import pygame
from pygame.locals import *

pygame.init()

# Costanti
ALTEZZA = 720
LUNGHEZZA = 960
GRANDEZZA_TILES = 48
FPS = 60

# Finestra di gioco
finestra = pygame.display.set_mode((LUNGHEZZA, ALTEZZA))
pygame.display.set_caption("Rock A' Raso")

# Caricamento immagini
TILE_IMAGES = {
    1: pygame.image.load('assets/[BLOCCHI]/tile_000.png'),
    2: pygame.image.load('assets/[BLOCCHI]/tile_003.png'),
    3: pygame.image.load('assets/[BLOCCHI]/tile_022.png'),
    4: pygame.image.load('assets/[BLOCCHI]/tile_023.png'),
    5: pygame.image.load('assets/[BLOCCHI]/tile_036.png'),
    6: pygame.image.load('assets/[BLOCCHI]/tile_044.png'),
    7: pygame.image.load('assets/[BLOCCHI]/tile_046.png'),
    8: pygame.image.load('assets/[BLOCCHI]/tile_104.png'),
    9: pygame.image.load('assets/[BLOCCHI]/tile_112.png'),
    10: pygame.image.load('assets/[BLOCCHI]/tile_107.png'),
    11: pygame.image.load('assets/[BLOCCHI]/tile_061.png'),
    12: pygame.image.load('assets/[BLOCCHI]/tile_063.png'),
    13: pygame.image.load('assets/[BLOCCHI]/tile_064.png'),
    14: pygame.image.load('assets/[BLOCCHI]/tile_077.png'),
    15: pygame.image.load('assets/[BLOCCHI]/tile_053.png'),
    16: pygame.image.load('assets/[BLOCCHI]/tile_049.png'),
    17: pygame.image.load('assets/[BLOCCHI]/tile_050.png')
}

class Mondo():
    def __init__(self, matrice):
        self.lista_tiles = []
        
        for riga_cont, riga in enumerate(matrice):
            for cal_cont, tile in enumerate(riga):
                if tile in TILE_IMAGES:  # Controllo se il tile esiste
                    img = pygame.transform.scale(TILE_IMAGES[tile], (GRANDEZZA_TILES, GRANDEZZA_TILES))
                    iso_x = (cal_cont - riga_cont) * (GRANDEZZA_TILES // 2)
                    iso_y = (cal_cont + riga_cont) * (GRANDEZZA_TILES // 4)
                    img_ratt = img.get_rect(topleft=(iso_x, iso_y))
                    self.lista_tiles.append((img, img_ratt))
    
    def disegna(self):
        for img, img_ratt in self.lista_tiles:
            finestra.blit(img, img_ratt)

# Istanza del mondo
matrice = [
    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
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
