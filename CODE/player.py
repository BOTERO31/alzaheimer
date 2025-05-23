import pygame
import os
from settings import *
from sprites import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = 'left', 0
        
        # Obtener la ruta base del proyecto
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Construir la ruta completa a la imagen
        image_path = os.path.join(base_path, 'IMAGES', 'player', 'down', '1.png')
        
      
            # Cargar y escalar la imagen
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (125, 125))
        self.rect = self.image.get_rect(center = pos)
        self.hitbox_rect = self.rect.inflate(-65, -100)
        
        #try:
            # Debug: Imprimir información de posición y tamaño
            #print(f"Player initialized at position: {pos}")
            #print(f"Player rect: {self.rect}")
            #print(f"Player hitbox: {self.hitbox_rect}")
        #except Exception as e:
            #print(f"Error loading player image: {e}")
            # Crear una superficie temporal roja para debug
            #self.image = pygame.Surface((125, 125))
            #self.image.fill((255, 0, 0))
        
        
        # movement
        self.direction = pygame.Vector2()
        self.speed = 100  
        self.collision_sprites = collision_sprites
        
    def load_images(self):
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}
        
        # Obtener la ruta base del proyecto
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        for state in self.frames.keys():
            # Construir la ruta completa al directorio de sprites
            sprite_path = os.path.join(base_path, 'IMAGES', 'player', state)
            if os.path.exists(sprite_path):
                for file_name in sorted(os.listdir(sprite_path)):
                    if file_name.endswith('.png'):
                        full_path = os.path.join(sprite_path, file_name)
                        surf = pygame.transform.scale(pygame.image.load(full_path).convert_alpha(), (125, 125))
                        self.frames[state].append(surf)
            
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        #self.direction = self.direction.normalize() if self.direction else self.direction
    
    def move(self, dt):
        
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collisions('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collisions('vertical')
        
        self.rect.center = self.hitbox_rect.center
        
        # Mantener al jugador dentro de los límites del mapa
        #self.rect.clamp_ip(pygame.Rect(0, 0, 2048, 2048))  # Ajustar estos valores según el tamaño del mapa
        self.rect.center = self.hitbox_rect.center 
    
    def collisions(self, direction):
        for sprites in self.collision_sprites:
            if sprites.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprites.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprites.rect.right
                    self.direction.x = 0
                else:
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprites.rect.top
                    if self.direction.y < 0: self.hitbox_rect.top = sprites.rect.bottom
                    self.direction.y = 0
    
    def animate(self, dt):
        # get state
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'
        
        # basic animation
        self.frame_index = self.frame_index + 7 * dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
    
    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)