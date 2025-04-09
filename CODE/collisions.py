import pygame
from settings import *
from camera import *
from objects import Estante
from player import Player
from items import Manzana
# from items import Manzana

class Collisions:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()    
        self.obstacle_sprites = pygame.sprite.Group()
        self.items_sprites = pygame.sprite.Group() 
        self.create_map()
    
    def create_map(self):
        for row_index, row in enumerate(SHOP_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if col == 'e':
                    Estante((x, y), [self.visible_sprites, self.obstacle_sprites])
                elif col == 'p':
                    self.player = Player((x, y), self.obstacle_sprites)
                    self.visible_sprites.add(self.player)
                elif col == 'i':
                    Manzana((x, y), [self.visible_sprites, self.items_sprites])