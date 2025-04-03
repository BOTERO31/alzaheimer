# Importar las librerías necesarias
import pygame
import constantes  
import os

# Inicializar todos los módulos necesarios de Pygame
pygame.init()

# Crear la ventana del juego con el tamaño definido previamente
ventana = pygame.display.set_mode((constantes.ancho_ventana, constantes.alto_ventana))
pygame.display.set_caption("Supermarket Rush")

# Colores y velocidad del personaje
x = 100
y = 100
velocidad = 4

#Join imagen
ruta_tiles = "tiles"

#Imagen
background = pygame.image.load(os.path.join(ruta_tiles, "tile.png"))

# Clase del jugador con sprites y animación
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.is_animating = False
        
        # Escalar las imágenes al tamaño deseado
        sprite_size = (120, 120)  # Cambia este tamaño según lo que necesites
        
        self.sprites.append(pygame.transform.scale(pygame.image.load(os.path.join(ruta_tiles, 'up_sprite_1.png')), sprite_size))
        self.sprites.append(pygame.transform.scale(pygame.image.load(os.path.join(ruta_tiles, 'up_sprite_2.png')), sprite_size))
        self.sprites.append(pygame.transform.scale(pygame.image.load(os.path.join(ruta_tiles, 'up_sprite_3.png')), sprite_size))
        self.sprites.append(pygame.transform.scale(pygame.image.load(os.path.join(ruta_tiles, 'up_sprite_4.png')), sprite_size))
        self.sprites.append(pygame.transform.scale(pygame.image.load(os.path.join(ruta_tiles, 'up_sprite_5.png')), sprite_size))
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.speed = 5
        self.direction = pygame.math.Vector2()

    def inputs(self, keys):
        if keys[pygame.K_DOWN]:  # Movimiento hacia abajo
            self.animate()
            self.direction.y = 1
        elif keys[pygame.K_UP]:  # Movimiento hacia arriba
            self.animate()
            self.direction.y = -1
        else:
            self.direction.y = 0
        if keys[pygame.K_LEFT]:  # Movimiento hacia la izquierda
            self.animate()
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:  # Movimiento hacia la derecha
            self.animate()
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.center += self.direction * self.speed

    def animate(self):
        self.is_animating = True

    def update(self, speed, keys):
        self.inputs(keys)
        self.move()
        if self.is_animating:
            self.current_sprite += speed
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False
            self.image = self.sprites[int(self.current_sprite)]

# Inicializar jugador y grupo de sprites
moving_sprites = pygame.sprite.Group()
player_pos = Player(x, y)
moving_sprites.add(player_pos)

# Dibujar la cuadrícula
def dibujar_grid():
    for x in range(30):
        pygame.draw.line(ventana, constantes.BLANCO, (x * 40, 0), (x * 40, constantes.alto_ventana)) 
        pygame.draw.line(ventana, constantes.BLANCO, (0, x * 40), (constantes.ancho_ventana, x * 40))

# Bucle principal del juego
corriendo = True
reloj = pygame.time.Clock()

while corriendo:
    keys = pygame.key.get_pressed()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    # Rellenar la ventana con el color de fondo
    ventana.fill(constantes.NEGRO)
    dibujar_grid()
    
    #background
    ventana.blit(background, (0,0))

    # Actualizar y dibujar el sprite animado del jugador
    moving_sprites.update(0.1, keys)
    moving_sprites.draw(ventana)

    # Actualizar la pantalla
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
