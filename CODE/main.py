from settings import *
from player import Player

class Game:
    def __init__(self):
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Mind Maze: Supermarket Rush')
        self.clock = pygame.time.Clock()
        self.running = True
        
        # background for now
        self.background = pygame.image.load(join('CODE', 'tile.png')).convert_alpha()
        
        # Groups
        self.all_sprites = pygame.sprite.Group()
        
        # Sprites
        self.player = Player((400,300), self.all_sprites)
        
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
            self.display_surface.fill('black')
            self.display_surface.blit(self.background, (0,0))
            self.all_sprites.update(dt)
            
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()
            
        pygame.quit()
        
if __name__ =='__main__':
    game = Game()
    game.run()