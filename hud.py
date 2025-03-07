import pygame
import assets
from world import Mondo
from player import Giocatore
from npc import Npc
from settings import ALTEZZA, LUNGHEZZA, GRIGIO, BIANCO

class HUD:
    def __init__(self, finestra, player, npc, boss, mondo):
        self.start(finestra, player, npc, boss, mondo)
    
    def start(self, finestra, player, npc, boss, mondo):
        self.finestra = finestra
        self.player = player
        self.npc = npc
        self.boss = boss
        self.mondo = mondo
        self.font = pygame.font.Font("assets/Arcade.ttf", 30)
        self.font2 = pygame.font.Font("assets/DungeonFont.ttf", 25)
        self.health_icon = pygame.image.load("assets/[ITEMS]/health.png")
        self.monete_icon = pygame.image.load("assets/[ITEMS]/coin.gif")
        self.health_icon = pygame.transform.scale(self.health_icon, (32, 32))
        self.monete_icon = pygame.transform.scale(self.monete_icon, (32, 32))
        self.dialogue_index = 1
        self.giaparlato = False

    def draw(self, events):
        hud_rect = pygame.Rect(0, ALTEZZA - 100, LUNGHEZZA, 100)
        pygame.draw.rect(self.finestra, GRIGIO, hud_rect)
        
        self.finestra.blit(self.health_icon, (20, ALTEZZA - 75))
        health_text = self.font2.render(f"Salute: {self.player.vita} / {self.player.vita_max}", True, BIANCO)
        self.finestra.blit(health_text, (60, ALTEZZA - 65))

        self.finestra.blit(self.monete_icon, (20, ALTEZZA - 35))
        monete_text = self.font2.render(f"Monete: {self.player.monete}", True, BIANCO)
        self.finestra.blit(monete_text, (60, ALTEZZA - 25))

        level_text = self.font2.render(f"Livello: {self.player.level}", True, BIANCO)
        self.finestra.blit(level_text, (250, ALTEZZA - 65))

        if self.mondo.livello_id == 2:
            boss_health_text = self.font2.render(f"Salute Boss: {int(self.boss.hp)}", True, BIANCO)
            self.finestra.blit(boss_health_text, (450, ALTEZZA - 65))
        self.handle_dialogue(events)

        if (self.player.is_near_fountain() and self.player.thirsty and self.giaparlato) or (self.player.is_near_npc(self.npc) and not self.npc.parlando) and not self.giaparlato:
            interazioni_text = self.font.render("Premi (E) per interagire.", True, BIANCO)
            self.finestra.blit(interazioni_text, (500, ALTEZZA - 70))

    def render_multiline_text(self, text, pos, font, color):
        x, y = pos
        for line in text.split('\n'):
            rendered_line = font.render(line, True, color)
            self.finestra.blit(rendered_line, (x, y))
            y = ALTEZZA - 30
            x = 500

    def handle_dialogue(self, events):
        if not self.player.is_near_npc(self.npc):
            self.npc.parlando = False
            self.dialogue_index = 1
            return

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e and not self.giaparlato:
                if self.player.is_near_npc(self.npc):
                    if not self.npc.parlando:
                        self.npc.parlando = True
                        self.dialogue_index = 1  
                    else:
                        self.dialogue_index += 1
                        if self.dialogue_index > len(assets.STRING_DIALOGUE):
                            self.npc.parlando = False
                            self.giaparlato = True

        if self.npc.parlando:
            text = assets.STRING_DIALOGUE.get(str(self.dialogue_index), "")
            self.render_multiline_text(text, (500, ALTEZZA - 70), self.font, BIANCO)