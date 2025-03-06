import pygame
import assets
from world import Mondo
from player import Giocatore
from npc import Npc
from settings import LUNGHEZZA, ALTEZZA
from settings import *

class Menu:
    def __init__(self, finestra):
        self.finestra = finestra
        self.font = pygame.font.Font("assets/Arcade.ttf", 40)
        self.font2 = pygame.font.Font("assets/DungeonFont.ttf", 50)
        self.button_rect = pygame.Rect(LUNGHEZZA // 2 - 100, ALTEZZA // 2 + 50, 200, 50)
        self.show_menu = True

    def draw(self):
        if self.show_menu:
            self.finestra.fill(GRIGIO)
            title_text = self.font2.render("Nemici Miei", True, BIANCO)
            self.finestra.blit(title_text, (LUNGHEZZA // 2 - title_text.get_width() // 2, ALTEZZA // 2 - 100))
            
            pygame.draw.rect(self.finestra, ROSSO, self.button_rect)
            button_text = self.font.render("START", True, BIANCO)
            self.finestra.blit(button_text, (self.button_rect.x + (self.button_rect.width - button_text.get_width()) // 2, self.button_rect.y + (self.button_rect.height - button_text.get_height()) // 2))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    self.show_menu = False