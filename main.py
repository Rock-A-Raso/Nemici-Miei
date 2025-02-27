import pygame
from pygame.locals import *
from pygame import mixer
import random


pygame.init()

# Costanti
ALTEZZA = 720
LUNGHEZZA = 960
GRANDEZZA_TILES = 72
FPS = 60
#finestra di gioco
finestra = pygame.display.set_mode((LUNGHEZZA, ALTEZZA))
pygame.display.set_caption("Rock A' Raso")

# carica suoni
mixer.music.load('assets/audio/loop1_dungeon.mp3')
mixer.music.set_volume(1)
grass_sound = mixer.Sound('assets/audio/grass-001.mp3')
grass_sound.set_volume(0.1)

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

#ANIMAZIONI PLAYER
# ANIMAZIONI PLAYER
PLAYER_FRAMES = {
    "down": [
        pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[DOWN]/walkd1.png'),
        pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[DOWN]/walkd2.png'),
        pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[DOWN]/walkd3.png'),
        pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[DOWN]/walkd4.png')
    ],
    "up": [
        pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[UP]/walku1.png'),
        pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[UP]/walku2.png'),
        pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[UP]/walku3.png'),
        pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[UP]/walku4.png')
    ],
    "left": [
        pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[LEFT]/walkl1.png'),
        pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[LEFT]/walkl2.png'),
        pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[LEFT]/walkl3.png'),
        pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[LEFT]/walkl4.png')
    ],
    "right": [
        pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[RIGHT]/walkr1.png'),
        pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[RIGHT]/walkr2.png'),
        pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[RIGHT]/walkr3.png'),
        pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[RIGHT]/walkr4.png')
    ]
}


# tile camminabili
WALKABLE_TILES = {1,2,3,4,5,6,11,12,13,14,15,16,17}

