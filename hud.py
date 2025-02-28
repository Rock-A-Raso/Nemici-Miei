import pygame
from settings import LUNGHEZZA, ALTEZZA

class HUD:
    def __init__(self, finestra, player):
        self.finestra = finestra
        self.player = player
        self.font = pygame.font.Font("assets/DungeonFont.ttf", 24)  # Usa il font DungeonFont
        # Creiamo delle superfici per le icone (oppure carica le immagini da file)
        self.health_icon = pygame.Surface((32, 32))
        self.health_icon.fill((255, 0, 0))  # Rosso per la salute
        self.monete_icon = pygame.Surface((32, 32))
        self.monete_icon.fill((0, 0, 255))    # Blu per le monete

    def draw(self):
        # Disegna uno sfondo per la HUD nella parte bassa della finestra
        hud_rect = pygame.Rect(0, ALTEZZA - 100, LUNGHEZZA, 100)
        pygame.draw.rect(self.finestra, (50, 50, 50), hud_rect)

        # Salute
        self.finestra.blit(self.health_icon, (20, ALTEZZA - 80))
        health_text = self.font.render(f"Salute: {self.player.vita} / {self.player.vita_max}", True, (255,255,255))
        self.finestra.blit(health_text, (60, ALTEZZA - 70))
        
        # Monete
        self.finestra.blit(self.monete_icon, (20, ALTEZZA - 40))
        monete_text = self.font.render(f"Monete: {self.player.monete}", True, (255,255,255))
        self.finestra.blit(monete_text, (60, ALTEZZA - 30))
        
        # Livello ed esperienza
        level_text = self.font.render(f"Livello: {self.player.level}", True, (255,255,255))
        self.finestra.blit(level_text, (250, ALTEZZA - 70))
        
        exp_text = self.font.render(f"EXP: {self.player.exp}/{self.player.next_level_exp}", True, (255,255,255))
        self.finestra.blit(exp_text, (250, ALTEZZA - 30))
