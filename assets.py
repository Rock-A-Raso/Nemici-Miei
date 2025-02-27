# assets.py
import pygame
from pygame import mixer

grass_sounds = []  # Lista che conterrà i suoni dell'erba
TILE_IMAGES = {}
PLAYER_FRAMES = {}
PLAYER_IDLE = {}

def load_assets():
    global grass_sounds, TILE_IMAGES, PLAYER_FRAMES, PLAYER_IDLE

    # Carica la musica di sottofondo
    mixer.music.load('assets/audio/Chill House.mp3')
    mixer.music.set_volume(0.1)
    
    # Carica i suoni dell'erba (settiamo il volume per ciascuno)
    grass_sounds = [
        mixer.Sound('assets/audio/grass-001.mp3'),
        mixer.Sound('assets/audio/grass-002.mp3'),
        mixer.Sound('assets/audio/grass-003.mp3'),
        mixer.Sound('assets/audio/grass-004.mp3')
    ]
    for sound in grass_sounds:
        sound.set_volume(0.01)

    # Carica le immagini dei tile
    TILE_IMAGES = {
        1: pygame.image.load('assets/[BLOCCHI]/tile_000.png'),
        2: pygame.image.load('assets/[BLOCCHI]/tile_003.png'),
        3: pygame.image.load('assets/[BLOCCHI]/tile_022.png'),
        4: pygame.image.load('assets/[BLOCCHI]/tile_023.png'),
        5: pygame.image.load('assets/[BLOCCHI]/tile_036.png'),
        6: pygame.image.load('assets/[BLOCCHI]/tile_044.png'),
        7: pygame.image.load('assets/[BLOCCHI]/tile_105.png'),
        8: pygame.image.load('assets/[BLOCCHI]/tile_104.png'),
        9: pygame.image.load('assets/[BLOCCHI]/tile_109.png'),
        10: pygame.image.load('assets/[BLOCCHI]/tile_106.png'),
        11: pygame.image.load('assets/[BLOCCHI]/tile_061.png'),
        12: pygame.image.load('assets/[BLOCCHI]/tile_063.png'),
        13: pygame.image.load('assets/[BLOCCHI]/tile_064.png'),
        14: pygame.image.load('assets/[BLOCCHI]/tile_077.png'),
        15: pygame.image.load('assets/[BLOCCHI]/tile_053.png'),
        16: pygame.image.load('assets/[BLOCCHI]/tile_049.png'),
        17: pygame.image.load('assets/[BLOCCHI]/tile_050.png'),
        18: pygame.image.load('assets/[BLOCCHI]/fontanella.png'),
        19: pygame.image.load('assets/[BLOCCHI]/tile_022.png'),
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
            pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[LEFT]/walkl1.png'),
        ],
        "right": [
            pygame.image.load('assets/[PERSONAGGIO]/[MOVEMENT]/[RIGHT]/walkr1.png'),
        ],
    }
