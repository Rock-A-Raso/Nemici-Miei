import pygame
from settings import LUNGHEZZA, ALTEZZA

# Costanti per i colori
ROSSO = (255, 0, 0)
BLU = (0, 0, 255)
BIANCO = (255, 255, 255)
GRIGIO = (50, 50, 50)
TRASPARENTE = (0, 0, 0, 128)

class HUD:
    def __init__(self, finestra, player):
        self.finestra = finestra
        self.player = player
        self.font = pygame.font.Font("assets/DungeonFont.ttf", 24) 
        
        # Carica le immagini per le icone (esempio)
        self.health_icon = pygame.image.load("assets/[ITEMS]/health.png") 
        self.monete_icon = pygame.image.load("assets/[ITEMS]/coin.gif")    

        # Ridimensiona le icone (opzionale)
        self.health_icon = pygame.transform.scale(self.health_icon, (32, 32))
        self.monete_icon = pygame.transform.scale(self.monete_icon, (32, 32))

    def draw(self):
        # Disegna uno sfondo per la HUD nella parte bassa della finestra
        hud_rect = pygame.Rect(0, ALTEZZA - 100, LUNGHEZZA, 100)
        pygame.draw.rect(self.finestra, GRIGIO, hud_rect)

        # Salute
        self.finestra.blit(self.health_icon, (20, ALTEZZA - 80))
        health_text = self.font.render(f"Salute: {self.player.vita} / {self.player.vita_max}", True, BIANCO)
        
        # Aggiungi uno sfondo semi-trasparente per il testo
        health_rect = health_text.get_rect(topleft=(60, ALTEZZA - 70))
        pygame.draw.rect(self.finestra, GRIGIO, health_rect)
        self.finestra.blit(health_text, (60, ALTEZZA - 70))
        
        # Monete
        self.finestra.blit(self.monete_icon, (20, ALTEZZA - 40))
        monete_text = self.font.render(f"Monete: {self.player.monete}", True, BIANCO)
        monete_rect = monete_text.get_rect(topleft=(60, ALTEZZA - 30))
        pygame.draw.rect(self.finestra, GRIGIO, monete_rect)
        self.finestra.blit(monete_text, (60, ALTEZZA - 30))
        
        # Livello ed esperienza
        level_text = self.font.render(f"Livello: {self.player.level}", True, BIANCO)
        self.finestra.blit(level_text, (250, ALTEZZA - 70))
        
        exp_text = self.font.render(f"EXP: {self.player.exp}/{self.player.next_level_exp}", True, BIANCO)
        self.finestra.blit(exp_text, (250, ALTEZZA - 30))