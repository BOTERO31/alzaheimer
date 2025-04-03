from settings import *

# Scale
player_scale = (100,100)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('IMAGES', 'player', 'up', 'up_sprite_1.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, player_scale)
        self.rect = self.image.get_frect(center = pos)
        
        # Movement
        self.direction = pygame.Vector2(1,0)
        self.speed = 400
        
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
    
    def move(self, dt):
        self.rect.center += self.direction * self.speed * dt
    
    def update(self, dt):
        self.input()
        self.move(dt)
        