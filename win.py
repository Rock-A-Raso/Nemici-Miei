import pygame
import assets
from settings import BIANCO, ROSSO, LUNGHEZZA, ALTEZZA

class Win:
    def __init__(self, finestra):
        self.finestra = finestra
        self.font = pygame.font.Font("assets/Arcade.ttf", 40)
        self.font2 = pygame.font.Font("assets/DungeonFont.ttf", 50)
        self.font3 = pygame.font.Font("assets/Arcade.ttf", 30)
        # Non servono più i bottoni, in quanto l'animazione parte subito
        self.show_menu = False
        self.show_credits = True

        # Variabili per l'animazione dei crediti
        # Partiamo con un offset iniziale negativo per far partire le righe fuori dallo schermo (in alto)
        self.credit_offset = -100  
        self.credit_speed = 1  # Velocità di scorrimento in pixel per frame
        self.line_spacing = 40  # Spazio verticale tra le righe

        self.credits_lines = [
            "Sviluppato da: Rock A' Raso GAME LLC",
            "Allocca Vincenzo,",
            "Cerciello Antonio,",
            "Cestiè Augusto",
            "Pellegrino Andrea,",
            "Prisco Carmine,",
            "Raffaele Sdino",
            "",
            "Grazie per aver giocato!"
        ]

    def update(self):
        # Aggiorna la posizione verticale dei crediti
        if self.show_credits:
            self.credit_offset += self.credit_speed
        self.draw()

    def draw(self):
        # Disegna lo sfondo
        self.finestra.blit(assets.SFONDO_IMAGES[3], (0, 0))
        
        if self.show_credits:
            # Titolo fisso in alto (opzionale)
            credits_title = self.font2.render("Crediti", True, ROSSO)
            self.finestra.blit(credits_title, (LUNGHEZZA // 2 - credits_title.get_width() // 2, 20))
            
            # Disegna ogni riga dei crediti con la posizione verticale animata
            for i, line in enumerate(self.credits_lines):
                credit_text = self.font3.render(line, True, BIANCO)
                # La posizione y viene calcolata in base all'offset corrente, allo spacing e ad un offset aggiuntivo per non sovrapporsi al titolo
                y = self.credit_offset + i * self.line_spacing + 100
                self.finestra.blit(credit_text, (LUNGHEZZA // 2 - credit_text.get_width() // 2, y))
