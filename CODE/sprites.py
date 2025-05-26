from settings import *
import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.ground = True
        
        
class CollisionSprite(Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.ground = False
        self.hitbox = self.rect.inflate(-10, -10)  # Ajustar el tamaño del hitbox para colisiones más precisas