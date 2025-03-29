# Player klasse - bestuurd door de speler
import pygame
from src.entity import Entity
from src.config import PLAYER_SPEED, PHYSICAL_STATS, MENTAL_STATS, SPIRITUAL_STATS

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "player")
        self.speed = PLAYER_SPEED
        self.direction = "down"  # down, up, left, right
        
        # Placeholder voor echte sprites - in demo gebruiken we gekleurde rechthoeken
        self.placeholder_sprites = self._create_placeholder_sprites()
        
        # Tri-Sharira statistieken
        self.stats = {
            # Universal
            "hp": 100,
            "max_hp": 100,
            "movement": 5,
            
            # Physical body (Sthūla Sharīra)
            "strength": 10,      # Attack power
            "endurance": 8,      # Stamina for actions
            "defense": 7,        # Physical damage reduction
            "speed": 9,          # Dodge and initiative
            
            # Mental body (Sūkshma Sharīra)
            "focus": 8,          # Accuracy and concentration
            "insight": 7,        # Finding weaknesses
            "willpower": 9,      # Status effect resistance
            "memory": 6,         # Pattern recognition
            
            # Spiritual body (Kārana Sharīra)
            "prana": 50,         # Spiritual energy
            "max_prana": 50,
            "intuition": 6,      # Prediction ability
            "devotion": 5,       # Healing and support boosts
            "karma": 8,          # Luck factor and NPC reactions
        }
        
        # Inventory
        self.inventory = []
        
        # Skills (basis vaardigheden)
        self.skills = [
            {"name": "Basic Attack", "type": "physical", "power": 5, "cost": 0},
            {"name": "Focus Mind", "type": "mental", "power": 0, "cost": 0, "effect": "increase_accuracy"},
            {"name": "Prana Beam", "type": "spiritual", "power": 8, "cost": 5},
        ]
    
    def _create_placeholder_sprites(self):
        """
        Maak tijdelijke sprites voor de demo (gekleurde rechthoeken)
        Later te vervangen door echte sprites
        """
        sprites = {}
        
        # Voor elke richting maken we een eenvoudige sprite
        directions = ["down", "up", "left", "right"]
        colors = {
            "down": (0, 0, 255),   # Blauw
            "up": (0, 100, 255),   # Lichterblauw
            "left": (0, 150, 255), # Nog lichter
            "right": (0, 200, 255) # Lichtst
        }
        
        for direction in directions:
            # Maak 4 frames als placeholder voor animaties
            frames = []
            for i in range(4):
                frame = pygame.Surface((self.width, self.height))
                frame.fill(colors[direction])
                # Teken een lichter vierkant om de 'beweging' aan te geven
                light_pos = i * 5  # Varieer de positie voor animatie
                pygame.draw.rect(frame, (200, 200, 255), 
                               (light_pos, light_pos, 10, 10))
                frames.append(frame)
            sprites[direction] = frames
            
        return sprites
    
    def handle_event(self, event):
        """Handle toetsenbordinvoer voor de speler"""
        # We verwerken toetsenbordinvoer in de update methode
        pass
    
    def update(self, obstacles=None):
        """Update spelerstatus op basis van input"""
        keys = pygame.key.get_pressed()
        
        # Reset beweging
        dx, dy = 0, 0
        moving = False
        
        # Controleer bewegingstoetsen
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed
            self.direction = "left"
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed
            self.direction = "right"
            moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed
            self.direction = "up"
            moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed
            self.direction = "down"
            moving = True
        
        # Update positie als we bewegen
        if moving:
            self.move(dx, dy, obstacles)
            self.animate()
        else:
            # Reset naar idle frame
            self.current_frame = 0
    
    def render(self, screen, camera_offset_x, camera_offset_y):
        """Render speler met huidige animatieframe"""
        # Haal de juiste sprite op basis van richting
        animation = self.placeholder_sprites[self.direction]
        frame = animation[self.current_frame]
        
        # Teken speler op scherm (gecorrigeerd voor camera)
        screen.blit(frame, (self.x - camera_offset_x, self.y - camera_offset_y))
        
        # Debug: teken collision rectangle
        collision_rect_screen = pygame.Rect(
            self.collision_rect.x - camera_offset_x,
            self.collision_rect.y - camera_offset_y,
            self.collision_rect.width,
            self.collision_rect.height
        )
        pygame.draw.rect(screen, (255, 0, 0), collision_rect_screen, 1)
    
    def add_to_inventory(self, item):
        """Voeg item toe aan inventory"""
        self.inventory.append(item)
    
    def use_skill(self, skill_index, target=None):
        """Gebruik vaardigheid (in gevecht)"""
        if skill_index >= len(self.skills):
            return False
        
        skill = self.skills[skill_index]
        
        # Controleer of we genoeg energie hebben
        if skill["cost"] > self.stats["prana"]:
            return False
        
        # Pas kosten toe
        self.stats["prana"] -= skill["cost"]
        
        # Voer skill effect uit - dit zou normaal gesproken naar het gevecht systeem gaan
        # Hier is een eenvoudige implementatie
        if target and skill["type"] == "physical":
            damage = skill["power"] + (self.stats["strength"] // 2)
            return {"type": "damage", "value": damage}
        elif target and skill["type"] == "spiritual":
            damage = skill["power"] + (self.stats["prana"] // 10)
            return {"type": "damage", "value": damage}
        elif skill["type"] == "mental" and "effect" in skill:
            if skill["effect"] == "increase_accuracy":
                return {"type": "buff", "stat": "focus", "value": 2}
        
        return True
