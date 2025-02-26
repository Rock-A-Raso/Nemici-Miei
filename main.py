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
    1: pygame.image.load('assets/[BLOCCHI]/tile_000.png'),  # terreno
    2: pygame.image.load('assets/[BLOCCHI]/tile_003.png'),  # terreno 1
    3: pygame.image.load('assets/[BLOCCHI]/tile_022.png'),  # terreno erba
    4: pygame.image.load('assets/[BLOCCHI]/tile_023.png'),  # terreno erba media
    5: pygame.image.load('assets/[BLOCCHI]/tile_036.png'),  # erba alta
    6: pygame.image.load('assets/[BLOCCHI]/tile_044.png'),  # fiori tulipani
    7: pygame.image.load('assets/[BLOCCHI]/tile_105.png'),  # mare bordo destrino
    8: pygame.image.load('assets/[BLOCCHI]/tile_104.png'),  # mare no bordi
    9: pygame.image.load('assets/[BLOCCHI]/tile_109.png'),  # mare destra
    10: pygame.image.load('assets/[BLOCCHI]/tile_106.png'),  # mare bordo giù
    11: pygame.image.load('assets/[BLOCCHI]/tile_061.png'),  # ciottoli
    12: pygame.image.load('assets/[BLOCCHI]/tile_063.png'),  # pietra liscia
    13: pygame.image.load('assets/[BLOCCHI]/tile_064.png'),  # pila rocce
    14: pygame.image.load('assets/[BLOCCHI]/tile_077.png'),  # scogli
    15: pygame.image.load('assets/[BLOCCHI]/tile_053.png'),  # roccia arancione
    16: pygame.image.load('assets/[BLOCCHI]/tile_049.png'),  # pila tronchi
    17: pygame.image.load('assets/[BLOCCHI]/tile_050.png'),  # tronco
    18: pygame.image.load('assets/[BLOCCHI]/fontanella.png'),  # fontanella
}

# Classe Giocatore
class Giocatore():
    def __init__(self, x, y):
        img = pygame.image.load('assets/[BLOCCHI]/fontanella.png')
        self.image = pygame.transform.scale(img, (GRANDEZZA_TILES, GRANDEZZA_TILES))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, mondo):
        deltax = 0
        deltay = 0

        # Calcolare la posizione del giocatore in termini di tile
        tile_x = self.rect.x // GRANDEZZA_TILES
        tile_y = self.rect.y // GRANDEZZA_TILES

        # Controlli
        tasti = pygame.key.get_pressed()
        if tasti[pygame.K_a]:  
            if mondo.is_tile_walkable(tile_x - 1, tile_y): 
                deltax -= GRANDEZZA_TILES // 4
        if tasti[pygame.K_d]:  
            if mondo.is_tile_walkable(tile_x + 1, tile_y):  
                deltax += GRANDEZZA_TILES // 4
        if tasti[pygame.K_s]:  
            if mondo.is_tile_walkable(tile_x, tile_y + 1):  
                deltay += GRANDEZZA_TILES // 4
        if tasti[pygame.K_w]:  
            if mondo.is_tile_walkable(tile_x, tile_y - 1):  
                deltay -= GRANDEZZA_TILES // 4

        # Aggiorna la posizione del giocatore
        self.rect.x += deltax
        self.rect.y += deltay

        # Disegna il giocatore
        finestra.blit(self.image, self.rect)


class Mondo():
    def __init__(self, matrice):
        self.lista_tiles = []
        self.lista_fontanelle = []
        self.matrice = matrice  # Salva la matrice del mondo

        # calcolo numero di celle totali nella finestra di gioco
        celle_x = LUNGHEZZA // GRANDEZZA_TILES
        celle_y = ALTEZZA // GRANDEZZA_TILES

        # centro finestra
        centro_finestra_x = LUNGHEZZA // 2
        centro_finestra_y = ALTEZZA // 2

        # centro matrice
        num_righe = len(matrice)
        num_colonne = len(matrice[0])
        centro_matrice_x = (num_colonne - 1 - (num_righe - 1)) * (GRANDEZZA_TILES // 2) // 2
        centro_matrice_y = (num_colonne - 1 + (num_righe - 1)) * (GRANDEZZA_TILES // 4) // 2

        for riga_cont, riga in enumerate(matrice):
            for cal_cont, tile in enumerate(riga):
                if tile in TILE_IMAGES:
                    iso_x = (cal_cont - riga_cont) * (GRANDEZZA_TILES // 2) + centro_finestra_x - centro_matrice_x
                    iso_y = (cal_cont + riga_cont) * (GRANDEZZA_TILES // 4) + centro_finestra_y - centro_matrice_y

                    if tile in [7, 8, 9, 10]:
                        iso_y -= 10

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

    def is_tile_walkable(self, x, y):
        if 0 <= y < len(self.matrice) and 0 <= x < len(self.matrice[0]):
            tile = self.matrice[y][x]
            return tile in [1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 16, 17]
        return False  

giocatore = Giocatore(0, 0)

# Istanza del mondo
matrice = [
    [3, 7, 7, 7, 7, 7, 7, 3, 3, 3],
    [3, 8, 8, 8, 8, 8, 8, 3, 3, 3],
    [3, 3, 8, 8, 8, 8, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 18, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]

mondo = Mondo(matrice)
clock = pygame.time.Clock()
run = True

# Loop di gioco
while run:
    finestra.fill((0, 0, 0))  # Sfondo nero
    mondo.disegna()
    giocatore.update(mondo)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    clock.tick(FPS)

pygame.quit()
