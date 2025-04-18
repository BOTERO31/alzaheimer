from settings import*

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = 'left', 0
        self.image = pygame.transform.scale(pygame.image.load(join('IMAGES', 'player', 'down', '1.png')).convert_alpha(), (125, 125))
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-65,-100)
        
        # movement
        self.direction = pygame.Vector2()
        self.speed = 200
        self.collision_sprites = collision_sprites
        
    def load_images(self):
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}
        
        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('IMAGES', 'player', state)):
                if file_names:
                    for file_name in sorted(file_names, key = lambda name: name.split('.')[1]):
                        full_path = join(folder_path, file_name)
                        surf = pygame.transform.scale(pygame.image.load(full_path).convert_alpha(), (125, 125))
                        self.frames[state].append(surf)
            
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN] - int(keys[pygame.K_UP]))
        self.direction = self.direction.normalize() if self.direction else self.direction
    
    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collisions('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collisions('vertical')
        
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
    
    def animate (self, dt):
        # get state
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0  else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0  else 'up'
        
        # basic animation
        self.frame_index = self.frame_index + 7 * dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
        
    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)