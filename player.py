import pygame 
import os


ruta_sprite = "prite","Sprites viejito","Up sprites"
ruta_tiles = "tiles"
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

        self.image = self.sprites_up[self.current_sprite]
        self.image = self.sprites_down[self.current_sprite]
        self.image = self.sprites_left[self.current_sprite]
        self.image = self.sprites_right[self.current_sprite]

        self.speed = 5
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-30, -35)  # Make hitbox smaller than rect
        
        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = obstacle_sprites

    def inputs(self, keys):
        if keys[pygame.K_DOWN]:  # Movimiento hacia abajo
            self.animate()
            self.direction.y = 1
            self.current_direction = 'down'
        elif keys[pygame.K_UP]:  # Movimiento hacia arriba
            self.animate()
            self.direction.y = -1
            self.current_direction = 'up'
        else:
            self.direction.y = 0
        if keys[pygame.K_LEFT]:  # Movimiento hacia la izquierda
            self.animate()
            self.direction.x = -1
            self.current_direction = 'left'
        elif keys[pygame.K_RIGHT]:  # Movimiento hacia la derecha
            self.animate()
            self.direction.x = 1
            self.current_direction = 'right'
        else:
            self.direction.x = 0

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
            self.current_sprite += 0.1  # Use a fixed animation speed
            if self.current_sprite >= len(self.sprites_up):
                self.current_sprite = 0
                self.is_animating = False
            
            # Use the appropriate sprite list based on direction
            if self.current_direction == 'up':
                self.image = self.sprites_up[int(self.current_sprite)]  
            elif self.current_direction == 'down':
                self.image = self.sprites_down[int(self.current_sprite)]
            elif self.current_direction == 'left':
                self.image = self.sprites_left[int(self.current_sprite)]
            elif self.current_direction == 'right':
                self.image = self.sprites_right[int(self.current_sprite)]