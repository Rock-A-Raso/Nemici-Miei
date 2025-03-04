import pygame
from pygame import mixer
from settings import LUNGHEZZA, ALTEZZA

grass_sounds = []
TILE_IMAGES = {}
PLAYER_FRAMES = {}
PLAYER_IDLE = {}
ENEMY_FRAMES = {}

def load_assets():
    global grass_sounds, coin_sound, TILE_IMAGES, PLAYER_FRAMES, PLAYER_IDLE, ENEMY_FRAMES
    mixer.music.load('assets/audio/soundtrack.mp3')
    mixer.music.set_volume(0.1)
    sfondo = pygame.image.load('assets/[SFONDI]/bg.png')
    sfondo = pygame.transform.scale(sfondo, (LUNGHEZZA, ALTEZZA))
    grass_sounds = [mixer.Sound('assets/audio/grass-001.mp3')]
    for sound in grass_sounds:
        sound.set_volume(0.01)
    coin_sound = mixer.Sound('assets/audio/coin.mp3')
    coin_sound.set_volume(0.2)
    TILE_IMAGES = {
        1: pygame.image.load('assets/[BLOCCHI]/tile_000.png'),    #     terreno no erba
        2: pygame.image.load('assets/[BLOCCHI]/tile_003.png'),    #     terreno no erba scuro
        3: pygame.image.load('assets/[BLOCCHI]/tile_022.png'),    #     terreno erba
        4: pygame.image.load('assets/[BLOCCHI]/tile_023.png'),    #     terreno erba 2 
        5: pygame.image.load('assets/[BLOCCHI]/tile_036.png'),    #     terreno erba alta
        6: pygame.image.load('assets/[BLOCCHI]/tile_041.png'),    #     fiori
        7: pygame.image.load('assets/[BLOCCHI]/tile_105.png'),    #     mare onda a destra
        8: pygame.image.load('assets/[BLOCCHI]/tile_104.png'),    #     mare no one
        9: pygame.image.load('assets/[BLOCCHI]/tile_109.png'),    #     mare onda destra e sinistra
        10: pygame.image.load('assets/[BLOCCHI]/tile_106.png'),   #    mare onda sinistra
        11: pygame.image.load('assets/[BLOCCHI]/tile_061.png'),   #    ciottoli
        12: pygame.image.load('assets/[BLOCCHI]/tile_063.png'),   #    ciottoli liscio
        13: pygame.image.load('assets/[BLOCCHI]/tile_064.png'),   #    ciottoli pila
        14: pygame.image.load('assets/[BLOCCHI]/tile_077.png'),   #    ciottoli in mare
        15: pygame.image.load('assets/[BLOCCHI]/tile_053.png'),   #    ciottolo arancio
        16: pygame.image.load('assets/[BLOCCHI]/tile_049.png'),   #    legno pila
        17: pygame.image.load('assets/[BLOCCHI]/tile_050.png'),   #    legno singolo
        18: pygame.image.load('assets/[BLOCCHI]/fontanella.png'), #  autoesplicativo
        19: pygame.image.load('assets/[BLOCCHI]/tile_022.png'),   #    void filler
        20: pygame.image.load('assets/[BLOCCHI]/tile_022.png'),   #    void filler
        21: pygame.image.load('assets/[BLOCCHI]/tile_044.png')    #    fiori
    }
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
    PLAYER_IDLE = {
        "down": [
            pygame.image.load('assets/[PERSONAGGIO]/[IDLE]/[DOWN]/idle1.png'),
            pygame.image.load('assets/[PERSONAGGIO]/[IDLE]/[DOWN]/idle2.png')
        ],
        "up": [
            pygame.image.load('assets/[PERSONAGGIO]/[IDLE]/[UP]/idle1.png'),
            pygame.image.load('assets/[PERSONAGGIO]/[IDLE]/[UP]/idle2.png')
        ],
        "left": [pygame.image.load('assets/[PERSONAGGIO]/[IDLE]/[LEFT]/idle1.png')],
        "right": [pygame.image.load('assets/[PERSONAGGIO]/[IDLE]/[RIGHT]/idle1.png')]
    }
    ENEMY_FRAMES = {
        "down": [
            pygame.image.load('assets/[MOBS]/[BAT]/[DOWN]/1.png'),
            pygame.image.load('assets/[MOBS]/[BAT]/[DOWN]/2.png'),
            pygame.image.load('assets/[MOBS]/[BAT]/[DOWN]/3.png')
        ],
        "up": [
            pygame.image.load('assets/[MOBS]/[BAT]/[UP]/1.png'),
            pygame.image.load('assets/[MOBS]/[BAT]/[UP]/2.png'),
            pygame.image.load('assets/[MOBS]/[BAT]/[UP]/3.png')
        ],
        "left": [
            pygame.image.load('assets/[MOBS]/[BAT]/[LEFT]/1.png'),
            pygame.image.load('assets/[MOBS]/[BAT]/[LEFT]/2.png'),
            pygame.image.load('assets/[MOBS]/[BAT]/[LEFT]/3.png')
        ],
        "right": [
            pygame.image.load('assets/[MOBS]/[BAT]/[LEFT]/1.png'),
            pygame.image.load('assets/[MOBS]/[BAT]/[RIGHT]/2.png'),
            pygame.image.load('assets/[MOBS]/[BAT]/[RIGHT]/3.png')
        ]
    }

livello_1 = [
    [3, 7, 7, 7, 7, 7, 7, 20, 20, 20],
    [4, 8, 8, 8, 8, 8, 8, 3, 3, 3],
    [3, 3, 8, 8, 8, 8, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 19, 19, 4, 3, 3, 3],
    [3, 3, 4, 3, 19, 18, 4, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 4, 3, 3, 3, 4, 3],
    [3, 3, 3, 4, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 19]
]

livello_2 = [
    [11, 11, 11, 11, 11, 11, 11, 11, 11, 11],  
    [12, 11, 11, 11, 11, 11, 11, 11, 11, 11],
    [11, 11, 11, 11, 11, 11, 11, 11, 11, 11], 
    [11, 11, 11, 11, 11, 11, 11, 11, 11, 11],  
    [11, 11, 11, 11, 11, 11, 12, 11, 11, 11],  
    [11, 11, 12, 11, 11, 11, 12, 11, 11, 11], 
    [11, 11, 11, 11, 11, 11, 11, 11, 11, 11], 
    [11, 11, 11, 11, 12, 11, 11, 11, 12, 11],  
    [11, 11, 11, 12, 11, 11, 11, 11, 11, 11], 
    [11, 11, 11, 11, 11, 11, 11, 11, 11, 11]
]


livelli = {1: livello_1, 2: livello_2}
