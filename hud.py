import pygame
from player import Giocatore
from npc import Npc
from settings import LUNGHEZZA, ALTEZZA

ROSSO = (255, 0, 0)
BLU = (0, 0, 255)
BIANCO = (255, 255, 255)
GRIGIO = (50, 50, 50)
TRASPARENTE = (0, 0, 0, 128)

class HUD:
    def __init__(self, finestra, player, npc):
        self.finestra = finestra
        self.player = player
        self.npc = npc
        self.font = pygame.font.Font("assets/DungeonFont.ttf", 24)
        self.health_icon = pygame.image.load("assets/[ITEMS]/health.png")
        self.monete_icon = pygame.image.load("assets/[ITEMS]/coin.gif")
        self.health_icon = pygame.transform.scale(self.health_icon, (32, 32))
        self.monete_icon = pygame.transform.scale(self.monete_icon, (32, 32))

    def draw(self):
        hud_rect = pygame.Rect(0, ALTEZZA - 100, LUNGHEZZA, 100)
        pygame.draw.rect(self.finestra, GRIGIO, hud_rect)
        
        self.finestra.blit(self.health_icon, (20, ALTEZZA - 80))
        health_text = self.font.render(f"Salute: {self.player.vita} / {self.player.vita_max}", True, BIANCO)
        self.finestra.blit(health_text, (60, ALTEZZA - 70))

        self.finestra.blit(self.monete_icon, (20, ALTEZZA - 40))
        monete_text = self.font.render(f"Monete: {self.player.monete}", True, BIANCO)
        self.finestra.blit(monete_text, (60, ALTEZZA - 30))

        level_text = self.font.render(f"Livello: {self.player.level}", True, BIANCO)
        self.finestra.blit(level_text, (250, ALTEZZA - 70))

        exp_text = self.font.render(f"EXP: {self.player.exp}/{self.player.next_level_exp}", True, BIANCO)
        self.finestra.blit(exp_text, (250, ALTEZZA - 30))

        keys = pygame.key.get_pressed()
        if self.player.is_near_npc(self.npc):
            self.npc.dialogo()
            if self.npc.parlando:
                dialogue_text = self.font.render(f"{self.npc.nome}: Come se fosse Antani? Prefettura?", True, BIANCO)
                self.finestra.blit(dialogue_text, (500, ALTEZZA - 30))
        else:
            self.npc.parlando = False
