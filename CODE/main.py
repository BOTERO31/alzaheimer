from settings import *
from player import Player
from sprites import *
from random import randint  

class Game:
    def __init__(self):
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Mind Maze: Supermarket Rush')
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Groups    
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        
        # Sprites
        self.player = Player((400,300), self.all_sprites, self.collision_sprites)
        for i in range(6):
            x, y  = randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)
            w, h = randint(50, 100), randint(50, 100)
            CollisionSprite((x, y), (w, h), (self.all_sprites, self.collision_sprites))
        
    def run(self):
        while self.running:
            # dt
            dt = self.clock.tick() / 1000
            
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            # update
            
            # draw
            self.display_surface.fill('white')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()
            
        pygame.quit()
        
if __name__ =='__main__':
    game = Game()
    game.run()