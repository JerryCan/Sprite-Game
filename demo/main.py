# Tri-Sharira RPG Demo
# Hoofdbestand om de game te starten

import pygame
import sys
from src.game import Game
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FPS

def main():
    # Initialiseer Pygame
    pygame.init()
    
    # Maak scherm
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    
    # Maak clock voor framerate controle
    clock = pygame.time.Clock()
    
    # Maak game instance
    game = Game(screen)
    
    # Main game loop
    running = True
    while running:
        # Verwerk events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)
        
        # Update game
        game.update()
        
        # Render
        screen.fill((0, 0, 0))
        game.render()
        pygame.display.flip()
        
        # Begrens framerate
        clock.tick(FPS)
    
    # Cleanup
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
