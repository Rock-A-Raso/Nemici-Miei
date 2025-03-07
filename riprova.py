# riprova.py
import pygame
from settings import LUNGHEZZA, ALTEZZA, BIANCO, ROSSO

class Try:
    def __init__(self, finestra):
        self.finestra = finestra
        self.font = pygame.font.Font("assets/Arcade.ttf", 40)
        self.font2 = pygame.font.Font("assets/DungeonFont.ttf", 50)
        self.button_rect = pygame.Rect(LUNGHEZZA // 2 - 100, ALTEZZA // 2 + 50, 200, 50)
        self.show_menu = True
        self.restart_requested = False  # Nuovo flag per restart

    def draw(self):
        if self.show_menu:
            title_text = self.font2.render("Nemici Miei", True, (0, 0, 0))
            self.finestra.blit(title_text, (LUNGHEZZA // 2 - title_text.get_width() // 2, ALTEZZA // 2 - 100))
            pygame.draw.rect(self.finestra, ROSSO, self.button_rect)
            button_text = self.font.render("Riprova", True, BIANCO)
            self.finestra.blit(button_text, (
                self.button_rect.x + (self.button_rect.width - button_text.get_width()) // 2,
                self.button_rect.y + (self.button_rect.height - button_text.get_height()) // 2
            ))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    # Imposta il flag di restart senza nascondere il pulsante
                    self.restart_requested = True

