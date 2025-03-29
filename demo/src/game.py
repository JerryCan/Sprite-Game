# Game klasse - hoofdklasse voor de game logica en state management
import pygame
import random
import os
from src.config import STATE_EXPLORE, STATE_DIALOGUE, STATE_COMBAT, STATE_MENU
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from src.player import Player
from src.world import World
from src.ui import UI
from src.combat import CombatSystem, Enemy

# Hulpfunctie om mapbestanden te vinden
def find_map_file(map_filename):
    """
    Zoekt een mapbestand in verschillende mogelijke locaties
    
    Args:
        map_filename (str): Naam van het mapbestand
    
    Returns:
        str: Volledig pad naar het mapbestand of None als niet gevonden
    """
    # Mogelijke locaties om te zoeken
    possible_locations = [
        os.path.join("Maps", map_filename),                  # ./Maps/
        os.path.join("..", "Maps", map_filename),            # ../Maps/
        os.path.join(".", map_filename),                     # ./
        os.path.join("..", map_filename),                    # ../
        os.path.join(os.path.dirname(__file__), "..", "..", "Maps", map_filename), # Vanaf script locatie
        map_filename                                         # Direct pad
    ]
    
    # Controleer elke mogelijke locatie
    for location in possible_locations:
        if os.path.exists(location):
            print(f"Map bestand gevonden: {location}")
            return os.path.abspath(location)
    
    # Niet gevonden
    print(f"WAARSCHUWING: Map bestand niet gevonden: {map_filename}")
    print(f"Gezocht in: {possible_locations}")
    return None

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = STATE_EXPLORE
        
        # Bepaal pad naar mapbestand
        map_filename = "Map-1-v0.1.map"
        map_file = find_map_file(map_filename)
        
        # Print info voor debugging
        print(f"Proberen map te laden: {map_file}")
        
        # Initialiseer componenten
        self.world = World(map_file)
        self.player = Player(400, 300)  # Start in het midden
        self.ui = UI()
        self.combat_system = CombatSystem()
        
        # Camera zal op speler focussen
        self.camera_offset_x = 0
        self.camera_offset_y = 0
        
        # Combat demo tegenstander
        self.demo_enemies = [
            Enemy("Wild Tiger", 2, "physical"),
            Enemy("Mind Wraith", 2, "mental"),
            Enemy("Spirit Fox", 2, "spiritual")
        ]
        
        # Voor demo: timer voor willekeurige encounters
        self.encounter_timer = 0
        self.encounter_threshold = 300  # ~5 seconden bij 60 FPS
        self.encounter_chance = 0.2  # 20% kans bij bereiken van threshold
        
        # Help text voor eerste opstart
        self.show_help = True
        self.help_timer = 300  # ~5 seconden tonen bij start
    
    def handle_event(self, event):
        """Verwerk pygame events op basis van huidige state"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
            # Toggle help met H toets
            self.show_help = not self.show_help
            if self.show_help:
                self.help_timer = 300
        
        if self.state == STATE_EXPLORE:
            # In verkenmode verwerkt speler beweging
            self.player.handle_event(event)
            
            # Check voor menu openen (ESC)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = STATE_MENU
                
        elif self.state == STATE_DIALOGUE:
            # In dialoog mode verwerkt UI de events
            self.ui.handle_dialogue_event(event)
            if self.ui.is_dialogue_finished():
                self.state = STATE_EXPLORE
                print("Dialogue finished, returning to explore state")
                
        elif self.state == STATE_COMBAT:
            # In combat mode verwerkt combat systeem events
            combat_done = self.combat_system.handle_event(event)
            if combat_done:
                self.state = STATE_EXPLORE
                
        elif self.state == STATE_MENU:
            # In menu mode verwerkt UI events
            close_menu = self.ui.handle_menu_event(event)
            if close_menu or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.state = STATE_EXPLORE
    
    def update(self):
        """Update game state"""
        if self.state == STATE_EXPLORE:
            # Update help timer
            if self.show_help and self.help_timer > 0:
                self.help_timer -= 1
                if self.help_timer <= 0:
                    self.show_help = False
            
            # Update speler en wereld
            self.player.update(self.world.obstacles)
            self.world.update()
            self.update_camera()
            
            # Check voor interacties
            self.check_interactions()
            
            # Update encounter timer voor willekeurige gevechten (alleen in demo)
            self.update_encounter_timer()
            
        elif self.state == STATE_COMBAT:
            # Update combat systeem
            self.combat_system.update()
            
            # Check of combat is afgelopen
            if self.combat_system.is_combat_over():
                # Process resultaat (XP, items, etc. in volledige game)
                if self.combat_system.get_victory_state():
                    # Bij overwinning zou je hier XP, items, etc. kunnen geven
                    pass
    
    def render(self):
        """Render de huidige game state"""
        if self.state == STATE_EXPLORE or self.state == STATE_DIALOGUE:
            # Render wereld en speler
            self.world.render(self.screen, self.camera_offset_x, self.camera_offset_y)
            self.player.render(self.screen, self.camera_offset_x, self.camera_offset_y)
            
            # Render HUD
            self.ui.render_hud(self.screen, self.player)
            
            # Render coördinaten
            self.render_coordinates()
            
            # Help text tonen indien nodig
            if self.show_help:
                self.render_help_text()
            
            # In dialoog mode, render dialoogvenster bovenop
            if self.state == STATE_DIALOGUE:
                self.ui.render_dialogue(self.screen)
                
        elif self.state == STATE_COMBAT:
            # Render combat scene
            self.combat_system.render(self.screen)
            
        elif self.state == STATE_MENU:
            # Render wereld en speler op achtergrond
            self.world.render(self.screen, self.camera_offset_x, self.camera_offset_y)
            self.player.render(self.screen, self.camera_offset_x, self.camera_offset_y)
            
            # Render menu bovenop
            self.ui.render_menu(self.screen, self.player)
    
    def render_coordinates(self):
        """Render de coördinaten van de speler"""
        # Bereken huidige tegel coördinaten (x, y)
        tile_x = self.player.x // TILE_SIZE
        tile_y = self.player.y // TILE_SIZE
        
        # Maak een font voor de coördinaten
        coord_font = pygame.font.SysFont(None, 20)
        
        # Maak tekstoppervlak met coördinaten
        coord_text = coord_font.render(f"Positie: ({tile_x}, {tile_y})", True, (255, 255, 255))
        
        # Maak achtergrond voor betere leesbaarheid
        text_bg = pygame.Surface((coord_text.get_width() + 10, coord_text.get_height() + 6))
        text_bg.fill((0, 0, 0))
        text_bg.set_alpha(180)  # Semitransparant
        
        # Render in rechteronderhoek
        bg_x = SCREEN_WIDTH - text_bg.get_width() - 10
        bg_y = SCREEN_HEIGHT - text_bg.get_height() - 10
        text_x = bg_x + 5
        text_y = bg_y + 3
        
        self.screen.blit(text_bg, (bg_x, bg_y))
        self.screen.blit(coord_text, (text_x, text_y))
    
    def update_camera(self):
        """Update camera positie om speler te volgen"""
        # Centreer camera op speler
        self.camera_offset_x = self.player.x - SCREEN_WIDTH // 2
        self.camera_offset_y = self.player.y - SCREEN_HEIGHT // 2
        
        # Begrens camera aan wereldgrenzen
        self.camera_offset_x = max(0, min(self.camera_offset_x, 
                                        self.world.width - SCREEN_WIDTH))
        self.camera_offset_y = max(0, min(self.camera_offset_y, 
                                        self.world.height - SCREEN_HEIGHT))
    
    def check_interactions(self):
        """Check voor interacties met NPC's of objecten"""
        # Check voor NPC interacties
        keys = pygame.key.get_pressed()
        
        # Gebruik een 'pressed' variabele in plaats van rechtstreekse key check
        if hasattr(self, 'space_pressed') and self.space_pressed and not keys[pygame.K_SPACE] and not keys[pygame.K_RETURN]:
            # Space was ingedrukt en is nu losgelaten
            self.space_pressed = False
        
        # Alleen interactie toestaan als space pas net is ingedrukt (niet vasthouden)
        if (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]) and not hasattr(self, 'space_pressed'):
            self.space_pressed = True
            
            for npc in self.world.npcs:
                if (abs(self.player.x - npc.x) < 40 and 
                    abs(self.player.y - npc.y) < 40):
                    # Voeg een korte vertraging toe voor veiligheid
                    pygame.time.delay(100)
                    self.state = STATE_DIALOGUE
                    self.ui.start_dialogue(npc.get_dialogue(self.player.stats["karma"]), npc.name)
                    return
    
    def update_encounter_timer(self):
        """Update timer voor willekeurige gevechten (alleen voor demo)"""
        # In deze versie alleen encounters in het bosgebied, niet in het dorp
        player_tile_x = self.player.x // 32
        player_tile_y = self.player.y // 32
        
        # Controleer of speler in bosgebied is (rechts van de rivier)
        in_forest_area = False
        if player_tile_x < len(self.world.tiles[0]) and player_tile_y < len(self.world.tiles):
            # Controleer of speler op gras staat en in 'bosgebied' is (heuristiek)
            if (player_tile_x > len(self.world.tiles[0]) // 2 and  # Ten oosten van midden van map 
                self.world.tiles[player_tile_y][player_tile_x] == 0):  # Op gras
                in_forest_area = True
        
        if in_forest_area:
            self.encounter_timer += 1
            if self.encounter_timer >= self.encounter_threshold:
                self.encounter_timer = 0
                # Kans op encounter
                if random.random() < self.encounter_chance:
                    # Start combat met willekeurige vijand
                    enemy = random.choice(self.demo_enemies)
                    self.start_combat(enemy)
        else:
            # Reset timer als niet in bosgebied
            self.encounter_timer = 0
    
    def start_combat(self, enemy):
        """Start een gevecht met een vijand"""
        self.state = STATE_COMBAT
        self.combat_system.start_combat(self.player, enemy)
    
    def render_help_text(self):
        """Render help text voor controls"""
        help_font = pygame.font.SysFont(None, 22)
        
        help_texts = [
            "Tri-Sharira RPG Demo Controls:",
            "Pijltjestoetsen/WASD: Beweging",
            "SPACE/ENTER: Interactie met NPC's",
            "ESC: Menu openen/sluiten",
            "H: Toggle help tekst",
            "In gevecht: Pijltjestoetsen om te navigeren, SPACE/ENTER om te selecteren"
        ]
        
        # Achtergrond voor help tekst
        help_bg = pygame.Surface((400, 150))
        help_bg.fill((0, 0, 0))
        help_bg.set_alpha(180)
        
        # Toon rechtsboven
        self.screen.blit(help_bg, (SCREEN_WIDTH - 410, 10))
        
        # Render elke tekstregel
        for i, text in enumerate(help_texts):
            text_surface = help_font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (SCREEN_WIDTH - 400, 20 + i * 22))