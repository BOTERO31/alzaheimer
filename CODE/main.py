from settings import *
from player import Player
from sprites import *
from random import randint
from pytmx.util_pygame import load_pygame
from groups import AllSprites

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
class Game():
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Mind Maze: Supermarket Rush')
        self.clock = pygame.time.Clock()
        self.running = True
        
        # group
        self.collision_sprite = pygame.sprite.Group()

        # setup
        self.setup()

    def setup(self):
        # Construir la ruta completa al archivo TMX
        tmx_path = os.path.join(BASE_PATH, 'DATA', 'maps', 'store_map.tmx')
        map = load_pygame(tmx_path)
        
        map_width = map.width * TILE_SIZE
        map_height = map.height * TILE_SIZE
        
        # group with map sizes
        self.all_sprites = AllSprites(map_width, map_height)
        
        
        for x,y,image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, self.all_sprites)
            
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprite), name=obj.name)
            
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprite)
            
        for marker in map.get_layer_by_name('Entities'):
            if marker.name == 'Player':
                self.player = Player((marker.x, marker.y), self.all_sprites, self.collision_sprite )

        self.collectible_group = pygame.sprite.Group()

        for obj in map.get_layer_by_name('Collectibles'):
            Collectible((obj.x, obj.y), obj.image, (self.all_sprites, self.collectible_group), player_group=pygame.sprite.GroupSingle(self.player), name=obj.name)

    def run(self):
        # Inicializar el temporizador
        ticks = pygame.time.get_ticks()
        duracion = 40
        timer_started = False
        fuente = pygame.font.SysFont('Arial', 64, bold=True)
        invert_keys = False
        while self.running:
            # dt
            dt = self.clock.tick() / 300
            
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Detectar cuando se presiona la tecla UP
                if event.type == pygame.KEYDOWN:
                    if not timer_started:
                        timer_started = True
                        ticks = pygame.time.get_ticks()
        
            # update
            self.all_sprites.update(dt, invert_keys)
            
            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            
            # Actualizar el temporizador si está activo
            if timer_started:
                seconds_passed = (pygame.time.get_ticks() - ticks) // 1000
                remaining = duracion - seconds_passed
                if remaining < 0:
                    remaining = 0
                if remaining == 30:
                    invert_keys = True
                minutes = remaining // 60
                seconds = remaining % 60
                time_text = f"{minutes:01}:{seconds:02}"
                text = fuente.render(time_text, True, (255, 255, 255))  # texto blanco
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 60))
                self.display_surface.blit(text, text_rect)

                if remaining == 0:
                    self.running = False
            
            pygame.display.flip()
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()