from settings import *
from player import Player

class AllSprites(pygame.sprite.Group):
    def __init__(self, map_width, map_height):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()
        self.map_width = map_width
        self.map_height = map_height
        
    def draw(self, target_pos):
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)
    
        self.offset.x = max(-(self.map_width - WINDOW_WIDTH), min(0, self.offset.x))
        self.offset.y = max(-(self.map_height - WINDOW_HEIGHT), min(0, self.offset.y))
    
        ground_sprites = [s for s in self if hasattr(s, 'ground')]
        for sprite in ground_sprites:
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)
    
        object_sprites = [s for s in self if not hasattr(s, 'ground') or not s.ground]
        valid_sprites = [s for s in object_sprites if hasattr(s, 'rect') and s.rect is not None]
    
        top_layer_sprites = [s for s in valid_sprites if hasattr(s, 'top_layer') and s.top_layer]
        normal_sprites = [s for s in valid_sprites if not hasattr(s, 'top_layer') or not s.top_layer]
    
        for sprite in sorted(normal_sprites, key=lambda s: s.rect.centery):
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)
    
        for sprite in top_layer_sprites:
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)