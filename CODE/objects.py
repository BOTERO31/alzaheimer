import pygame
from settings import *

ruta_sprite = 'DATA', 'tilesets'

class Estante(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('IMAGES', 'objects', 'tile_shelf1.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-75, -120)