# Entity basisklasse voor alle gameobjecten met positie en interactie
import pygame
from src.config import TILE_SIZE

class Entity:
    def __init__(self, x, y, entity_type):
        self.x = x
        self.y = y
        self.type = entity_type
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Animatie attributen
        self.current_frame = 0
        self.animation_speed = 0.1
        self.animation_timer = 0
        self.direction = "down"  # Standaard richting
        
        # Voor basis collision detection
        self.collision_rect = pygame.Rect(x + 4, y + self.height - 10, self.width - 8, 10)
    
    def move(self, dx, dy, obstacles=None):
        """
        Beweeg entity met collision detection tegen obstacles
        """
        # Update collision rect positie voor bewegingscheck
        temp_rect = self.collision_rect.copy()
        temp_rect.x += dx
        temp_rect.y += dy
        
        # Check collision met obstacles
        can_move = True
        if obstacles:
            for obstacle in obstacles:
                if temp_rect.colliderect(obstacle.collision_rect):
                    can_move = False
                    break
        
        # Beweeg als er geen obstakels zijn
        if can_move:
            self.x += dx
            self.y += dy
            self.rect.x = self.x
            self.rect.y = self.y
            self.collision_rect.x = self.x + 4
            self.collision_rect.y = self.y + self.height - 10
            return True
        return False
    
    def animate(self):
        """Update animatie frame"""
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % 4  # Aanname: 4 frames per animatie
    
    def update(self):
        """Update entity state, wordt elke frame aangeroepen"""
        pass
    
    def render(self, screen, camera_offset_x, camera_offset_y):
        """
        Render entity op scherm met camera offset
        Moet worden geïmplementeerd door afgeleiden klassen
        """
        pass
