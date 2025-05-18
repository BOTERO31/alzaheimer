import pygame 
import os
from constantes import *



ruta_sprite = "prite","Sprites viejito","Up sprites"
ruta_tiles = "tiles"
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.sprites_down = []
        self.sprites_up = []
        self.sprites_left = []
        self.sprites_right = []
        self.is_animating = False
        self.current_direction = 'down'
        
        sprite_size = (125, 125)
        
        # Obtener la ruta base del proyecto
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Construir la ruta completa a la imagen
        image_path = os.path.join(base_path, 'DATA', 'graphics', 'player', 'down', 'down_0.png')
        
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-30, -35)
        
        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = collision_sprites

        # Load up sprites
        self.sprites_up.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Up sprites', 'grandpa_sprite1.png')), sprite_size))
        self.sprites_up.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Up sprites', 'grandpa_sprite2.png')), sprite_size))
        self.sprites_up.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Up sprites', 'grandpa_sprite3.png')), sprite_size))
        self.sprites_up.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Up sprites', 'grandpa_sprite4.png')), sprite_size))
        self.sprites_up.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Up sprites', 'grandpa_sprite5.png')), sprite_size))
        self.sprites_up.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Up sprites', 'grandpa_sprite6.png')), sprite_size))
        self.sprites_up.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Up sprites', 'grandpa_sprite7.png')), sprite_size))

        # Load down sprites
        self.sprites_down.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Down sprites', 'grandpa_sprite1.png')), sprite_size))
        self.sprites_down.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Down sprites', 'grandpa_sprite2.png')), sprite_size))
        self.sprites_down.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Down sprites', 'grandpa_sprite3.png')), sprite_size))
        self.sprites_down.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Down sprites', 'grandpa_sprite4.png')), sprite_size))
        self.sprites_down.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Down sprites', 'grandpa_sprite5.png')), sprite_size))
        self.sprites_down.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Down sprites', 'grandpa_sprite6.png')), sprite_size))
        self.sprites_down.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Down sprites', 'grandpa_sprite7.png')), sprite_size))

        # Load left sprites
        self.sprites_left.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Left sprites', 'grandpa_sprite1.png')), sprite_size))
        self.sprites_left.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Left sprites', 'grandpa_sprite2.png')), sprite_size))
        self.sprites_left.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Left sprites', 'grandpa_sprite3.png')), sprite_size))
        self.sprites_left.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Left sprites', 'grandpa_sprite4.png')), sprite_size))
        self.sprites_left.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Left sprites', 'grandpa_sprite5.png')), sprite_size))
        self.sprites_left.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Left sprites', 'grandpa_sprite6.png')), sprite_size))
        self.sprites_left.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Left sprites', 'grandpa_sprite7.png')), sprite_size))
        self.sprites_left.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Left sprites', 'grandpa_sprite8.png')), sprite_size))

        # Load right sprites
        self.sprites_right.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Right sprites', 'grandpa_sprite1.png')), sprite_size))
        self.sprites_right.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Right sprites', 'grandpa_sprite2.png')), sprite_size))
        self.sprites_right.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Right sprites', 'grandpa_sprite3.png')), sprite_size))
        self.sprites_right.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Right sprites', 'grandpa_sprite4.png')), sprite_size))
        self.sprites_right.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Right sprites', 'grandpa_sprite5.png')), sprite_size))
        self.sprites_right.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Right sprites', 'grandpa_sprite6.png')), sprite_size))
        self.sprites_right.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Right sprites', 'grandpa_sprite7.png')), sprite_size))
        self.sprites_right.append(pygame.transform.scale(pygame.image.load(os.path.join('sprite', 'Sprites viejito', 'Right sprites', 'grandpa_sprite8.png')), sprite_size))

        self.current_sprite = 0
        self.speed = 5

    def inputs(self, keys):
        if keys[pygame.K_DOWN]:
            self.animate()
            self.direction.y = 1
            self.current_direction = 'down'
        elif keys[pygame.K_UP]:
            self.animate()
            self.direction.y = -1
            self.current_direction = 'up'
        else:
            self.direction.y = 0
        if keys[pygame.K_LEFT]:
            self.animate()
            self.direction.x = -1
            self.current_direction = 'left'
        elif keys[pygame.K_RIGHT]:
            self.animate()
            self.direction.x = 1
            self.current_direction = 'right'
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collisions('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collisions('vertical')
        self.rect.center = self.hitbox.center

    def collisions(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.animate()
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.animate()
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.animate()
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:
                        self.animate()
                        self.hitbox.top = sprite.hitbox.bottom

    def animate(self):
        self.is_animating = True

    def update(self, speed, keys):
        self.inputs(keys)
        self.move(speed)
        if self.is_animating:
            self.current_sprite += 0.1
            if self.current_sprite >= len(self.sprites_up):
                self.current_sprite = 0
                self.is_animating = False
            
            if self.current_direction == 'up':
                self.image = self.sprites_up[int(self.current_sprite)]
            elif self.current_direction == 'down':
                self.image = self.sprites_down[int(self.current_sprite)]
            elif self.current_direction == 'left':
                self.image = self.sprites_left[int(self.current_sprite)]
            elif self.current_direction == 'right':
                self.image = self.sprites_right[int(self.current_sprite)]