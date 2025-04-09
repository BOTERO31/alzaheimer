# import pygame

# class Camera(pygame.sprite.Group):
#     def __init__(self):
#         super().__init__()
#         self.display_surface = pygame.display.get_surface()
#         self.offset = pygame.math.Vector2()

#     def modify_draw(self, player):
#         self.offset.x = player.rect.centerx - self.display_surface.get_width() // 2
#         self.offset.y = player.rect.centery - self.display_surface.get_height() // 2

#         for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
#             offset_pos = sprite.rect.topleft - self.offset
#             self.display_surface.blit(sprite.image, offset_pos)