import pygame
from pygame import mixer
from settings import LUNGHEZZA, ALTEZZA

grass_sounds = []  # Lista che conterrà i suoni dell'erba
TILE_IMAGES = {}
PLAYER_FRAMES = {}
PLAYER_IDLE = {}
ENEMY_FRAMES = {}

def load_assets():
    global grass_sounds, coin_sound, TILE_IMAGES, PLAYER_FRAMES, PLAYER_IDLE, ENEMY_FRAMES

    # carica la musica
    mixer.music.load('assets/audio/soundtrack.mp3')
    mixer.music.set_volume(0.1)

    sfondo = pygame.image.load('assets/[SFONDI]/bg.png')
    sfondo = pygame.transform.scale(sfondo, (LUNGHEZZA, ALTEZZA))
    
    # carica i suoni dell'erba 
    grass_sounds = [
        mixer.Sound('assets/audio/grass-001.mp3'),
    ]
    for sound in grass_sounds:
        sound.set_volume(0.01)

    # carica i souni della moneta
    coin_sound = mixer.Sound('assets/audio/coin.mp3')
    coin_sound.set_volume(0.2)

    # Carica le immagini dei tile
    TILE_IMAGES = {
        1: pygame.image.load('assets/[BLOCCHI]/tile_000.png'), #     terreno no erba
        2: pygame.image.load('assets/[BLOCCHI]/tile_003.png'), #     terreno no erba scuro
        3: pygame.image.load('assets/[BLOCCHI]/tile_022.png'), #     terreno erba
        4: pygame.image.load('assets/[BLOCCHI]/tile_023.png'), #     terreno erba 2 
        5: pygame.image.load('assets/[BLOCCHI]/tile_036.png'), #     terreno erba alta
        6: pygame.image.load('assets/[BLOCCHI]/tile_041.png'), #     fiori
        7: pygame.image.load('assets/[BLOCCHI]/tile_105.png'), #     mare onda a destra
        8: pygame.image.load('assets/[BLOCCHI]/tile_104.png'), #     mare no one
        9: pygame.image.load('assets/[BLOCCHI]/tile_109.png'), #     mare onda destra e sinistra
        10: pygame.image.load('assets/[BLOCCHI]/tile_106.png'), #    mare onda sinistra
        11: pygame.image.load('assets/[BLOCCHI]/tile_061.png'), #    ciottoli
        12: pygame.image.load('assets/[BLOCCHI]/tile_063.png'), #    ciottoli liscio
        13: pygame.image.load('assets/[BLOCCHI]/tile_064.png'), #    ciottoli pila
        14: pygame.image.load('assets/[BLOCCHI]/tile_077.png'), #    ciottoli in mare
        15: pygame.image.load('assets/[BLOCCHI]/tile_053.png'), #    ciottolo arancio
        16: pygame.image.load('assets/[BLOCCHI]/tile_049.png'), #    legno pila
        17: pygame.image.load('assets/[BLOCCHI]/tile_050.png'), #    legno singolo
        18: pygame.image.load('assets/[BLOCCHI]/fontanella.png'), #  autoesplicativo
        19: pygame.image.load('assets/[BLOCCHI]/tile_022.png'), #    void filler
        20: pygame.image.load('assets/[BLOCCHI]/tile_022.png'), #    void filler
        21: pygame.image.load('assets/[BLOCCHI]/tile_044.png'), #    fiori
    }

    # Carica le animazioni di movimento del giocatore
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

    # Carica le animazioni idle del giocatore
    PLAYER_IDLE = {
        "down": [
            pygame.image.load('assets/[PERSONAGGIO]/[IDLE]/[DOWN]/idle1.png'),
            pygame.image.load('assets/[PERSONAGGIO]/[IDLE]/[DOWN]/idle2.png')
        ],
        "up": [
            pygame.image.load('assets/[PERSONAGGIO]/[IDLE]/[UP]/idle1.png'),
            pygame.image.load('assets/[PERSONAGGIO]/[IDLE]/[UP]/idle2.png')
        ],
        "left": [
            pygame.image.load('assets/[PERSONAGGIO]/[IDLE]/[LEFT]/idle1.png')
        ],
        "right": [
            pygame.image.load('assets/[PERSONAGGIO]/[IDLE]/[RIGHT]/idle1.png')
        ],
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

