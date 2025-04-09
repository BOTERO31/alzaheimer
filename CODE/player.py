import pygame 
from os.path import join


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, obstacle_sprites):
        super().__init__()
        self.sprites_down = []
        self.sprites_up = []
        self.sprites_left = []
        self.sprites_right = []
        self.is_animating = False
        self.current_direction = 'down'  # Track current direction
        
        sprite_size = (125, 125)  # Cambia este tamaño según lo que necesites
#sprites up animation
        self.sprites_up.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'up', 'up_sprite1.png')), sprite_size))
        self.sprites_up.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'up', 'up_sprite2.png')), sprite_size))
        self.sprites_up.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'up', 'up_sprite3.png')), sprite_size))
        self.sprites_up.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'up', 'up_sprite4.png')), sprite_size))
        self.sprites_up.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'up', 'up_sprite5.png')), sprite_size))
        self.sprites_up.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'up', 'up_sprite6.png')), sprite_size))
        self.sprites_up.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'up', 'up_sprite7.png')), sprite_size))
        # Load down sprites
        self.sprites_down.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'down', 'down_sprite1.png')), sprite_size))
        self.sprites_down.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'down', 'down_sprite2.png')), sprite_size))
        self.sprites_down.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'down', 'down_sprite3.png')), sprite_size))
        self.sprites_down.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'down', 'down_sprite4.png')), sprite_size))
        self.sprites_down.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'down', 'down_sprite5.png')), sprite_size))
        self.sprites_down.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'down', 'down_sprite6.png')), sprite_size))
        self.sprites_down.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'down', 'down_sprite7.png')), sprite_size))
        # Load left sprites 
        self.sprites_left.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'left', 'left_sprite1.png')), sprite_size))
        self.sprites_left.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'left', 'left_sprite2.png')), sprite_size))
        self.sprites_left.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'left', 'left_sprite3.png')), sprite_size))
        self.sprites_left.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'left', 'left_sprite4.png')), sprite_size))
        self.sprites_left.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'left', 'left_sprite5.png')), sprite_size))
        self.sprites_left.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'left', 'left_sprite6.png')), sprite_size))
        self.sprites_left.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'left', 'left_sprite7.png')), sprite_size))
        self.sprites_left.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'left', 'left_sprite8.png')), sprite_size))
        # Load right sprites    
        self.sprites_right.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'right', 'right_sprite1.png')), sprite_size))
        self.sprites_right.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'right', 'right_sprite2.png')), sprite_size))
        self.sprites_right.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'right', 'right_sprite3.png')), sprite_size))
        self.sprites_right.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'right', 'right_sprite4.png')), sprite_size))    
        self.sprites_right.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'right', 'right_sprite5.png')), sprite_size))
        self.sprites_right.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'right', 'right_sprite6.png')), sprite_size))
        self.sprites_right.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'right', 'right_sprite7.png')), sprite_size))
        self.sprites_right.append(pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'right', 'right_sprite8.png')), sprite_size))
        
        self.current_sprite = 0
        self.image = self.sprites_down[0]

        self.speed = 5
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-30, -35)  # Make hitbox smaller than rect
        
        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = obstacle_sprites

    def inputs(self, keys):
        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.current_direction = 'down'
            self.animate()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.current_direction = 'up'
            self.animate()

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.current_direction = 'left'
            self.animate()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.current_direction = 'right'
            self.animate()


    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collisions('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collisions('vertical')
        self.rect.center = self.hitbox.center

    #Colisiones personaje
    def collisions(self, direction):
        if direction == 'horizontal': 
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # Moving right
                        self.animate()  # Trigger animation on collision
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:  # Moving left
                        self.animate()  # Trigger animation on collision
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # Moving down
                        self.animate()  # Trigger animation on collision
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:  # Moving up
                        self.animate()  # Trigger animation on collision
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
