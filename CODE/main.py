from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from list import load_collectibles, draw_objectives

class Game():
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Mind Maze: Supermarket Rush')
        self.clock = pygame.time.Clock()
        self.running = True
        
        #Cargar hoja, la del fondo en la lista de items
        hoja_path = os.path.join(BASE_PATH, 'DATA', 'graphics', 'ui', 'hoja.png')
        self.hoja_objetivos = pygame.image.load(hoja_path).convert_alpha()
        self.hoja_objetivos = pygame.transform.scale(self.hoja_objetivos, (140, 180))

        # groups
        self.collision_sprite = pygame.sprite.Group()

        # setup
        self.setup()

    def setup(self):
        self.generated_items = {}

        # cargar mapa
        tmx_path = os.path.join(BASE_PATH, 'DATA', 'maps', 'store_map.tmx')
        map = load_pygame(tmx_path)

        map_width = map.width * TILE_SIZE
        map_height = map.height * TILE_SIZE

        self.all_sprites = AllSprites(map_width, map_height)

        # cargar capas del mapa
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprite), name=obj.name)

        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprite)

        for marker in map.get_layer_by_name('Entities'):
            if marker.name == 'Player':
                self.player = Player((marker.x, marker.y), self.all_sprites, self.collision_sprite)

        #Creo un nuevo grupo de objetos recolectables
        self.collectible_group = pygame.sprite.Group()
        #Llamo a la funcion de load collectibles de "list"
        self.lista_objetivo = load_collectibles(map, self.player, self.all_sprites, self.collectible_group)

    def run(self):
        ticks = pygame.time.get_ticks()
        duracion = 40
        timer_started = False
        fuente = pygame.font.SysFont('Arial', 64, bold=True)

        while self.running:
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if not timer_started:
                        timer_started = True
                        ticks = pygame.time.get_ticks()

            self.all_sprites.update(dt)
            self.all_sprites.draw(self.player.rect.center)
            draw_objectives(self.display_surface, self.hoja_objetivos, self.lista_objetivo)

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
                text = fuente.render(time_text, True, (255, 255, 255))
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 60))
                self.display_surface.blit(text, text_rect)

                if remaining == 0:
                    self.running = False

            pygame.display.flip()
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()