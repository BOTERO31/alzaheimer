import pygame


pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Mind maze: Supermarket rush')

BG = (255, 255, 255 )

#Sprites y animación 

class player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.is_animating = False
        self.sprites.append(pygame.image.load('grandpa_sprite1.png'))
        self.sprites.append(pygame.image.load('grandpa_sprite2.png'))
        self.sprites.append(pygame.image.load('grandpa_sprite3.png'))
        self.sprites.append(pygame.image.load('grandpa_sprite4.png'))
        self.sprites.append(pygame.image.load('grandpa_sprite5.png'))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.speed = 2
        self.direction = pygame.math.Vector2()

    def inputs(self):
        if key[pygame.K_s] == True:
            player_pos.animate()
            self.direction.y = 1
        elif key[pygame.K_w] == True:
            player_pos.animate()
            self.direction.y = -1
        else:
            self.direction.y = 0
        if key[pygame.K_a] == True:
            player_pos.animate()
            self.direction.x = -1
        elif key[pygame.K_d] == True:
            player_pos.animate()
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.center += self.direction * speed

    def animate(self):
        self.is_animating  = True
        
    def update(self, speed):
        if self.is_animating == True:
            self.current_sprite += speed
            
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False

            self.image = self.sprites[int(self.current_sprite)]
            
        self.inputs()
        self.move(self.speed)

pygame.init()
clock = pygame.time.Clock()

moving_sprites = pygame.sprite.Group()
player_pos = player(10, 10)
moving_sprites.add(player_pos)

run = True
while run:
    
    key = pygame.key.get_pressed()
    screen.fill(BG)
    moving_sprites.draw(screen)
    moving_sprites.update(0.1)
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False

    pygame.display.flip()
    pygame.display.update()

pygame.quit()