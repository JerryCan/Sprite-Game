# Combat systeem voor Tri-Sharira RPG
import pygame
import random
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, GREEN, BLUE

class Enemy:
    """Eenvoudige vijand klasse voor demo"""
    def __init__(self, name, level, enemy_type):
        self.name = name
        self.level = level
        self.type = enemy_type  # physical, mental, spiritual
        
        # Basis stats
        self.stats = {
            "hp": 50 + (level * 10),
            "max_hp": 50 + (level * 10),
            "strength": 5 + (level * 2),
            "defense": 3 + level,
            "speed": 4 + level,
            "focus": 5 + level,
            "prana": 20 + (level * 5),
            "max_prana": 20 + (level * 5)
        }
        
        # Aanvallen op basis van type
        self.attacks = []
        if enemy_type == "physical":
            self.attacks = [
                {"name": "Strike", "type": "physical", "power": 5, "cost": 0},
                {"name": "Power Blow", "type": "physical", "power": 10, "cost": 5}
            ]
        elif enemy_type == "mental":
            self.attacks = [
                {"name": "Mind Jab", "type": "mental", "power": 5, "cost": 0},
                {"name": "Confuse", "type": "mental", "power": 3, "cost": 5, 
                 "effect": "confusion", "duration": 2}
            ]
        elif enemy_type == "spiritual":
            self.attacks = [
                {"name": "Spirit Touch", "type": "spiritual", "power": 4, "cost": 0},
                {"name": "Energy Drain", "type": "spiritual", "power": 7, "cost": 5, 
                 "effect": "drain", "drain_amount": 3}
            ]
        
        # Sprite placeholder voor demo
        self.sprite = self._create_placeholder_sprite()
    
    def _create_placeholder_sprite(self):
        """Maak eenvoudige sprite op basis van type"""
        sprite = pygame.Surface((64, 64))
        
        if self.type == "physical":
            sprite.fill((200, 50, 50))  # Rood voor fysiek
            # Teken symbool
            pygame.draw.polygon(sprite, (255, 200, 200), [(20, 15), (44, 15), (32, 45)])
        elif self.type == "mental":
            sprite.fill((50, 50, 200))  # Blauw voor mentaal
            # Teken symbool
            pygame.draw.circle(sprite, (200, 200, 255), (32, 32), 20)
        elif self.type == "spiritual":
            sprite.fill((150, 50, 200))  # Paars voor spiritueel
            # Teken symbool
            pygame.draw.rect(sprite, (220, 200, 255), (12, 12, 40, 40))
        
        return sprite
    
    def choose_attack(self):
        """Kies een willekeurige aanval"""
        # 70% kans op basis aanval, 30% kans op speciale aanval
        if random.random() < 0.7 or self.stats["prana"] < 5:
            return self.attacks[0]  # Basis aanval
        else:
            return self.attacks[1]  # Speciale aanval

