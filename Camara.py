
import pygame
import colisiones

class Camera(pygame.sprite.Group):
    def __init__(self):

        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def modify_draw(self, player):

        self.offset = pygame.math.Vector2(player.rect.center)
        
        for sprite in self.sprites(): 
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)
        
        