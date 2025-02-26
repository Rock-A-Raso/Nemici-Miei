import pygame
from pygame.locals import *

pygame.init()

# Costanti
ALTEZZA = 720
LUNGHEZZA = 960
GRANDEZZA_TILES = 72
FPS = 60

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
    19: pygame.image.load('assets/[BLOCCHI]/tile_022.png'),  # terreno erba non camminabile
}

# tile camminabili
WALKABLE_TILES = {1,2,3,4,5,6,11,12,13,14,15,16,17}

class Mondo():
    def __init__(self, matrice):
        self.matrice = matrice
        self.num_righe = len(matrice)
        self.num_colonne = len(matrice[0])
        # Calcola il bounding box della mappa isometrica
        min_x = (0 - (self.num_righe - 1)) * (GRANDEZZA_TILES // 2)
        max_x = ((self.num_colonne - 1) - 0) * (GRANDEZZA_TILES // 2) + GRANDEZZA_TILES
        min_y = 0
        max_y = ((self.num_colonne - 1) + (self.num_righe - 1)) * (GRANDEZZA_TILES // 4) + GRANDEZZA_TILES
        center_x = (min_x + max_x) // 2
        center_y = (min_y + max_y) // 2
        self.offset_x = LUNGHEZZA // 2 - center_x
        self.offset_y = ALTEZZA // 2 - center_y

        self.lista_tiles = []
        self.lista_fontanelle = []
        for riga in range(self.num_righe):
            for col in range(self.num_colonne):
                tile_val = self.matrice[riga][col]
                if tile_val in TILE_IMAGES:
                    screen_x, screen_y = self.tile_to_screen(col, riga)
                    # regola l'offset verticale
                    if tile_val in [7,8,9,10]:
                        screen_y -= 10
                    if tile_val == 18:
                        # disegna il terreno
                        img_ground = pygame.transform.scale(TILE_IMAGES[3], (GRANDEZZA_TILES, GRANDEZZA_TILES))
                        rect_ground = img_ground.get_rect(topleft=(screen_x, screen_y))
                        self.lista_tiles.append((img_ground, rect_ground))
                        # disegna la fontanella
                        img_font = pygame.transform.scale(TILE_IMAGES[tile_val], (100, 100))
                        bottom_center = (screen_x + GRANDEZZA_TILES//2, screen_y + GRANDEZZA_TILES//2)
                        rect_font = img_font.get_rect(midbottom=bottom_center)
                        self.lista_fontanelle.append((img_font, rect_font))
                    else:
                        img = pygame.transform.scale(TILE_IMAGES[tile_val], (GRANDEZZA_TILES, GRANDEZZA_TILES))
                        rect = img.get_rect(topleft=(screen_x, screen_y))
                        self.lista_tiles.append((img, rect))

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
        for img, rect in self.lista_tiles:
            finestra.blit(img, rect)
        for img, rect in self.lista_fontanelle:
            finestra.blit(img, rect)

###############################################################################
# Classe Giocatore: il movimento avviene tile per tile. Il personaggio
# è ancorato in modo che sia allineato al
# centro in basso del tile.
###############################################################################
class Giocatore():
    def __init__(self, tile_x, tile_y, mondo):
        self.mondo = mondo
        self.tile_x = tile_x
        self.tile_y = tile_y
        screen_x, screen_y = mondo.tile_to_screen(tile_x, tile_y)
        bottom_center = (screen_x + GRANDEZZA_TILES//2, screen_y + GRANDEZZA_TILES//2)
        img = pygame.image.load('assets/[PERSONAGGIO]/walkd1.png')
        self.image = pygame.transform.scale(img, (GRANDEZZA_TILES // 2, GRANDEZZA_TILES // 2))
        self.rect = self.image.get_rect(midbottom=bottom_center)
        self.dest_x, self.dest_y = self.rect.topleft
        self.velocita = 8
        self.in_movimento = False

    def update(self):
        # se non ha ancora raggiunto la destinazione, continua a muoversi
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
        else:
            self.in_movimento = False
            tasti = pygame.key.get_pressed()
            new_tile_x, new_tile_y = self.tile_x, self.tile_y
            if tasti[pygame.K_a]:
                new_tile_x -= 1
            if tasti[pygame.K_d]:
                new_tile_x += 1
            if tasti[pygame.K_w]:
                new_tile_y -= 1
            if tasti[pygame.K_s]:
                new_tile_y += 1
            if self.mondo.is_tile_walkable(new_tile_x, new_tile_y):
                self.tile_x, self.tile_y = new_tile_x, new_tile_y
                screen_x, screen_y = self.mondo.tile_to_screen(new_tile_x, new_tile_y)
                bottom_center = (screen_x + GRANDEZZA_TILES//2, screen_y + GRANDEZZA_TILES//2)
                self.dest_x = bottom_center[0] - self.rect.width // 2
                self.dest_y = bottom_center[1] - self.rect.height
                self.in_movimento = True
        finestra.blit(self.image, self.rect)

matrice = [
    [3, 7, 7, 7, 7, 7, 7, 3, 3, 3],
    [3, 8, 8, 8, 8, 8, 8, 3, 3, 3],
    [3, 3, 8, 8, 8, 8, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 19, 19, 3, 3, 3, 3],
    [3, 3, 3, 3, 19, 18, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]

mondo = Mondo(matrice)
player = Giocatore(0, 0, mondo)

clock = pygame.time.Clock()
run = True

while run:
    finestra.fill((0, 0, 0))
    mondo.disegna()
    player.update()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
    clock.tick(FPS)

pygame.quit()
