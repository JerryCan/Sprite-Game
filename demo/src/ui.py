# UI klasse voor interface elementen
import pygame
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, GREEN, BLUE

class UI:
    def __init__(self):
        # Laad een standaard font
        self.font = pygame.font.SysFont(None, 24)
        self.header_font = pygame.font.SysFont(None, 32)
        
        # Dialoog attributen
        self.current_dialogue = ""
        self.dialogue_finished = False
        self.dialogue_speaker = ""
        
        # Menu attributen
        self.menu_options = ["Items", "Skills", "Status", "Save"]
        self.selected_option = 0
        
        # Status attributen
        self.showing_status = False
        self.status_categories = ["Physical", "Mental", "Spiritual"]
        self.selected_category = 0
    
    def handle_dialogue_event(self, event):
        """Verwerk events in dialoog state"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                print(f"Space/Enter pressed in dialogue, setting dialogue_finished to True")
                self.dialogue_finished = True
                # Voeg een korte vertraging toe
                pygame.time.delay(200)
    
    def handle_menu_event(self, event):
        """Verwerk events in menu state"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Voer menu optie uit
                selected = self.menu_options[self.selected_option]
                if selected == "Status":
                    self.showing_status = True
            elif event.key == pygame.K_ESCAPE:
                # Sluit menu en status
                self.showing_status = False
                return True  # Geef signaal om menu te sluiten
        return False
    
    def start_dialogue(self, dialogue, speaker=""):
        """Start een nieuwe dialoog"""
        self.current_dialogue = dialogue
        self.dialogue_speaker = speaker
        self.dialogue_finished = False
    
    def is_dialogue_finished(self):
        """Controleer of huidige dialoog is afgesloten"""
        return self.dialogue_finished
    
    def render_dialogue(self, screen):
        """Render dialoogvenster en tekst"""
        # Maak dialoogvenster
        dialogue_box = pygame.Surface((SCREEN_WIDTH - 100, 150))
        dialogue_box.fill(WHITE)
        dialogue_box.set_alpha(230)  # Licht transparant
        
        # Positioneer onderaan scherm
        box_x = 50
        box_y = SCREEN_HEIGHT - 180
        
        # Render op scherm
        screen.blit(dialogue_box, (box_x, box_y))
        
        # Render speakernaam indien aanwezig
        if self.dialogue_speaker:
            speaker_text = self.header_font.render(self.dialogue_speaker, True, (50, 50, 150))
            screen.blit(speaker_text, (box_x + 20, box_y + 15))
            text_y_start = box_y + 50  # Tekst wat lager beginnen
        else:
            text_y_start = box_y + 20
            
        # Render dialoogtekst
        self.render_text_multiline(screen, self.current_dialogue, box_x + 20, text_y_start)
        
        # Render 'doorgaan' prompt
        continue_text = self.font.render("Druk op SPATIE om door te gaan...", True, BLACK)
        screen.blit(continue_text, (box_x + 20, box_y + 110))
    
    def render_menu(self, screen, player):
        """Render game menu"""
        # Maak menu achtergrond
        menu_bg = pygame.Surface((200, SCREEN_HEIGHT - 100))
        menu_bg.fill(WHITE)
        menu_bg.set_alpha(230)
        
        # Positioneer rechts op scherm
        screen.blit(menu_bg, (SCREEN_WIDTH - 220, 50))
        
        # Render titel
        title_text = self.header_font.render("Menu", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH - 200, 60))
        
        # Render opties
        for i, option in enumerate(self.menu_options):
            if i == self.selected_option:
                color = RED  # Geselecteerde optie
            else:
                color = BLACK
            
            option_text = self.font.render(option, True, color)
            screen.blit(option_text, (SCREEN_WIDTH - 200, 100 + i * 40))
        
        # Indien status wordt getoond
        if self.showing_status and self.menu_options[self.selected_option] == "Status":
            self.render_status(screen, player)
    
    def render_status(self, screen, player):
        """Render status scherm met Tri-Sharira statistieken"""
        # Maak status venster
        status_width = 400
        status_height = 350
        status_bg = pygame.Surface((status_width, status_height))
        status_bg.fill(WHITE)
        
        # Positioneer in midden van scherm
        status_x = SCREEN_WIDTH // 2 - status_width // 2
        status_y = SCREEN_HEIGHT // 2 - status_height // 2
        
        screen.blit(status_bg, (status_x, status_y))
        
        # Render titel
        title_text = self.header_font.render("Character Status", True, BLACK)
        screen.blit(title_text, (status_x + 20, status_y + 20))
        
        # Render basis stats
        base_stats_text = self.font.render(f"HP: {player.stats['hp']}/{player.stats['max_hp']}   Prana: {player.stats['prana']}/{player.stats['max_prana']}", True, BLACK)
        screen.blit(base_stats_text, (status_x + 20, status_y + 60))
        
        # Render categorietabs
        for i, category in enumerate(self.status_categories):
            if i == self.selected_category:
                color = (50, 50, 150)  # Geselecteerde categorie
                pygame.draw.rect(screen, color, (status_x + i * 133, status_y + 90, 133, 30))
                tab_text = self.font.render(category, True, WHITE)
            else:
                color = (200, 200, 200)  # Niet-geselecteerde categorie
                pygame.draw.rect(screen, color, (status_x + i * 133, status_y + 90, 133, 30))
                tab_text = self.font.render(category, True, BLACK)
            
            screen.blit(tab_text, (status_x + i * 133 + 20, status_y + 95))
        
        # Render stats op basis van geselecteerde categorie
        if self.selected_category == 0:  # Fysiek
            stats_to_show = ["strength", "endurance", "defense", "speed"]
            stat_colors = [(220, 50, 50), (180, 80, 80), (150, 70, 70), (200, 60, 60)]
        elif self.selected_category == 1:  # Mentaal
            stats_to_show = ["focus", "insight", "willpower", "memory"]
            stat_colors = [(50, 50, 220), (70, 70, 180), (60, 60, 200), (80, 80, 150)]
        else:  # Spiritueel
            stats_to_show = ["intuition", "devotion", "karma"]
            stat_colors = [(100, 50, 200), (150, 50, 180), (180, 50, 150)]
        
        # Render stats met balken
        for i, stat in enumerate(stats_to_show):
            stat_name = stat.capitalize()
            stat_value = player.stats[stat]
            
            # Teken label
            stat_text = self.font.render(f"{stat_name}: {stat_value}", True, BLACK)
            screen.blit(stat_text, (status_x + 30, status_y + 140 + i * 40))
            
            # Teken statbar (max 100 punten voor stats in deze demo)
            max_bar_width = 200
            bar_width = int((stat_value / 20) * max_bar_width)  # Schaal naar maximaal 20 voor demo
            
            pygame.draw.rect(screen, (200, 200, 200), (status_x + 170, status_y + 140 + i * 40, max_bar_width, 20))
            pygame.draw.rect(screen, stat_colors[i], (status_x + 170, status_y + 140 + i * 40, bar_width, 20))
        
        # Teken instructie
        instruction_text = self.font.render("Gebruik pijltjestoetsen om categorieën te wisselen", True, BLACK)
        screen.blit(instruction_text, (status_x + 20, status_y + status_height - 40))
    
    def render_text_multiline(self, screen, text, x, y):
        """Render tekst over meerdere regels"""
        # Split tekst in woorden en maak regels die in het dialoogvenster passen
        words = text.split(' ')
        lines = []
        line = ""
        for word in words:
            test_line = line + word + " "
            # Controleer of deze regel niet te lang is
            if self.font.size(test_line)[0] < SCREEN_WIDTH - 140:
                line = test_line
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)  # Voeg laatste regel toe
        
        # Render elke regel
        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, BLACK)
            screen.blit(text_surface, (x, y + i * 24))  # 24px regelafstand
    
    def render_hud(self, screen, player):
        """Render heads-up display met speler stats"""
        # Teken HP en Prana balken
        hp_text = self.font.render(f"HP: {player.stats['hp']}/{player.stats['max_hp']}", True, WHITE)
        prana_text = self.font.render(f"Prana: {player.stats['prana']}/{player.stats['max_prana']}", True, WHITE)
        
        # Plaats in linkerbovenhoek met donkere achtergrond
        hp_bg = pygame.Surface((150, 25))
        hp_bg.fill((0, 0, 0))
        hp_bg.set_alpha(180)
        screen.blit(hp_bg, (10, 10))
        screen.blit(hp_text, (15, 15))
        
        prana_bg = pygame.Surface((150, 25))
        prana_bg.fill((0, 0, 0))
        prana_bg.set_alpha(180)
        screen.blit(prana_bg, (10, 40))
        screen.blit(prana_text, (15, 45))
        
        # Indicator voor huidige locatie
        location_bg = pygame.Surface((200, 25))
        location_bg.fill((0, 0, 0))
        location_bg.set_alpha(180)
        screen.blit(location_bg, (SCREEN_WIDTH - 210, 10))
        
        location_text = self.font.render("Chandrapur Village", True, WHITE)
        screen.blit(location_text, (SCREEN_WIDTH - 200, 15))