class CombatSystem:
    def __init__(self):
        # Laad een font voor combat UI
        self.font = pygame.font.SysFont(None, 24)
        self.header_font = pygame.font.SysFont(None, 32)
        self.reset()
    
    def reset(self):
        """Reset combat state"""
        self.player = None
        self.enemy = None
        self.player_turn = True
        self.combat_over = False
        self.victory = False
        self.selected_action = 0
        self.selected_skill = 0
        self.action_categories = ["Attack", "Skills", "Items", "Escape"]
        self.current_menu = "main"  # main, skills, items
        self.message = ""
        self.message_timer = 0
        self.action_results = []
        self.battle_log = []
        self.status_effects = {"player": [], "enemy": []}
    
    def start_combat(self, player, enemy):
        """Start een gevecht tussen speler en vijand"""
        self.reset()
        self.player = player
        self.enemy = enemy
        self.player_turn = True
        self.combat_over = False
        self.message = f"Een {enemy.name} verschijnt!"
        self.battle_log.append(self.message)
    
    def handle_event(self, event):
        """Verwerk combat input"""
        if not self.player_turn or self.combat_over:
            # Als het niet speler's beurt is of gevecht over is, enkel SPACE/RETURN accepteren
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                if self.combat_over:
                    return True  # Signaal om gevecht volledig te beëindigen
                else:
                    self.execute_enemy_turn()
            return False
        
        if event.type == pygame.KEYDOWN:
            if self.current_menu == "main":
                if event.key == pygame.K_UP:
                    self.selected_action = (self.selected_action - 1) % len(self.action_categories)
                elif event.key == pygame.K_DOWN:
                    self.selected_action = (self.selected_action + 1) % len(self.action_categories)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    action = self.action_categories[self.selected_action]
                    if action == "Attack":
                        # Directe aanval
                        self.execute_basic_attack()
                    elif action == "Skills":
                        # Open skill submenu
                        self.current_menu = "skills"
                        self.selected_skill = 0
                    elif action == "Items":
                        # Open item submenu (niet geïmplementeerd in demo)
                        self.message = "Geen items beschikbaar in demo"
                        self.battle_log.append(self.message)
                    elif action == "Escape":
                        # Probeer te ontsnappen
                        self.try_escape()
            
            elif self.current_menu == "skills":
                if event.key == pygame.K_UP:
                    self.selected_skill = (self.selected_skill - 1) % len(self.player.skills)
                elif event.key == pygame.K_DOWN:
                    self.selected_skill = (self.selected_skill + 1) % len(self.player.skills)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # Gebruik geselecteerde skill
                    self.use_skill(self.selected_skill)
                elif event.key == pygame.K_ESCAPE:
                    # Terug naar hoofdmenu
                    self.current_menu = "main"
        
        return False
    
    def execute_basic_attack(self):
        """Voer een basis aanval uit"""
        # Berekenen van schade
        base_damage = self.player.stats["strength"] - (self.enemy.stats["defense"] // 2)
        damage = max(1, base_damage)  # Minimaal 1 schade
        
        # Toepassen schade
        self.enemy.stats["hp"] -= damage
        
        # Bericht tonen
        self.message = f"Je valt aan voor {damage} schade!"
        self.battle_log.append(self.message)
        
        # Controleer of vijand verslagen is
        if self.enemy.stats["hp"] <= 0:
            self.enemy.stats["hp"] = 0
            self.victory = True
            self.combat_over = True
            self.message = f"Je hebt de {self.enemy.name} verslagen!"
            self.battle_log.append(self.message)
        else:
            # Einde spelerbeurt
            self.player_turn = False
    
    def use_skill(self, skill_index):
        """Gebruik een vaardigheid in gevecht"""
        skill = self.player.skills[skill_index]
        
        # Controleer of we genoeg prana hebben
        if skill["cost"] > self.player.stats["prana"]:
            self.message = "Niet genoeg Prana!"
            self.battle_log.append(self.message)
            return
        
        # Pas kosten toe
        self.player.stats["prana"] -= skill["cost"]
        
        # Voer actie uit op basis van skill type
        if skill["type"] == "physical":
            # Fysieke aanval
            base_damage = skill["power"] + (self.player.stats["strength"] // 2)
            damage = max(1, base_damage - (self.enemy.stats["defense"] // 3))
            
            self.enemy.stats["hp"] -= damage
            self.message = f"Je gebruikt {skill['name']} voor {damage} schade!"
            
        elif skill["type"] == "mental":
            # Mentale vaardigheid
            if "effect" in skill and skill["effect"] == "increase_accuracy":
                # Buff voor speler
                self.message = f"Je gebruikt {skill['name']} en verhoogt je nauwkeurigheid!"
                self.status_effects["player"].append({
                    "name": "accuracy_up",
                    "duration": 3,
                    "value": 2
                })
            else:
                # Mentale aanval
                base_damage = skill["power"] + (self.player.stats["focus"] // 2)
                damage = max(1, base_damage)
                self.enemy.stats["hp"] -= damage
                self.message = f"Je gebruikt {skill['name']} voor {damage} mentale schade!"
                
        elif skill["type"] == "spiritual":
            # Spirituele vaardigheid
            base_damage = skill["power"] + (self.player.stats["prana"] // 10)
            damage = max(1, base_damage)
            
            self.enemy.stats["hp"] -= damage
            self.message = f"Je gebruikt {skill['name']} voor {damage} spirituele schade!"
        
        self.battle_log.append(self.message)
        
        # Reset naar hoofdmenu
        self.current_menu = "main"
        
        # Controleer of vijand verslagen is
        if self.enemy.stats["hp"] <= 0:
            self.enemy.stats["hp"] = 0
            self.victory = True
            self.combat_over = True
            self.message = f"Je hebt de {self.enemy.name} verslagen!"
            self.battle_log.append(self.message)
        else:
            # Einde spelerbeurt
            self.player_turn = False
    
    def try_escape(self):
        """Probeer te ontsnappen uit gevecht"""
        # 50% kans op ontsnappen in demo
        if random.random() < 0.5:
            self.message = "Je ontsnapt succesvol!"
            self.battle_log.append(self.message)
            self.combat_over = True
        else:
            self.message = "Je kunt niet ontsnappen!"
            self.battle_log.append(self.message)
            # Beurt gaat verloren bij mislukte ontsnapping
            self.player_turn = False
    
    def execute_enemy_turn(self):
        """Voer vijand actie uit"""
        # Update status effecten
        self._update_status_effects()
        
        # Kies een aanval
        attack = self.enemy.choose_attack()
        
        # Pas prana kosten toe indien van toepassing
        if attack["cost"] > 0:
            self.enemy.stats["prana"] -= attack["cost"]
        
        # Bereken en pas schade toe
        if attack["type"] == "physical":
            base_damage = attack["power"] + (self.enemy.stats["strength"] // 2)
            damage = max(1, base_damage - (self.player.stats["defense"] // 2))
            
            self.player.stats["hp"] -= damage
            self.message = f"{self.enemy.name} gebruikt {attack['name']} voor {damage} schade!"
            
        elif attack["type"] == "mental":
            base_damage = attack["power"]
            damage = max(1, base_damage)
            
            self.player.stats["hp"] -= damage
            self.message = f"{self.enemy.name} gebruikt {attack['name']} voor {damage} mentale schade!"
            
            # Voeg effect toe indien aanwezig
            if "effect" in attack:
                if attack["effect"] == "confusion":
                    self.status_effects["player"].append({
                        "name": "confusion",
                        "duration": attack["duration"],
                        "chance": 0.3  # 30% kans om beurt te missen
                    })
                    self.message += " Je bent in verwarring!"
            
        elif attack["type"] == "spiritual":
            base_damage = attack["power"]
            damage = max(1, base_damage)
            
            self.player.stats["hp"] -= damage
            self.message = f"{self.enemy.name} gebruikt {attack['name']} voor {damage} spirituele schade!"
            
            # Voeg effect toe indien aanwezig
            if "effect" in attack:
                if attack["effect"] == "drain":
                    drain = attack["drain_amount"]
                    self.player.stats["prana"] = max(0, self.player.stats["prana"] - drain)
                    self.enemy.stats["prana"] = min(self.enemy.stats["max_prana"], 
                                                  self.enemy.stats["prana"] + drain)
                    self.message += f" {drain} Prana gestolen!"
        
        self.battle_log.append(self.message)
        
        # Check of speler is verslagen
        if self.player.stats["hp"] <= 0:
            self.player.stats["hp"] = 0
            self.victory = False
            self.combat_over = True
            self.message = "Je bent verslagen..."
            self.battle_log.append(self.message)
        else:
            # Terug naar spelerbeurt
            self.player_turn = True
    
    def _update_status_effects(self):
        """Update alle status effecten, verlaag duration en verwijder verlopen effecten"""
        # Update player status effecten
        updated_player_effects = []
        for effect in self.status_effects["player"]:
            effect["duration"] -= 1
            if effect["duration"] > 0:
                updated_player_effects.append(effect)
        self.status_effects["player"] = updated_player_effects
        
        # Update enemy status effecten
        updated_enemy_effects = []
        for effect in self.status_effects["enemy"]:
            effect["duration"] -= 1
            if effect["duration"] > 0:
                updated_enemy_effects.append(effect)
        self.status_effects["enemy"] = updated_enemy_effects
    
    def update(self):
        """Update combat state"""
        # Update message timer voor tijdelijke berichten
        if self.message_timer > 0:
            self.message_timer -= 1
    
    def render(self, screen):
        """Render combat scene"""
        # Vul achtergrond
        screen.fill((40, 40, 80))  # Donkerblauw voor gevechtsachtergrond
        
        # Render combat arena
        self._render_arena(screen)
        
        # Render vijand
        self._render_enemy(screen)
        
        # Render speler stats
        self._render_player_stats(screen)
        
        # Render actie menu
        self._render_action_menu(screen)
        
        # Render berichten en battle log
        self._render_messages(screen)
        
        # Render beurtindicator
        turn_text = self.header_font.render(
            "Jouw beurt" if self.player_turn else f"{self.enemy.name}'s beurt", 
            True, GREEN if self.player_turn else RED)
        screen.blit(turn_text, (SCREEN_WIDTH // 2 - 60, 20))
    
    def _render_arena(self, screen):
        """Render combat arena"""
        # Teken een eenvoudige arena
        arena_rect = pygame.Rect(100, 120, SCREEN_WIDTH - 200, 200)
        pygame.draw.rect(screen, (60, 60, 100), arena_rect)
        pygame.draw.rect(screen, (80, 80, 120), arena_rect, 3)
    
    def _render_enemy(self, screen):
        """Render vijand sprite en health bar"""
        # Teken vijand in het midden van de arena
        enemy_x = SCREEN_WIDTH // 2 - 32  # Centreer 64px sprite
        enemy_y = 150
        screen.blit(self.enemy.sprite, (enemy_x, enemy_y))
        
        # Teken naam en level
        name_text = self.font.render(f"{self.enemy.name} Lvl {self.enemy.level}", True, WHITE)
        screen.blit(name_text, (enemy_x - 10, enemy_y - 25))
        
        # Teken health bar
        hp_percent = self.enemy.stats["hp"] / self.enemy.stats["max_hp"]
        bar_width = 100
        filled_width = int(hp_percent * bar_width)
        
        # Achtergrond (leeg deel)
        pygame.draw.rect(screen, (100, 100, 100), 
                       (enemy_x - 18, enemy_y - 10, bar_width, 6))
        # Gevuld deel
        pygame.draw.rect(screen, RED, 
                       (enemy_x - 18, enemy_y - 10, filled_width, 6))
    
    def _render_player_stats(self, screen):
        """Render speler stats voor gevecht"""
        # Teken speler stats linksonder
        stats_bg = pygame.Surface((180, 120))
        stats_bg.fill((40, 40, 60))
        stats_bg.set_alpha(230)
        screen.blit(stats_bg, (20, SCREEN_HEIGHT - 140))
        
        # HP en Prana bars
        hp_percent = self.player.stats["hp"] / self.player.stats["max_hp"]
        prana_percent = self.player.stats["prana"] / self.player.stats["max_prana"]
        
        # HP tekst en bar
        hp_text = self.font.render(f"HP: {self.player.stats['hp']}/{self.player.stats['max_hp']}", 
                                  True, WHITE)
        screen.blit(hp_text, (30, SCREEN_HEIGHT - 130))
        
        # HP bar achtergrond
        pygame.draw.rect(screen, (100, 100, 100), 
                       (30, SCREEN_HEIGHT - 110, 150, 10))
        # HP bar gevuld
        pygame.draw.rect(screen, (200, 50, 50), 
                       (30, SCREEN_HEIGHT - 110, int(hp_percent * 150), 10))
        
        # Prana tekst en bar
        prana_text = self.font.render(f"Prana: {self.player.stats['prana']}/{self.player.stats['max_prana']}", 
                                     True, WHITE)
        screen.blit(prana_text, (30, SCREEN_HEIGHT - 90))
        
        # Prana bar achtergrond
        pygame.draw.rect(screen, (100, 100, 100), 
                       (30, SCREEN_HEIGHT - 70, 150, 10))
        # Prana bar gevuld
        pygame.draw.rect(screen, (50, 50, 200), 
                       (30, SCREEN_HEIGHT - 70, int(prana_percent * 150), 10))
        
        # Status effecten
        if self.status_effects["player"]:
            effect_text = "Status: "
            for effect in self.status_effects["player"]:
                effect_text += f"{effect['name']}({effect['duration']}) "
            effect_surface = self.font.render(effect_text, True, (255, 255, 100))
            screen.blit(effect_surface, (30, SCREEN_HEIGHT - 50))
    
    def _render_action_menu(self, screen):
        """Render actie menu voor speler keuzes"""
        # Teken actie menu rechtsonder
        menu_bg = pygame.Surface((180, 150))
        menu_bg.fill((40, 40, 60))
        menu_bg.set_alpha(230)
        screen.blit(menu_bg, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 170))
        
        # Teken titel
        if self.current_menu == "main":
            title_text = self.font.render("Acties", True, WHITE)
            screen.blit(title_text, (SCREEN_WIDTH - 190, SCREEN_HEIGHT - 165))
            
            # Teken actie opties
            for i, action in enumerate(self.action_categories):
                if i == self.selected_action:
                    color = (255, 255, 0)  # Geel voor geselecteerd
                else:
                    color = WHITE
                
                action_text = self.font.render(action, True, color)
                screen.blit(action_text, (SCREEN_WIDTH - 180, SCREEN_HEIGHT - 135 + i * 25))
        
        elif self.current_menu == "skills":
            title_text = self.font.render("Vaardigheden", True, WHITE)
            screen.blit(title_text, (SCREEN_WIDTH - 190, SCREEN_HEIGHT - 165))
            
            # Teken skill opties
            for i, skill in enumerate(self.player.skills):
                if i == self.selected_skill:
                    color = (255, 255, 0)  # Geel voor geselecteerd
                else:
                    color = WHITE
                
                # Toon skill naam en prana kosten
                skill_text = self.font.render(f"{skill['name']} ({skill['cost']} PRA)", True, color)
                screen.blit(skill_text, (SCREEN_WIDTH - 180, SCREEN_HEIGHT - 135 + i * 25))
    
    def _render_messages(self, screen):
        """Render combat berichten en battle log"""
        # Teken bericht box onderaan
        message_bg = pygame.Surface((SCREEN_WIDTH - 240, 100))
        message_bg.fill((30, 30, 50))
        message_bg.set_alpha(230)
        screen.blit(message_bg, (220, SCREEN_HEIGHT - 120))
        
        # Teken laatst bericht groot
        if self.message:
            message_text = self.font.render(self.message, True, WHITE)
            screen.blit(message_text, (230, SCREEN_HEIGHT - 110))
        
        # Teken laatste 3 log entries als geschiedenis
        for i, log_entry in enumerate(self.battle_log[-4:-1]):
            if i >= 3:  # Max 3 log entries tonen
                break
            log_text = self.font.render(log_entry, True, (200, 200, 200))
            screen.blit(log_text, (230, SCREEN_HEIGHT - 80 + i * 20))
    
    def is_combat_over(self):
        """Controleer of gevecht is beëindigd"""
        return self.combat_over
    
    def get_victory_state(self):
        """Geef aan of speler heeft gewonnen"""
        return self.victory
