import pygame
import assets
from settings import BIANCO, ROSSO, LUNGHEZZA, ALTEZZA

class Win:
    def __init__(self, finestra):
        self.finestra = finestra
        self.font = pygame.font.Font("assets/Arcade.ttf", 40)
        self.font2 = pygame.font.Font("assets/DungeonFont.ttf", 50)
        self.font3 = pygame.font.Font("assets/Arcade.ttf", 30)
        self.show_credits = True

        self.credit_offset = -500  
        self.credit_speed = 1  
        self.line_spacing = 40  

        self.credits_lines = [
            "Sviluppato da: Rock A' Raso GAME LLC",
            "Allocca Vincenzo,",
            "Cerciello Antonio,",
            "Cestie' Augusto",
            "Pellegrino Andrea,",
            "Prisco Carmine,",
            "Sdino Raffaele",
            "",
            "Grazie per aver giocato!",
            "",
            "HAI VINTO!"
        ]

    def update(self):
        if self.show_credits:
            self.credit_offset += self.credit_speed
        self.draw()

    def draw(self):
        self.finestra.fill((0, 0, 0))
        
        if self.show_credits:
            credits_title = self.font2.render("Crediti", True, ROSSO)
            self.finestra.blit(credits_title, (LUNGHEZZA // 2 - credits_title.get_width() // 2, 20))
            
            for i, line in enumerate(self.credits_lines):
                credit_text = self.font3.render(line, True, BIANCO)
                y = self.credit_offset + i * self.line_spacing + 100
                self.finestra.blit(credit_text, (LUNGHEZZA // 2 - credit_text.get_width() // 2, y))
