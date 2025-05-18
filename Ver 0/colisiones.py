import pygame
from constantes import *
from estante import Tile
from player import Player
import Camara
class Collisions:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = pygame.sprite.Group()    
        self.obstacle_sprites = pygame.sprite.Group()    

        self.create_map()
    
    def create_map(self):
        
        for row_index,row in enumerate(SHOP_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'e':
                    Tile((x,y),[self.visible_sprites, self.obstacle_sprites])
                else:

                    if col == 'p':
                        self.player = Player((x, y), self.obstacle_sprites)
                        self.visible_sprites.add(self.player)
        
    def run(self):
        # update and draw
        self.visible_sprites.draw(self.player.camera)
        self.visible_sprites.update()

    
