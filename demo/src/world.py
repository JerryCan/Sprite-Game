# World klasse voor het beheren van de spelwereld
import pygame
import random
import os
from src.config import TILE_SIZE, GREEN, BLUE, BROWN, LIGHTBLUE
from src.npc import NPC

# Hulpfuncties voor het tekenen van objecten en NPC's
def draw_tree(screen, x, y, size):
    """Teken een mooie boom met gelaagde bladeren"""
    # Teken stam (bruin)
    trunk_width = size // 3
    trunk_height = size // 2
    trunk_x = x + (size - trunk_width) // 2
    trunk_y = y + size - trunk_height
    pygame.draw.rect(screen, (101, 67, 33), (trunk_x, trunk_y, trunk_width, trunk_height))
    
    # Teken bladeren (groen, gelaagde cirkels)
    # Onderste laag (donkergroen)
    pygame.draw.circle(screen, (0, 100, 0), (x + size // 2, y + size // 2), size // 2)
    # Middelste laag (medium groen)
    pygame.draw.circle(screen, (0, 120, 0), (x + size // 2, y + size // 3), size // 2.5)
    # Bovenste laag (lichtgroen)
    pygame.draw.circle(screen, (50, 150, 50), (x + size // 2, y + size // 4), size // 3)

def draw_house(screen, x, y, width, height):
    """Teken een huis met details zoals ramen en deur"""
    # Hoofdstructuur (beige/bruin)
    pygame.draw.rect(screen, (210, 180, 140), (x, y, width, height))
    
    # Dak (donkerbruin of rood)
    roof_points = [
        (x, y),
        (x + width // 2, y - height // 3),
        (x + width, y)
    ]
    pygame.draw.polygon(screen, (139, 69, 19), roof_points)
    
    # Deur (donker hout)
    door_width = width // 4
    door_height = height // 2
    door_x = x + (width - door_width) // 2
    door_y = y + height - door_height
    pygame.draw.rect(screen, (101, 67, 33), (door_x, door_y, door_width, door_height))
    
    # Deurknop (geel/goud)
    knob_x = door_x + door_width - door_width // 4
    knob_y = door_y + door_height // 2
    pygame.draw.circle(screen, (218, 165, 32), (knob_x, knob_y), 2)
    
    # Ramen (lichtblauw)
    window_size = width // 5
    # Linkerzijde raam
    window_left_x = x + width // 4 - window_size // 2
    window_y = y + height // 3 - window_size // 2
    pygame.draw.rect(screen, (173, 216, 230), (window_left_x, window_y, window_size, window_size))
    # Kruis in raam
    pygame.draw.line(screen, (0, 0, 0), (window_left_x + window_size // 2, window_y),
                    (window_left_x + window_size // 2, window_y + window_size), 1)
    pygame.draw.line(screen, (0, 0, 0), (window_left_x, window_y + window_size // 2),
                    (window_left_x + window_size, window_y + window_size // 2), 1)
    
    # Rechterzijde raam
    window_right_x = x + width - width // 4 - window_size // 2
    pygame.draw.rect(screen, (173, 216, 230), (window_right_x, window_y, window_size, window_size))
    # Kruis in raam
    pygame.draw.line(screen, (0, 0, 0), (window_right_x + window_size // 2, window_y),
                    (window_right_x + window_size // 2, window_y + window_size), 1)
    pygame.draw.line(screen, (0, 0, 0), (window_right_x, window_y + window_size // 2),
                    (window_right_x + window_size, window_y + window_size // 2), 1)

def draw_temple(screen, x, y, width, height):
    """Teken een tempel/ashram met details zoals zuilen en koepel"""
    # Basis (lichte zandkleur)
    pygame.draw.rect(screen, (255, 222, 173), (x, y, width, height))
    
    # Trap aan de voorkant
    stair_width = width // 2
    stair_height = height // 4
    stair_x = x + (width - stair_width) // 2
    stair_y = y + height - stair_height
    
    # Teken 3 traptreden
    for i in range(3):
        step_height = stair_height // 3
        step_y = stair_y + i * step_height
        step_width = stair_width - i * (stair_width // 6)
        step_x = x + (width - step_width) // 2
        pygame.draw.rect(screen, (222, 184, 135), (step_x, step_y, step_width, step_height))
    
    # Zuilen
    pillar_width = width // 8
    pillar_height = height - stair_height
    # Linker zuil
    pygame.draw.rect(screen, (255, 248, 220), (x + pillar_width, y, pillar_width, pillar_height))
    # Rechter zuil
    pygame.draw.rect(screen, (255, 248, 220), (x + width - pillar_width * 2, y, pillar_width, pillar_height))
    
    # Dakkoepel (goudkleurig)
    dome_rect = pygame.Rect(x + width // 4, y - height // 4, width // 2, height // 2)
    pygame.draw.arc(screen, (218, 165, 32), dome_rect, 0, 3.14, 3)
    
    # Versieringen op het dak
    spire_x = x + width // 2
    spire_y = y - height // 4
    pygame.draw.line(screen, (218, 165, 32), (spire_x, spire_y), (spire_x, spire_y - height // 3), 2)
    # Ornament bovenop
    pygame.draw.circle(screen, (255, 215, 0), (spire_x, spire_y - height // 3), 5)

def get_npc_color(npc_type):
    """Geeft een kleur terug voor elk NPC type"""
    colors = {
        'elder': (100, 100, 200),      # Blauw voor dorpsoudste
        'merchant': (200, 180, 0),     # Goudkleurig voor handelaar
        'youth': (50, 200, 50),        # Groen voor jongere
        'spiritual': (150, 50, 200),   # Paars voor spirituele leraar/guru
        'default': (150, 150, 150)     # Grijs als default
    }
    return colors.get(npc_type, colors['default'])

def draw_npc(screen, npc_type, x, y, size):
    """Teken een NPC met specifieke kenmerken per type"""
    # Basis cirkel voor alle NPC's (lichaam)
    pygame.draw.circle(screen, get_npc_color(npc_type), (x + size // 2, y + size // 2), size // 2)
    
    # Hoofd bovenop lichaam
    head_size = size // 3
    pygame.draw.circle(screen, (255, 218, 185), (x + size // 2, y + size // 4), head_size)
    
    # Speciale kenmerken per type NPC
    if npc_type == 'elder':
        # Witte baard voor dorpsoudste
        pygame.draw.arc(screen, (255, 255, 255), 
                       (x + size // 4, y + size // 4, size // 2, size // 2), 
                       0.2, 2.9, 2)
        # Staf
        pygame.draw.line(screen, (139, 69, 19), 
                        (x + size // 4, y + size // 2), 
                        (x + size // 4, y + size), 2)
    
    elif npc_type == 'merchant':
        # Handelszak/rugzak
        pygame.draw.rect(screen, (101, 67, 33), 
                        (x + size - size // 3, y + size // 2, 
                         size // 4, size // 3))
    
    elif npc_type == 'youth':
        # Jong/kleiner figuur
        # Haar (meer haar voor jonger personage)
        pygame.draw.arc(screen, (139, 69, 19), 
                       (x + size // 3, y + size // 6, size // 3, size // 3), 
                       3.14, 6.28, 2)
    
    elif npc_type == 'spiritual':
        # Meditatie houding
        # Benen gekruist
        pygame.draw.arc(screen, (0, 0, 0), 
                       (x + size // 4, y + 2*size // 3, size // 2, size // 4), 
                       0, 3.14, 1)
        pygame.draw.arc(screen, (0, 0, 0), 
                       (x + size // 4, y + 2*size // 3 + size // 8, size // 2, size // 4), 
                       0, 3.14, 1)
        
        # Aura (subtiel lichtend effect)
        for i in range(3):
            s = pygame.Surface((size + i*4, size + i*4), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 255, 255, 50), 
                              (size // 2 + i*2, size // 2 + i*2), 
                              size // 2 + i*2, 1)
            screen.blit(s, (x - i*2, y - i*2))

class World:
    def __init__(self, map_file=None):
        # Gebruik het opgegeven mapbestand of de standaard map
        self.map_file = map_file
        
        # Probeer de map te laden, val terug op demo map als het niet lukt
        if self.map_file and os.path.exists(self.map_file):
            print(f"Map laden uit bestand: {self.map_file}")
            self.grid_data, map_width, map_height = self.load_map_from_file(self.map_file)
        else:
            print("Map bestand niet gevonden, gebruik demo map")
            # Gebruik een kleine demo map als fallback
            self.grid_data = self._generate_demo_grid()
            map_height = len(self.grid_data)
            map_width = len(self.grid_data[0]) if map_height > 0 else 0
        
        # Stel de wereldgrootte in op basis van de mapafmetingen
        self.width = map_width * TILE_SIZE
        self.height = map_height * TILE_SIZE
        
        # Converteer de griddata naar een tilemap
        self.tiles = self.convert_map_to_tilemap(self.grid_data)
        
        # Objecten in de wereld (bomen, huizen, etc.)
        self.objects = self.extract_objects_from_map(self.grid_data, TILE_SIZE)
        
        # NPC's
        self.npcs = self.extract_npcs_from_map(self.grid_data, TILE_SIZE)
        
        # Obstakels (combinatie van bepaalde tiles en objecten)
        self.obstacles = self._get_obstacles()
    
    def _generate_demo_grid(self):
        """
        Genereert een kleine demo map als fallback
        
        Returns:
            list: 2D lijst met demo map gegevens
        """
        # Maak een kleine 15x15 demo map
        # G=Gras, W=Water, P=Pad, Tr=Boom, H=Huis, Te=Tempel, NE=Dorpsoudste, etc.
        grid = [
            ["G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G"],
            ["G", "G", "Tr", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G"],
            ["G", "G", "G", "G", "Te", "Te", "Te", "G", "G", "G", "G", "W", "W", "G", "G"],
            ["G", "G", "G", "NE", "Te", "Te", "Te", "G", "G", "G", "G", "W", "W", "G", "G"],
            ["G", "G", "G", "P", "P", "P", "P", "P", "G", "G", "G", "W", "W", "G", "G"],
            ["G", "G", "Tr", "P", "P", "P", "P", "P", "P", "G", "G", "W", "W", "G", "G"],
            ["G", "G", "G", "P", "P", "P", "P", "P", "P", "P", "P", "W", "W", "G", "G"],
            ["G", "G", "H", "H", "V", "P", "P", "P", "P", "P", "P", "W", "W", "P", "P"],
            ["G", "G", "H", "H", "P", "P", "P", "NJ", "P", "P", "P", "W", "W", "G", "G"],
            ["G", "G", "G", "G", "P", "P", "P", "H", "H", "P", "G", "W", "W", "G", "G"],
            ["G", "G", "Tr", "G", "G", "G", "G", "H", "H", "G", "G", "W", "W", "G", "NS"],
            ["G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G"],
            ["G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G"],
            ["G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G", "G"],
            ["G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G", "G", "G"]
        ]
        return grid

    def load_map_from_file(self, file_path):
        """
        Laadt een map vanuit een .map bestand
        
        Args:
            file_path (str): Pad naar het .map bestand
            
        Returns:
            tuple: (grid_data, width, height) waar:
                - grid_data is een 2D lijst met mapgegevens
                - width is de breedte van de map
                - height is de hoogte van de map
        """
        grid_data = []
        width = 0
        height = 0
        
        try:
            with open(file_path, 'r') as file:
                # Filter commentaarregels en lege regels
                lines = [line.strip() for line in file.readlines() 
                       if line.strip() and not line.strip().startswith('//')]                
                # Bepaal dimensies
                height = len(lines)
                
                # Bepaal de delimiter (standaard '|')
                delimiter = '|'
                
                # Verwerk mapdata
                for line in lines:
                    # Split de regel op de delimiter
                    cells = line.split(delimiter)
                    
                    # Sla de regel op in grid_data
                    grid_data.append(cells)
                    
                    # Update breedte indien nodig
                    if len(cells) > width:
                        width = len(cells)
        
        except Exception as e:
            print(f"Fout bij het laden van de map: {e}")
            # Maak een lege map bij fout
            grid_data = [['G' for _ in range(10)] for _ in range(10)]
            width, height = 10, 10
        
        return grid_data, width, height
    
    def convert_map_to_tilemap(self, grid_data):
        """
        Converteert ruw griddata naar een tilemap voor de game engine
        
        Args:
            grid_data (list): 2D lijst met mapgegevens
            
        Returns:
            list: 2D lijst met tiletypen (0=gras, 1=water, 2=pad, etc.)
        """
        height = len(grid_data)
        width = len(grid_data[0]) if height > 0 else 0
        
        # Maak een lege tilemap
        tilemap = [[0 for _ in range(width)] for _ in range(height)]
        
        # Mapping van terreintypen naar tilenummers
        terrain_to_tile = {
            'G': 0,  # Gras
            'W': 1,  # Water
            'P': 2,  # Pad
            'Br': 3, # Brug
            'Be': 4  # Berg
        }
        
        # Vul de tilemap met de juiste waarden
        for y in range(height):
            for x in range(min(width, len(grid_data[y]))):
                cell = grid_data[y][x]
                # Zet terreintype om naar tilenummer als het een terreintype is
                # Objecten en NPC's worden later toegevoegd
                if cell in terrain_to_tile:
                    tilemap[y][x] = terrain_to_tile[cell]
                else:
                    # Voor andere elementen zoals Tr, H, NPC's, etc. is de ondergrond gras
                    tilemap[y][x] = 0  # Gras als default
        
        return tilemap
    
    def extract_objects_from_map(self, grid_data, tile_size):
        """
        Haalt objecten (gebouwen, bomen, etc.) uit de mapdata
        
        Args:
            grid_data (list): 2D lijst met mapgegevens
            tile_size (int): Grootte van een tegel in pixels
            
        Returns:
            list: Lijst met objecten voor de wereld
        """
        objects = []
        
        # Houd bij welke tegels al zijn verwerkt voor meerdere tegels brede objecten
        processed_tiles = set()
        
        # Loop door de grid heen
        for y, row in enumerate(grid_data):
            for x, cell in enumerate(row):
                # Sla over als deze tegel al is verwerkt
                if (x, y) in processed_tiles:
                    continue
                
                # Positie in pixels
                px, py = x * tile_size, y * tile_size
                
                # Controleer op bomen
                if cell == 'Tr':
                    objects.append({
                        'type': 'tree',
                        'x': px,
                        'y': py,
                        'width': tile_size,
                        'height': tile_size,
                        'collision': pygame.Rect(px + 8, py + tile_size - 8, tile_size - 16, 8),
                        'name': None
                    })
                
                # Controleer op huizen
                elif cell == 'H':
                    # Zoek naar aangrenzend huistegel om grootte te bepalen
                    width = height = tile_size
                    
                    # Controleer rechts
                    if x + 1 < len(row) and row[x + 1] == 'H':
                        width = tile_size * 2
                        processed_tiles.add((x + 1, y))
                    
                    # Controleer onder
                    if y + 1 < len(grid_data) and x < len(grid_data[y + 1]) and grid_data[y + 1][x] == 'H':
                        height = tile_size * 2
                        processed_tiles.add((x, y + 1))
                        
                        # Controleer rechtsonder voor 2x2 huis
                        if x + 1 < len(row) and row[x + 1] == 'H' and y + 1 < len(grid_data) and \
                           x + 1 < len(grid_data[y + 1]) and grid_data[y + 1][x + 1] == 'H':
                            processed_tiles.add((x + 1, y + 1))
                    
                    objects.append({
                        'type': 'house',
                        'x': px,
                        'y': py,
                        'width': width,
                        'height': height,
                        'collision': pygame.Rect(px, py, width, height),
                        'name': f"Huis {x},{y}"  # Standaardnaam, later aan te passen
                    })
                
                # Controleer op tempels/ashrams
                elif cell == 'Te':
                    # Zoek naar aangrenzende tempeltegels om grootte te bepalen
                    width = height = tile_size
                    
                    # Zoek naar horizontale uitbreiding
                    i = 1
                    while x + i < len(row) and row[x + i] == 'Te':
                        processed_tiles.add((x + i, y))
                        i += 1
                    width = tile_size * i
                    
                    # Zoek naar verticale uitbreiding
                    j = 1
                    is_rectangle = True
                    while y + j < len(grid_data) and is_rectangle:
                        # Controleer of de rij onder volledig bestaat uit Te tegels
                        for k in range(i):
                            if (x + k >= len(grid_data[y + j]) or grid_data[y + j][x + k] != 'Te'):
                                is_rectangle = False
                                break
                        
                        if is_rectangle:
                            # Markeer alle tegels als verwerkt
                            for k in range(i):
                                processed_tiles.add((x + k, y + j))
                            j += 1
                        else:
                            break
                    
                    height = tile_size * j
                    
                    objects.append({
                        'type': 'temple',
                        'x': px,
                        'y': py,
                        'width': width,
                        'height': height,
                        'collision': pygame.Rect(px, py, width, height),
                        'name': "Tempel/Ashram"  # Standaardnaam, later aan te passen
                    })
        
        return objects
    
    def extract_npcs_from_map(self, grid_data, tile_size):
        """
        Haalt NPC's uit de mapdata
        
        Args:
            grid_data (list): 2D lijst met mapgegevens
            tile_size (int): Grootte van een tegel in pixels
            
        Returns:
            list: Lijst met NPC's voor de wereld
        """
        npcs = []
        
        # NPC definities
        npc_types = {
            'NE': {
                'type': 'elder',
                'name': 'Dorpsoudste Arjun',
                'dialogue': 'Welkom in ons dorp. Ik ben verantwoordelijk voor het bestuur hier.',
                'movement': 'stationary'
            },
            'NH': {
                'type': 'merchant',
                'name': 'Handelaar Vikram',
                'dialogue': 'Ik heb waren uit vele regio\'s. Wat zoek je?',
                'movement': 'wander'
            },
            'NJ': {
                'type': 'youth',
                'name': 'Jongere Anil',
                'dialogue': 'Ik wil later op avontuur gaan, net als jij!',
                'movement': 'wander'
            },
            'NS': {
                'type': 'spiritual',
                'name': 'Guru Prana',
                'dialogue': 'De balans tussen de drie lichamen is essentieel voor innerlijke vrede.',
                'movement': 'stationary'
            },
            'V': {
                'type': 'merchant',
                'name': 'Marktkoopman',
                'dialogue': 'Kijk gerust rond op onze markt!',
                'movement': 'wander'
            }
        }
        
        # Loop door de grid heen
        for y, row in enumerate(grid_data):
            for x, cell in enumerate(row):
                # Controleer of de cel een NPC is
                if cell in npc_types:
                    # Positie in pixels
                    px, py = x * tile_size, y * tile_size
                    
                    # Haal NPC gegevens op
                    npc_data = npc_types[cell]
                    
                    # Creëer de NPC
                    npc = NPC(px, py, npc_data['type'], npc_data['name'], npc_data['dialogue'])
                    npc.set_movement_pattern(npc_data['movement'])
                    
                    npcs.append(npc)
        
        return npcs
    
    def _get_obstacles(self):
        """Verzamel alle objecten waarmee collision detection moet gebeuren"""
        obstacles = []
        
        # Voeg objecten toe met collision
        for obj in self.objects:
            if 'collision' in obj:
                # Maak Entity-achtige objecten voor collision
                obstacle = type('Obstacle', (), {})()
                obstacle.collision_rect = obj['collision']
                obstacles.append(obstacle)
        
        # Water tiles zijn ook obstakels
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile == 1:  # water (controleer of dit overeenkomt met je water tile index)
                    obstacle = type('Obstacle', (), {})()
                    obstacle.collision_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    obstacles.append(obstacle)
        
        # Voeg wereldgrenzen toe
        # Bovenkant wereldgrens
        top_border = type('Obstacle', (), {})()
        top_border.collision_rect = pygame.Rect(0, -TILE_SIZE, self.width, TILE_SIZE)
        obstacles.append(top_border)
        
        # Onderkant wereldgrens
        bottom_border = type('Obstacle', (), {})()
        bottom_border.collision_rect = pygame.Rect(0, self.height, self.width, TILE_SIZE)
        obstacles.append(bottom_border)
        
        # Linkerkant wereldgrens
        left_border = type('Obstacle', (), {})()
        left_border.collision_rect = pygame.Rect(-TILE_SIZE, 0, TILE_SIZE, self.height)
        obstacles.append(left_border)
        
        # Rechterkant wereldgrens
        right_border = type('Obstacle', (), {})()
        right_border.collision_rect = pygame.Rect(self.width, 0, TILE_SIZE, self.height)
        obstacles.append(right_border)
        
        return obstacles
    
    def update(self):
        """Update de toestand van de wereld"""
        # Update NPCs
        for npc in self.npcs:
            npc.update(self.obstacles)
    
    def render(self, screen, camera_offset_x, camera_offset_y):
        """Render de wereld met camera offset"""
        # Bepaal welke tiles zichtbaar zijn op basis van de camera positie
        start_x = max(0, camera_offset_x // TILE_SIZE)
        end_x = min(len(self.tiles[0]), (camera_offset_x + screen.get_width()) // TILE_SIZE + 1)
        start_y = max(0, camera_offset_y // TILE_SIZE)
        end_y = min(len(self.tiles), (camera_offset_y + screen.get_height()) // TILE_SIZE + 1)
        
        # Render tiles
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if y < len(self.tiles) and x < len(self.tiles[y]):
                    tile_type = self.tiles[y][x]
                    
                    # Bepaal kleur op basis van tile type
                    color = GREEN  # Default: gras
                    if tile_type == 1:
                        color = LIGHTBLUE  # Water
                    elif tile_type == 2:
                        color = BROWN  # Pad
                    elif tile_type == 3:
                        color = (150, 100, 50)  # Bruine brug
                    elif tile_type == 4:
                        color = (100, 100, 100)  # Grijze berg
                    
                    # Teken de tile
                    rect = pygame.Rect(
                        x * TILE_SIZE - camera_offset_x,
                        y * TILE_SIZE - camera_offset_y,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Kader om elke tile
        
        # Render objecten
        name_labels = []  # Verzamel naamlabels om bovenop alles te tekenen
        
        for obj in self.objects:
            # Controleer of object in scherm is
            obj_rect = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
            screen_rect = pygame.Rect(camera_offset_x, camera_offset_y, 
                                     screen.get_width(), screen.get_height())
            
            if obj_rect.colliderect(screen_rect):
                # Schermcoördinaten berekenen (gecorrigeerd voor camera)
                screen_x = obj['x'] - camera_offset_x
                screen_y = obj['y'] - camera_offset_y
                
                if obj['type'] == 'tree':
                    # Gebruik de verbeterde boomfunctie
                    draw_tree(screen, screen_x, screen_y, TILE_SIZE)
                
                elif obj['type'] == 'house':
                    # Gebruik de verbeterde huisfunctie
                    draw_house(screen, screen_x, screen_y, obj['width'], obj['height'])
                    
                    # Verzamel naam van het gebouw voor latere weergave
                    if obj['name']:
                        name_labels.append({
                            'text': obj['name'],
                            'position': (screen_x + obj['width'] // 2, screen_y - 15)
                        })
                
                elif obj['type'] == 'temple':
                    # Gebruik de verbeterde tempelfunctie
                    draw_temple(screen, screen_x, screen_y, obj['width'], obj['height'])
                    
                    # Verzamel naam van het gebouw voor latere weergave
                    if obj['name']:
                        name_labels.append({
                            'text': obj['name'],
                            'position': (screen_x + obj['width'] // 2, screen_y - 20)
                        })
        
        # Render NPCs
        for npc in self.npcs:
            # Controleer of NPC in scherm is
            if (0 <= npc.x - camera_offset_x <= screen.get_width() and
                0 <= npc.y - camera_offset_y <= screen.get_height()):
                # Gebruik de standaard NPC render code of de verbeterde visualisatie
                if hasattr(npc, 'custom_render') and callable(npc.custom_render):
                    # Als NPC eigen render functie heeft, gebruik die
                    npc.custom_render(screen, camera_offset_x, camera_offset_y)
                else:
                    # Anders gebruik de verbeterde NPC visualisatie
                    screen_x = npc.x - camera_offset_x
                    screen_y = npc.y - camera_offset_y
                    draw_npc(screen, npc.type, screen_x, screen_y, TILE_SIZE)
                    
                    # Teken de naam van de NPC boven het hoofd
                    if hasattr(npc, 'name') and npc.name:
                        name_labels.append({
                            'text': npc.name,
                            'position': (screen_x + TILE_SIZE // 2, screen_y - 10)
                        })
        
        # Teken de naamlabels bovenop alles
        font = pygame.font.SysFont(None, 18)  # Kleinere font voor naamlabels
        for label in name_labels:
            # Teken een kleine transparante achtergrond voor betere leesbaarheid
            text_surface = font.render(label['text'], True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=label['position'])
            
            bg_rect = text_rect.copy()
            bg_rect.inflate_ip(10, 6)  # Maak achtergrond iets groter dan tekst
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
            bg_surface.fill((255, 255, 255))
            bg_surface.set_alpha(180)  # Half-transparant
            
            screen.blit(bg_surface, bg_rect)
            screen.blit(text_surface, text_rect)