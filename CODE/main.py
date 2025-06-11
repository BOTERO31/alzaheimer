from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from list import load_collectibles, draw_objectives
from blur_vision import confusion
from puntuacion import Puntuacion
from memory_lost import MemoryLossManager
from shadow_text import draw_shadowed_text

class Game():
    def __init__(self):
        # setup
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(8)  # Configurar 8 canales
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Mind Maze: Supermarket Rush')
        self.clock = pygame.time.Clock()
        self.running = True
        self.duracion = 90
        
        # Mostrar pantalla de presentación con logo
        self.show_logo()

        #Mostrar mensajes
        self.invertido = False
        self.texto_invertido_mostrado = False
        self.texto_confusion_mostrado = False
        self.texto_inicial = False
        self.mensaje_mostrado_timer = 0
        self.mensaje_extra_actual = None


        #Perdida de memoria
        self.memory_loss_manager = MemoryLossManager(intervalo=30)
        
        # Configuración de canales de audio
        self.music_channel = pygame.mixer.Channel(0)
        self.ambient_channel = pygame.mixer.Channel(1)
        self.effects_channel = pygame.mixer.Channel(2)
        
        # Inicializar sistema de puntuación
        self.puntuacion = Puntuacion()
        
        #Cargar hoja, la del fondo en la lista de items
        hoja_path = os.path.join(BASE_PATH, 'DATA', 'graphics', 'ui', 'hoja.png')
        self.hoja_objetivos = pygame.image.load(hoja_path).convert_alpha()
        self.hoja_objetivos = pygame.transform.scale(self.hoja_objetivos, (140, 180))

        # groups
        self.collision_sprite = pygame.sprite.Group()

        # setup
        self.remaining = 90
        self.setup()
    def reiniciar_juego(self):
        self.display_surface.fill(BLACK)
        pygame.display.flip()
        self.__init__()  # Reinicia el juego desde cero
        self.run()       # Corre el bucle principal de nuevo
        
    def show_logo(self):
        # Pantalla gris
        self.display_surface.fill((100, 100, 100))  # gris claro
        pygame.display.flip()

        # Cargar el logo
        logo_path = os.path.join(BASE_PATH, 'IMAGES', 'logo', 'Alzhaimer.jpg')  # Ajusta la ruta real
        logo = pygame.image.load(logo_path).convert_alpha()
        logo = pygame.transform.scale(logo, (400, 400))  # Ajusta el tamaño a tu gusto

        # Crear una superficie para aplicar fade
        logo_surface = pygame.Surface(logo.get_size(), pygame.SRCALPHA)
        logo_rect = logo.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        # Mostrar durante 5 segundos con fade out en los últimos 2 segundos
        start_time = pygame.time.get_ticks()
        fade_duration = 2000  # milisegundos
        total_duration = 5000

        running = True
        while running:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - start_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display_surface.fill((200, 200, 200))  # Fondo gris

            # Calcular opacidad
            if elapsed < total_duration - fade_duration:
                alpha = 255
            else:
                fade_progress = (elapsed - (total_duration - fade_duration)) / fade_duration
                alpha = int(255 * (1 - fade_progress))

            logo_surface.fill((255, 255, 255, 0))  # fondo transparente
            logo_surface.blit(logo, (0, 0))
            logo_surface.set_alpha(alpha)

            self.display_surface.blit(logo_surface, logo_rect)
            pygame.display.flip()

            if elapsed >= total_duration:
                running = False

            self.clock.tick(60)

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
            sprite = CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprite), name=obj.name)
            if obj.name and obj.name.lower() == 'register':
                self.register_rect = sprite.rect

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
        sound_path_synthom = os.path.join(BASE_PATH,'AUDIO', 'synthom.wav')
        self.synthom_sfx = pygame.mixer.Sound(sound_path_synthom)
        timer_started = False
        fuente = pygame.font.SysFont('Arial', 34, bold=True)
        invert_keys = False
        game_ended = False  # Nueva variable para controlar si el juego ha terminado

        sound_path_music = os.path.join(BASE_PATH,'AUDIO', 'music.mp3')
        self.music = pygame.mixer.Sound(sound_path_music)

        sound_path_ambientation = os.path.join(BASE_PATH,'AUDIO', 'ambientation.mp3')
        self.ambientation = pygame.mixer.Sound(sound_path_ambientation)

        sound_path_loose = os.path.join(BASE_PATH,'AUDIO', 'loose.wav')
        self.loose = pygame.mixer.Sound(sound_path_loose)

        ticks = 0  # Inicializamos ticks en 0

        while self.running:
            if not (game_ended) and timer_started:  # Solo actualizar el tiempo si el juego no ha terminado y el timer ha iniciado
                seconds_passed = (pygame.time.get_ticks() - ticks) // 1000
                self.remaining = self.duracion - seconds_passed
            dt = self.clock.tick() / 500
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if not timer_started:
                        timer_started = True
                        ticks = pygame.time.get_ticks()  # Iniciamos el contador cuando se presiona una tecla
                        self.remaining = 90

            
            self.all_sprites.update(dt, invert_keys, self.remaining)
            self.all_sprites.draw(self.player.rect.center)
            
            # mostrar contador de puntos
            puntos_text = (f"Puntos: {self.player.puntos}")
            text = fuente.render(puntos_text, True, (255, 255, 255))
            text_rect = text.get_rect(center=(1100, 40))
            self.display_surface.blit(text, text_rect)
            
            # mostrar mejor puntuacion
            if self.puntuacion.mejor_puntuacion:
                mejor_puntuacion = self.puntuacion.mejor_puntuacion[0]
                self.best_time = mejor_puntuacion['tiempo']
                best_min = self.best_time // 60
                best_sec = self.best_time%60
                max_puntos_text = f"Mejor: {mejor_puntuacion['puntuacion']} - {best_min:01}:{best_sec:02}"
                text = fuente.render(max_puntos_text, True, (255, 255, 255))
                text_rect = text.get_rect(center=(1100, 80))
                self.display_surface.blit(text, text_rect)

            # Dibujar la lista de objetivos
            draw_objectives(self.lista_objetivo, self.display_surface, self.hoja_objetivos, self.memory_loss_manager)

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
                #iniciar musica
                if not self.music_channel.get_busy():
                    self.music_channel.play(self.music, loops=-1)
                    self.music_channel.set_volume(0.2)
                
                if not self.ambient_channel.get_busy():
                    self.ambient_channel.play(self.ambientation, loops=-1)
                    self.ambient_channel.set_volume(0.1)
                
                if self.remaining == 84:
                    self.synthom_sfx.play()
                    self.synthom_sfx.set_volume(1.0)
                elif self.remaining == 49:
                    self.synthom_sfx.play()
                    self.synthom_sfx.set_volume(1.0)
                elif self.remaining == 19:
                    self.synthom_sfx.play()
                    self.synthom_sfx.set_volume(1.0)

                # Mensaje inicial
                if not self.texto_inicial and self.remaining < 85:
                    self.mensaje_extra_actual = "Recolecta los elementos y llevalos a la caja ante que..."
                    self.mensaje_mostrado_timer = pygame.time.get_ticks()
                    self.texto_inicial = True

                # Mostrar mensajes previos a síntomas con retardo
                if not self.texto_invertido_mostrado and self.remaining < 55:
                    self.mensaje_extra_actual = "¿Hacia dónde era...? ¿Cómo llego?"
                    self.mensaje_mostrado_timer = pygame.time.get_ticks()
                    self.texto_invertido_mostrado = True

                if not self.texto_confusion_mostrado and self.remaining < 25:
                    self.mensaje_extra_actual = "Mi mente se nubla... mi visión se quiebra."
                    self.mensaje_mostrado_timer = pygame.time.get_ticks()
                    self.texto_confusion_mostrado = True

                # Mostrar texto en pantalla durante 3 segundos
                if self.mensaje_extra_actual:
                    tiempo_actual = pygame.time.get_ticks()
                    if tiempo_actual - self.mensaje_mostrado_timer < 5000:
                        draw_shadowed_text(
                            self.display_surface,
                            self.mensaje_extra_actual,
                            fuente,
                            (255, 255, 255),  # color del texto
                            (0, 0, 0),        # color de sombra
                            (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
                        )
                    else:
                        self.mensaje_extra_actual = None

                
                #contador minutos usados
                self.t_usado = self.duracion - self.remaining
                used_minutes = self.t_usado // 60
                used_seconds = self.t_usado % 60

                #Perdida de memoria
                # Perdida de memoria
                self.memory_loss_manager.check_mensaje(self.lista_objetivo)
                self.memory_loss_manager.actualizar(self.lista_objetivo, self.remaining)

                # Mostrar mensaje previo al síntoma
                if self.memory_loss_manager.mostrar_mensaje and self.memory_loss_manager.mensaje_actual:
                    mensaje = str(self.memory_loss_manager.mensaje_actual)
                    draw_shadowed_text(
                            self.display_surface,
                            mensaje,
                            fuente,
                            (255, 255, 255),  # color del texto
                            (0, 0, 0),        # color de sombra
                            (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
                        )
                
                if self.remaining < 0:
                    self.remaining = 0

                # Activar inversión de teclas
                if not self.invertido and 15 < self.remaining < 50:
                    invert_keys = True
                    self.invertido = True

                # Efecto de visión borrosa
                if self.remaining < 20:
                    confusion(self.display_surface)

                # Sonido de derrota inminente
                if self.remaining == 8:
                    self.effects_channel.play(self.loose)
                    self.effects_channel.set_volume(1.0)


                minutes = self.remaining // 60
                seconds = self.remaining % 60
                time_text = f"{minutes:01}:{seconds:02}"
                text = fuente.render(time_text, True, (255, 255, 255))
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 60))
                self.display_surface.blit(text, text_rect)

                
                if not all(valor == 0 for valor in self.lista_objetivo.values()) and self.remaining == 0:
                    game_ended = True  # Detener el contador
                    self.display_surface.fill(BLACK)
                    
                    # Lista de líneas de texto
                    lines = [
                        "Has perdido",
                        f"Tiempo: {used_minutes:01}:{used_seconds:02}",
                        f"PUNTUACION: {self.player.puntos}",
                        "Presiona ESC para salir",
                        "Presiona R para volver al inicio"
                    ]
                    # Renderizar cada línea
                    y_offset = WINDOW_HEIGHT*0.3 - (len(lines) * 20) // 2
                    for line in lines:
                        text = fuente.render(line, True, (255, 255, 255))
                        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
                        self.display_surface.blit(text, text_rect)
                        y_offset += 80  # Espacio entre líneas
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_ESCAPE]:
                        self.running = False
                elif all(valor == 0 for valor in self.lista_objetivo.values()):
                    # Verifica si está tocando la caja registradora
                    if self.player.rect.colliderect(self.register_rect):
                        game_ended = True  # Detener el contador
                        self.display_surface.fill(BLACK)
                        
                        # Guardar la puntuación actual
                        self.puntuacion.guardar_puntuacion(self.player.puntos, self.t_usado)
                        
                        # Lista de líneas de texto
                        lines = [
                            "Has ganado",
                            f"Tiempo: {used_minutes:01}:{used_seconds:02}",
                            f"PUNTUACION: {self.player.puntos}",
                            "Presiona ESC para salir",
                            "Presiona R para volver al inicio"
                        ]
                        # Renderizar cada línea
                        y_offset = WINDOW_HEIGHT*0.3 - (len(lines) * 20) // 2
                        for line in lines:
                            text = fuente.render(line, True, (255, 255, 255))
                            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
                            self.display_surface.blit(text, text_rect)
                            y_offset += 80  # Espacio entre líneas
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_ESCAPE]:
                            self.running = False
                        elif keys[pygame.K_r]:
                            self.running = False
                            self.reiniciar_juego()
            pygame.display.flip()
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()