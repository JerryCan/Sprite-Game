# NPC klasse voor niet-speelbare karakters
import pygame
import random
from src.entity import Entity
from src.config import TILE_SIZE

class NPC(Entity):
    def __init__(self, x, y, npc_type, name, dialogue):
        super().__init__(x, y, npc_type)
        self.name = name
        self.base_dialogue = dialogue
        self.dialogue = dialogue  # Huidige dialoog
        self.interactable = True  # Kan de speler interactie hebben
        self.movement_pattern = None  # Mogelijk: "stationary", "patrol", "wander"
        self.movement_timer = 0
        self.movement_cooldown = 60  # Frames tussen bewegingen
        self.patrol_points = []  # Voor NPCs die een route volgen
        self.current_patrol_point = 0
        
        # Maak placeholder sprite op basis van type
        self.sprite = self._create_placeholder_sprite(npc_type)
    
    def _create_placeholder_sprite(self, npc_type):
        """Maak eenvoudige sprite voor de demo"""
        sprite = pygame.Surface((TILE_SIZE, TILE_SIZE))
        
        # Kleur op basis van NPC type
        if npc_type == "elder":
            sprite.fill((100, 100, 255))  # Blauw voor oudere
        elif npc_type == "merchant":
            sprite.fill((255, 255, 0))    # Geel voor handelaar
        elif npc_type == "spiritual":
            sprite.fill((150, 0, 255))    # Paars voor spirituele figuur
        elif npc_type == "youth":
            sprite.fill((0, 255, 0))      # Groen voor jongere
        else:
            sprite.fill((200, 200, 200))  # Grijs voor generiek
        
        # Teken een kader om de NPC
        pygame.draw.rect(sprite, (0, 0, 0), (0, 0, TILE_SIZE, TILE_SIZE), 1)
        
        return sprite
    
    def set_movement_pattern(self, pattern, patrol_points=None):
        """
        Stel bewegingspatroon in voor de NPC
        pattern: "stationary", "wander", of "patrol"
        patrol_points: lijst van (x,y) coördinaten voor patrouille
        """
        self.movement_pattern = pattern
        if pattern == "patrol" and patrol_points:
            self.patrol_points = patrol_points
    
    def update(self, obstacles=None):
        """Update NPC gedrag"""
        if self.movement_pattern == "stationary":
            pass  # Geen beweging
        
        elif self.movement_pattern == "wander":
            # Willekeurige beweging af en toe
            self.movement_timer += 1
            if self.movement_timer >= self.movement_cooldown:
                self.movement_timer = 0
                if random.random() < 0.5:  # 50% kans om te bewegen
                    direction = random.choice(["up", "down", "left", "right"])
                    dx, dy = 0, 0
                    
                    if direction == "up":
                        dy = -1
                        self.direction = "up"
                    elif direction == "down":
                        dy = 1
                        self.direction = "down"
                    elif direction == "left":
                        dx = -1
                        self.direction = "left"
                    elif direction == "right":
                        dx = 1
                        self.direction = "right"
                    
                    self.move(dx, dy, obstacles)
        
        elif self.movement_pattern == "patrol":
            # Volg patrouillepunten
            if not self.patrol_points:
                return
                
            self.movement_timer += 1
            if self.movement_timer >= self.movement_cooldown:
                self.movement_timer = 0
                
                # Bereken richting naar volgend punt
                target_x, target_y = self.patrol_points[self.current_patrol_point]
                dx, dy = 0, 0
                
                if self.x < target_x:
                    dx = 1
                    self.direction = "right"
                elif self.x > target_x:
                    dx = -1
                    self.direction = "left"
                elif self.y < target_y:
                    dy = 1
                    self.direction = "down"
                elif self.y > target_y:
                    dy = -1
                    self.direction = "up"
                
                # Beweeg naar target
                self.move(dx, dy, obstacles)
                
                # Check of we bij het punt zijn
                if abs(self.x - target_x) < 2 and abs(self.y - target_y) < 2:
                    self.current_patrol_point = (self.current_patrol_point + 1) % len(self.patrol_points)
    
    def render(self, screen, camera_offset_x, camera_offset_y):
        """Render NPC op scherm"""
        screen.blit(self.sprite, (self.x - camera_offset_x, self.y - camera_offset_y))
        
        # Debug: teken collision rectangle
        collision_rect_screen = pygame.Rect(
            self.collision_rect.x - camera_offset_x,
            self.collision_rect.y - camera_offset_y,
            self.collision_rect.width,
            self.collision_rect.height
        )
        pygame.draw.rect(screen, (255, 0, 0), collision_rect_screen, 1)
    
    def get_dialogue(self, player_karma=0):
        """
        Haal dialoog op, potentieel gewijzigd door speler karma/reputatie
        """
        # In een meer uitgebreide implementatie zou dit dialoog kunnen aanpassen
        # op basis van speler-statistieken of verhaalprogressie
        if player_karma > 10:
            return f"{self.name}: {self.base_dialogue} Je lijkt een goede ziel."
        elif player_karma < -10:
            return f"{self.name}: {self.base_dialogue} Ik voel dat je intenties niet zuiver zijn."
        else:
            return f"{self.name}: {self.base_dialogue}"
