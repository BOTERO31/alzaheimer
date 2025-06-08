from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from list import load_collectibles, draw_objectives
from alusinacion import confusion

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
        self.remaining = 40
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
                self.player = Player((marker.x, marker.y), self.all_sprites, self.collision_sprite, self.remaining)

        #Creo un nuevo grupo de objetos recolectables
        self.collectible_group = pygame.sprite.Group()
        #Llamo a la funcion de load collectibles de "list"
        self.lista_objetivo = load_collectibles(map, self.player, self.all_sprites, self.collectible_group)

    def run(self):
        print("remaining", self.remaining)
        
        timer_started = False
        fuente = pygame.font.SysFont('Arial', 34, bold=True)
        invert_keys = False
        game_ended = False  # Nueva variable para controlar si el juego ha terminado
        
        ticks = pygame.time.get_ticks()
        while self.running:
            duracion = 90
            if not game_ended:  # Solo actualizar el tiempo si el juego no ha terminado
                seconds_passed = (pygame.time.get_ticks() - ticks) // 1000
                self.remaining = duracion - seconds_passed
            duracion = 90
            seconds_passed = (pygame.time.get_ticks() - ticks) // 1000
            self.remaining = duracion - seconds_passed
            dt = self.clock.tick() / 500
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if not timer_started:
                        timer_started = True
                        ticks = pygame.time.get_ticks()

            self.all_sprites.update(dt, invert_keys, self.remaining)
            self.all_sprites.draw(self.player.rect.center)
            
            # mostrar contador de puntos
            puntos_text = (f"{self.player.puntos}")
            text = fuente.render(puntos_text, True, (255, 255, 255))
            text_rect = text.get_rect(center=( 1200, 60))
            self.display_surface.blit(text, text_rect)

            # Dibujar la lista de objetivos
            draw_objectives(self.display_surface, self.hoja_objetivos, self.lista_objetivo)
            # Pantalla de inicio
            if not timer_started:
                
                rect = pygame.Rect(WINDOW_WIDTH*0.05,WINDOW_HEIGHT*0.1, WINDOW_WIDTH*0.8, WINDOW_HEIGHT*0.8)
                s = pygame.Surface((WINDOW_WIDTH*0.9, WINDOW_HEIGHT*0.8), pygame.SRCALPHA)  
                s.fill((0, 0, 0, 128))  # Negro con 50% de transparencia
                self.display_surface.blit(s, rect)
                #Movement keys 
                pant_path = os.path.join(BASE_PATH, 'IMAGES', 'p_inicial', 'mov_keys.png')
                self.inicio_pantalla = pygame.image.load(pant_path).convert_alpha()
                self.inicio_pantalla = pygame.transform.scale(self.inicio_pantalla, (300, 300))
                self.display_surface.blit(self.inicio_pantalla, (WINDOW_WIDTH*0.2, WINDOW_HEIGHT*0.3))
                move_text = "Te mueves con:"
                text = fuente.render(move_text, True, (255, 255, 255))
                text_rect = text.get_rect(center=(WINDOW_WIDTH*0.3, WINDOW_HEIGHT*0.3))
                self.display_surface.blit(text, text_rect)

                #E key
                pant_path = os.path.join(BASE_PATH, 'IMAGES', 'p_inicial', 'e_key.png')
                self.inicio_pantalla = pygame.image.load(pant_path).convert_alpha()
                self.inicio_pantalla = pygame.transform.scale(self.inicio_pantalla, (200, 200))
                self.display_surface.blit(self.inicio_pantalla, (WINDOW_WIDTH*0.6, WINDOW_HEIGHT*0.3))
                e_text = "Recoges objetos con:"
                text = fuente.render(e_text, True, (255, 255, 255))
                text_rect = text.get_rect(center=(WINDOW_WIDTH*0.7, WINDOW_HEIGHT*0.3))
                self.display_surface.blit(text, text_rect)
                #texto extra
                extra_text = "Presiona cualquier tecla para comenzar"
                text = fuente.render(extra_text, True, (255, 255, 255))
                text_rect = text.get_rect(center=(WINDOW_WIDTH*0.5, WINDOW_HEIGHT*0.7))
                self.display_surface.blit(text, text_rect)
            if timer_started:
                
                if self.remaining < 0:
                    self.remaining = 0
                if self.remaining < 60 and self.remaining > 15:
                    invert_keys = True
                if self.remaining < 30:
                    confusion(self.display_surface)

                minutes = self.remaining // 60
                seconds = self.remaining % 60
                time_text = f"{minutes:01}:{seconds:02}"
                text = fuente.render(time_text, True, (255, 255, 255))
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 60))
                self.display_surface.blit(text, text_rect)

                t_usado = duracion - self.remaining
                used_minutes = t_usado // 60
                used_seconds = t_usado % 60
                if not all(valor == 0 for valor in self.lista_objetivo.values()) and self.remaining == 0:
                    game_ended = True  # Detener el contador
                    self.display_surface.fill(BLACK)
                    
                    # Lista de líneas de texto
                    lines = [
                        "Has perdido",
                        f"Tiempo: {used_minutes:01}:{used_seconds:02}",
                        f"PUNTUACION: {self.player.puntos}",
                        "Esc para salir"
                    ]
                    # Renderizar cada línea
                    y_offset = WINDOW_HEIGHT // 2 - (len(lines) * 20) // 2
                    for line in lines:
                        text = fuente.render(line, True, (255, 255, 255))
                        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
                        self.display_surface.blit(text, text_rect)
                        y_offset += 80  # Espacio entre líneas
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_ESCAPE]:
                        self.running = False
                elif all(valor == 0 for valor in self.lista_objetivo.values()):
                    game_ended = True  # Detener el contador
                    self.display_surface.fill(BLACK)
                    # Lista de líneas de texto
                    lines = [
                        "Has ganado",
                        f"Tiempo: {used_minutes:01}:{used_seconds:02}",
                        f"PUNTUACION: {self.player.puntos}",
                        "Esc para salir"
                    ]
                    # Renderizar cada línea
                    y_offset = WINDOW_HEIGHT // 2 - (len(lines) * 20) // 2
                    for line in lines:
                        text = fuente.render(line, True, (255, 255, 255))
                        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
                        self.display_surface.blit(text, text_rect)
                        y_offset += 80  # Espacio entre líneas
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_ESCAPE]:
                        self.running = False
    
            pygame.display.flip()
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()