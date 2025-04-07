import pygame
from constantes import *
import os

ruta_sprite = "sprite"
class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join(ruta_sprite, 'tile_shelf1.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-75, -60)
