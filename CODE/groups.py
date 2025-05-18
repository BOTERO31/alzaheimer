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
        # Calculate offset to center the target position
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)
        
        # Clamp the offset to keep the camera within map bounds
        self.offset.x = max(-(self.map_width - WINDOW_WIDTH), min(0, self.offset.x))
        self.offset.y = max(-(self.map_height - WINDOW_HEIGHT), min(0, self.offset.y))
        
        # Debug: Print camera information
        #print(f"Camera offset: {self.offset}")
        #print(f"Target position: {target_pos}")
        
        # Draw ground sprites first
        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        for sprite in ground_sprites:
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)
        
        # Draw other sprites (including player) on top
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground') or not sprite.ground]

        valid_sprites = [sprite for sprite in object_sprites if hasattr(sprite, 'rect') and sprite.rect is not None]

        for sprite in sorted(valid_sprites, key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            