class Mondo():
    def __init__(self, matrice):
        self.matrice = matrice
        self.num_righe = len(matrice)
        self.num_colonne = len(matrice[0])
        self.lista_tiles = []
        self.lista_fontanelle = []
        self.lista_fiori = []  # Lista per i fiori

        # Definizione degli offset per il rendering isometrico
        self.offset_x = LUNGHEZZA // 2  # Centra la mappa orizzontalmente
        self.offset_y = 100  # Offset verticale per il posizionamento

        for riga in range(self.num_righe):
            for col in range(self.num_colonne):
                tile_val = self.matrice[riga][col]
                if tile_val in TILE_IMAGES:
                    screen_x, screen_y = self.tile_to_screen(col, riga)
                    if tile_val in [7, 8, 9, 10]:
                        screen_y -= 10
                    if tile_val == 18:
                        img_ground = pygame.transform.scale(TILE_IMAGES[3], (GRANDEZZA_TILES, GRANDEZZA_TILES))
                        rect_ground = img_ground.get_rect(topleft=(screen_x, screen_y))
                        self.lista_tiles.append((img_ground, rect_ground))
                        img_font = pygame.transform.scale(TILE_IMAGES[tile_val], (100, 100))
                        bottom_center = (screen_x + GRANDEZZA_TILES // 2, screen_y + GRANDEZZA_TILES // 2)
                        rect_font = img_font.get_rect(midbottom=bottom_center)
                        self.lista_fontanelle.append((img_font, rect_font))
                    else:
                        img = pygame.transform.scale(TILE_IMAGES[tile_val], (GRANDEZZA_TILES, GRANDEZZA_TILES))
                        rect = img.get_rect(topleft=(screen_x, screen_y))
                        self.lista_tiles.append((img, rect))
                        
                        # Generazione casuale dei fiori sui pezzi di erba
                        if tile_val in [3, 4, 5] and random.random() < 0.1:  # 30% di probabilità di spawn
                            img_fiore = pygame.transform.scale(TILE_IMAGES[6], (GRANDEZZA_TILES // 2, GRANDEZZA_TILES // 2))
                            rect_fiore = img_fiore.get_rect(center=(screen_x + GRANDEZZA_TILES // 2, screen_y + GRANDEZZA_TILES // 2))
                            self.lista_fiori.append((img_fiore, rect_fiore))


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
        for img, rect in self.lista_fiori:
            finestra.blit(img, rect)
    
    def trova_fontanella(self):
        for riga in range(self.num_righe):
            for col in range(self.num_colonne):
                if self.matrice[riga][col] == 18:
                    return col, riga  
        return None, None  # Restituisci un valore di default se non ci sono fontanelle


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
        img = pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[DOWN]/walkd1.png')
        self.image = pygame.transform.scale(img, (GRANDEZZA_TILES / 2, GRANDEZZA_TILES / 2))  # Raddoppia la dimensione
        self.rect = self.image.get_rect(midbottom=bottom_center)
        self.dest_x, self.dest_y = self.rect.topleft
        self.velocita = 8
        self.in_movimento = False
        self.fountain_x, self.fountain_y = mondo.trova_fontanella()
        self.thirsty = True
        self.direction = "down"  # AGGIUNTO: Imposta una direzione predefinita
        self.frame_index = 0  # AGGIUNTO: Tiene traccia dell'animazione
        self.frame_counter = 0  # AGGIUNTO: Conta i tick per l'animaziones

    def update(self):
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
            self.animate()
        else:
            self.in_movimento = False
            tasti = pygame.key.get_pressed()
            new_tile_x, new_tile_y = self.tile_x, self.tile_y
            if tasti[pygame.K_a]:
                new_tile_x -= 1
                self.direction = "left"
                self.in_movimento = True
            if tasti[pygame.K_d]:
                new_tile_x += 1
                self.direction = "right"
                self.in_movimento = True
            if tasti[pygame.K_w]:
                new_tile_y -= 1
                self.direction = "up"
                self.in_movimento = True
            if tasti[pygame.K_s]:
                new_tile_y += 1
                self.direction = "down"
                self.in_movimento = True
            if self.mondo.is_tile_walkable(new_tile_x, new_tile_y):
                self.tile_x, self.tile_y = new_tile_x, new_tile_y
                screen_x, screen_y = self.mondo.tile_to_screen(new_tile_x, new_tile_y)
                bottom_center = (screen_x + GRANDEZZA_TILES//2, screen_y + GRANDEZZA_TILES//2)
                self.dest_x = bottom_center[0] - self.rect.width // 2
                self.dest_y = bottom_center[1] - self.rect.height
                if self.in_movimento:  
                    grass_sound.play(maxtime=300, fade_ms=50)

        
        self.image = PLAYER_FRAMES[self.direction][self.frame_index]
        finestra.blit(self.image, self.rect)
    
    def animate(self):
        self.frame_counter += 1
        if self.frame_counter >= 15:  # Cambia frame ogni 5 tick
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(PLAYER_FRAMES[self.direction])

    def is_near_fountain(self):
        if self.fountain_x is None or self.fountain_y is None:
            return False

        adjacent_tiles = [
            (self.fountain_x, self.fountain_y - 2),
            (self.fountain_x, self.fountain_y + 1),
            (self.fountain_x - 2, self.fountain_y),
            (self.fountain_x + 1, self.fountain_y),
            (self.fountain_x - 1, self.fountain_y - 2),
            (self.fountain_x - 1, self.fountain_y + 1),
            (self.fountain_x - 2, self.fountain_y - 1),
            (self.fountain_x + 1, self.fountain_y - 1)
        ]
        return (self.tile_x, self.tile_y) in adjacent_tiles

    def controlla_fontanella(self):
        if self.is_near_fountain() and self.thirsty:
            print("Biv.")
            self.thirsty = False  
matrice = [
    [3, 7, 7, 7, 7, 7, 7, 3, 3, 3],
    [4, 8, 8, 8, 8, 8, 8, 3, 3, 3],
    [3, 3, 8, 8, 8, 8, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 19, 19, 4, 3, 3, 3],
    [3, 3, 4, 3, 19, 18, 4, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 4, 3, 3, 3, 4, 3],
    [3, 3, 3, 4, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]

mondo = Mondo(matrice)
player = Giocatore(0, 0, mondo)

clock = pygame.time.Clock()
run = True
mixer.music.play(loops=-1)

while run:
    finestra.fill((0, 0, 0))
    mondo.disegna()
    player.controlla_fontanella()
    player.update()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
    clock.tick(FPS)

pygame.quit()
