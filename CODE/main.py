import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from settings import *
from player import Player
from sprites import *
from random import randint
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from os.path import join

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
class Game():
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Mind Maze: Supermarket Rush')
        self.clock = pygame.time.Clock()
        self.running = True
        
        # group
        self.collision_sprite = pygame.sprite.Group()
        
        self.setup()

        # sprites
        
    def setup(self):
        # Obtener la ruta base del proyecto
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Construir la ruta completa al archivo TMX
        tmx_path = os.path.join(base_path, 'DATA', 'maps', 'store_map.tmx')
        map = load_pygame(tmx_path)
        
        map_width = map.width * TILE_SIZE
        map_height = map.height * TILE_SIZE
        
        # group with map sizes
        self.all_sprites = AllSprites(map_width, map_height)
        
        
        for x,y,image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, self.all_sprites)
            
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprite))
            
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprite)
            
        for marker in map.get_layer_by_name('Entities'):
            if marker.name == 'Player':
                self.player = Player((marker.x, marker.y), self.all_sprites, self.collision_sprite )




    def run(self):
        # Inicializar el temporizador
        ticks = pygame.time.get_ticks()
        duracion = 60
        timer_started = False
        fuente = pygame.font.SysFont(None, 36)
        invert_keys = False
        
        while self.running:
            # dt
            dt = self.clock.tick() / 1000
            
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Detectar cuando se presiona la tecla UP
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if not timer_started:
                        timer_started = True
                        ticks = pygame.time.get_ticks()
        
            # update
            self.all_sprites.update(dt, invert_keys)
            
            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            
            # Actualizar el temporizador si está activo
            if timer_started:
                seconds_passed = (pygame.time.get_ticks() - ticks) // 1000
                remaining = duracion - seconds_passed
                if remaining < 0:
                    remaining = 0

                minutes = remaining // 60
                seconds = remaining % 60
                time_text = f"{minutes:01}:{seconds:02}"
                text = fuente.render(time_text, True, (0, 0, 0))
                self.display_surface.blit(text, (120, 60))
                if remaining == 30:
                    invert_keys = True
                if remaining == 0:
                    self.running = False
            
            pygame.display.update()
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()