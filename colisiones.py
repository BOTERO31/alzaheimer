import pygame
from constantes import *
from estante import Tile
from alzheimer import Player

class Colitions:
    def __init__(self):
        self.display_surface = pygame.dysplay.get_surface()

        self.visible_sprites = pygame.sprite.Group()    
        self.obstacle_sprites = pygame.sprite.Group()    

        self.create_map()
        
    def create_map(self):
        for row_index,row in enumerate(SHOP_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                Y = col_index * TILE_SIZE
                if col == 'e':
                    Tile((x,y),[self.visible_sprites])

        

    def run(self):
        # update and draw
        self.visible_sprites.draw(self.display_surface)